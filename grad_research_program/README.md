# ProtoMF with Music Features

このリポジトリは、ProtoMFモデルに音源特徴量を加えた音楽推薦システムを構築、そして学習したモデルに関する推薦過程の可視化を行うためのコードとツールを提供します。また、Last.fmデータセットの前処理および音源特徴量の抽出・結合を行う機能も備えています。

---

## 📂 リポジトリ構成
```bash
.
├── README.md
├── data_preprocessing
│   └── CLMR_Lastfm.ipynb
└── main
    ├── ProtoMF_github.ipynb
    └── explanations_util.ipynb
```

### **main**
- **`ProtoMF_github.ipynb`**  
  ProtoMFモデルに音源特徴量を加えたモデルで音楽推薦を実行できます。  
  **主な機能**：
  - 音源特徴量を考慮したProtoMFの音楽推薦モデルのトレーニングおよび評価。
  - ProtoMFの説明可能性を活用したユーザおよびアイテムのプロトタイプ解析。

- **`explanations_util.ipynb`**  
  ProtoMF_github.ipynbで学習した各モデルに関して推薦過程の可視化を行うことができます。
  **主な機能**：
  -  t-SNEを用いた埋め込みベクトルとプロトタイプベクトルの可視化
  -  上位アイテムの取得
  -  重みベクトルの可視化
  -  影響したプロトタイプと関連するアイテムの表示

### **data_preprocessing**
- **`CLMR_Lastfm.ipynb`**  
  Last.fmデータセットの前処理を行うノートブックです。以下の処理が可能です：  
  1. **Spotify API を用いた音源ファイルの取得**  
     - データセット内の楽曲に対応する音源ファイルをSpotifyから取得します。
  2. **音源ファイルパスの保存**  
     - 取得した音源ファイルのパスをデータセットに保存します。
  3. **CLMR（Contrastive Learning of Musical Representations）による音源特徴量の抽出**  
     - 音源ファイルから特徴量を抽出し、データセットに統合します。
  4. **大規模データ対応**  
     - データセットが非常に大きいため、途中結果を逐次保存できる仕組みを実装しています。

---

## 🚀 使用方法

### 環境の準備


<details><summary>package</summary><div>

```
ーーーーーーーーーー
requirements
ProtoMF_github.ipynbに従ってインストールしてください
```bash
!pip install accelerate==0.34.2 \
            arviz==0.19 \
            autograd==1.7.0 \
            bigframes==1.18.0 \
            dask==2024.8.0 \
            distributed==2024.8.0 \
            duckdb==1.1.0 \
            earthengine-api==1.0.0 \
            flax==0.8.5 \
            gdown==5.2.0 \
            geemap==0.34.3 \
            geopandas==1.0.1 \
            google-cloud-aiplatform==1.67.1 \
            google-cloud-bigquery-storage==2.26.0 \
            holidays==0.57 \
            huggingface-hub==0.24.7 \
            ibis-framework==9.2.0 \
            jax==0.4.33 \
            jaxlib==0.4.33 \
            kagglehub==0.3.0 \
            lightgbm==4.5.0 \
            matplotlib-venn==1.1.1 \
            mizani==0.11.4 \
            Pillow==10.4.0 \
            plotly==5.24.1 \
            plotnine==0.13.6 \
            polars==1.6.0 \
            progressbar2==4.5.0 \
            PyDrive2==1.20.0 \
            pymc==5.16.2 \
            pytensor==2.25.4 \
            scikit-image==0.24.0 \
            scikit-learn==1.5.2 \
            torch==2.4.1 \
            torchaudio==2.4.1 \
            torchvision==0.19.1 \
            transformers==4.44.2 \
            urllib3==2.2.3 \
            xarray==2024.9.0
```
wandb 0.19.4
ray 2.41.0
2025/2/19時点での最新バージョンを使用しています．
ーーーーーーーーーーー
 
```

</div></details>

### 音源特徴量を含む音楽推薦モデルの実行
1. `main`フォルダに移動します。
2. `ProtoMF_github.ipynb` を開き、セルを順に実行します。
3. データセットと音源特徴量を利用した音楽推薦システムを構築できます。

### データセットの前処理と音源特徴量の抽出
1. `data_preprocessing`フォルダに移動します。
2. `CLMR_Lastfm.ipynb` を開き、セルを順に実行します。
   - Spotify APIの認証情報が必要です。APIキーを取得し、ノートブック内に設定してください。
3. 前処理結果は逐次保存されるため、処理が中断しても再開可能です。

---

# Note
データセットリンク
> https://drive.google.com/drive/folders/1OpHFcvizYaG1ELiK2ynrTaIy6_n8tOfS?usp=share_link

## ⚠️ 注意事項
- **Spotify API** の使用には認証情報が必要です。APIキーの取得方法は[Spotify for Developers](https://developer.spotify.com/)を参照してください。
- データセットサイズが非常に大きいため、処理には時間とディスク容量が必要です。

# Author

<!--作成情報を列挙-->
* 岡畑　優佑
* 同志社大学 理工学部 インテリジェント情報工学科 知的システムデザイン研究室
* okahata.yusuke@mikilab.doshishs.ac.jp

