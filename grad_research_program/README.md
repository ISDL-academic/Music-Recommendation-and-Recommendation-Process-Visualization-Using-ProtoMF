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
ProtoMF_github.ipynbに従ってインストールしてください


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

