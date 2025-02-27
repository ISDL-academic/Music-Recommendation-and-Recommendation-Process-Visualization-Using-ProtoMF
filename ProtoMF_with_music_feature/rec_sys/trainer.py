import os
import torch
import ray
from ray import train
from torch import nn
from torch.utils import data
from feature_extraction.feature_extractor_factories import FeatureExtractorFactory
from rec_sys.rec_sys import RecSys
from utilities.consts import OPTIMIZING_METRIC, MAX_PATIENCE
from utilities.eval import Evaluator

class Trainer:

    def __init__(self, train_loader: data.DataLoader, val_loader: data.DataLoader, conf, save_path=None):
        """
        Train and Evaluate the model.
        :param train_loader: Training DataLoader
        :param val_loader: Validation DataLoader
        :param conf: Experiment configuration parameters
        """

        self.train_loader = train_loader
        self.val_loader = val_loader

        self.rec_sys_param = conf.rec_sys_param
        self.ft_ext_param = conf.ft_ext_param
        self.optim_param = conf.optim_param

        self.n_epochs = conf.n_epochs
        self.loss_func_name = conf.loss_func_name
        self.loss_func_aggr = conf.loss_func_aggr if 'loss_func_aggr' in conf else 'mean'

        self.device = conf.device

        self.optimizing_metric = OPTIMIZING_METRIC
        self.max_patience = MAX_PATIENCE

        self.model = self._build_model()
        self.optimizer = self._build_optimizer()

        self.save_path = save_path  # Model save path
        print("Model will be saved at: ", save_path)
        print(f'Built Trainer module \n'
              f'- n_epochs: {self.n_epochs} \n'
              f'- loss_func_name: {self.loss_func_name} \n'
              f'- loss_func_aggr: {self.loss_func_aggr} \n'
              f'- device: {self.device} \n'
              f'- optimizing_metric: {self.optimizing_metric} \n')

    def _build_model(self):
        # Step 1 --- Building User and Item Feature Extractors
        n_users = self.train_loader.dataset.n_users
        n_items = self.train_loader.dataset.n_items

        user_feature_extractor, item_feature_extractor = \
            FeatureExtractorFactory.create_models(self.ft_ext_param, n_users, n_items)
       
        # Step 2 --- Building RecSys Module
        rec_sys = RecSys(n_users, n_items, self.rec_sys_param, user_feature_extractor, item_feature_extractor,
                         self.loss_func_name, self.loss_func_aggr)

        rec_sys.init_parameters()
        rec_sys = nn.DataParallel(rec_sys)
        rec_sys = rec_sys.to(self.device)

        return rec_sys

    def _build_optimizer(self):
        self.lr = self.optim_param['lr'] if 'lr' in self.optim_param else 1e-3
        self.wd = self.optim_param['wd'] if 'wd' in self.optim_param else 1e-4

        optim_name = self.optim_param['optim']
        if optim_name == 'adam':
            optim = torch.optim.Adam(self.model.parameters(), lr=self.lr, weight_decay=self.wd)
        elif optim_name == 'adagrad':
            optim = torch.optim.Adagrad(self.model.parameters(), lr=self.lr, weight_decay=self.wd)
        else:
            raise ValueError('Optimizer not yet included')

        print(f'Built Optimizer  \n'
              f'- name: {optim_name} \n'
              f'- lr: {self.lr} \n'
              f'- wd: {self.wd} \n')

        return optim

    def run(self):
        """
        Runs the Training procedure
        """
        metrics_values = self.val()
        best_value = metrics_values[self.optimizing_metric]
        # Initial report to track the starting point
        train.report(metrics_values)
        print('Init - Avg Val Value {:.3f} \n'.format(best_value))

        patience = 0
        for epoch in range(self.n_epochs):

            if patience == self.max_patience:
                print('Max Patience reached, stopping.')
                break

            self.model.train()

            epoch_train_loss = 0

            for u_idxs, i_idxs, labels in self.train_loader:
                u_idxs = u_idxs.to(self.device)
                i_idxs = i_idxs.to(self.device)
                labels = labels.to(self.device)

                out = self.model(u_idxs, i_idxs)

                loss = self.model.module.loss_func(out, labels)

                epoch_train_loss += loss.item()

                loss.backward()
                self.optimizer.step()
                self.optimizer.zero_grad()

            epoch_train_loss /= len(self.train_loader)
            print("Epoch {} - Epoch Avg Train Loss {:.3f} \n".format(epoch, epoch_train_loss))

            metrics_values = self.val()
            curr_value = metrics_values[self.optimizing_metric]
            print('Epoch {} - Avg Val Value {:.3f} \n'.format(epoch, curr_value))
            
            # Report the metrics for each epoch
            metrics_values.update({'epoch_train_loss': epoch_train_loss})  # Add training loss
            train.report(metrics_values)

            if curr_value > best_value:
                best_value = curr_value
                print('Epoch {} - New best model found (val value {:.3f}) \n'.format(epoch, curr_value))

                # Save the model if it is the best one so far
                if self.save_path:
                    model_save_path = os.path.join(self.save_path, 'best_model.pth')
                    os.makedirs(self.save_path, exist_ok=True)  # Create the directory if not exists
                    print(f"Saving model at: {model_save_path}")

                    # Save only model weights
                    torch.save(self.model.module.state_dict(), model_save_path)

                    # Verify if the model was saved correctly
                    if os.path.exists(model_save_path):
                        print(f"Model saved successfully at: {model_save_path}")
                    else:
                        print("Error: Model file not found after saving attempt.")
                
                patience = 0
            else:
                patience += 1

    @torch.no_grad()
    def val(self):
        """
        Runs the evaluation procedure.
        :return: A dictionary with evaluation metrics (e.g., hit ratio, NDCG)
        """
        self.model.eval()
        print('Validation started')
        val_loss = 0
        eval = Evaluator(self.val_loader.dataset.n_users)

        for u_idxs, i_idxs, labels in self.val_loader:
            u_idxs = u_idxs.to(self.device)
            i_idxs = i_idxs.to(self.device)
            labels = labels.to(self.device)

            out = self.model(u_idxs, i_idxs)

            val_loss += self.model.module.loss_func(out, labels).item()

            out = nn.Sigmoid()(out)
            out = out.to('cpu')

            eval.eval_batch(out)

        val_loss /= len(self.val_loader)

        # Debugging output for eval.get_results()
        results = eval.get_results()
        if results is None or not isinstance(results, dict):
            raise ValueError(f"Invalid results from eval.get_results(): {results}")

        # Debugging output for val_loss
        if val_loss is None or not isinstance(val_loss, (float, int)):
            raise ValueError(f"Invalid val_loss value: {val_loss}")

        # Return the evaluation metrics as a dictionary, including validation loss
        metrics_values = {**results, 'val_loss': val_loss}
        return metrics_values
