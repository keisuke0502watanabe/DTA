# DTA (Differential Thermal Analysis) Measurement System

## 概要
このプロジェクトは、DTA（示差熱分析）測定システムの制御とデータ収集を行うためのプログラム群です。温度制御、データ収集、Google Spreadsheetへのデータ転送などの機能を提供します。

## 主要コンポーネント

### 温度制御
- `Chino.py`: 温度制御ユニット（Chino）との通信を管理
- `setScanrate.py`: 温度スキャンレートの設定

### 測定機器制御
- `Keigetpv.py`: Keisuke 2000と2182Aの測定値取得
- `setSerKei.py`: 測定機器のシリアル通信設定

### メインプログラム
- `Q1Yes.py`: メインの測定プログラム
- `DTAmain.py`: DTA測定のメイン制御

### データ処理
- `vttotemp.py`: 電圧から温度への変換
- `am.py`: 環境温度の測定
- `import_data_to_sqlite.py`: データベースへのデータインポート

## 必要なハードウェア
- Chino温度制御ユニット
- Keisuke 2000
- Keisuke 2182A
- Raspberry Pi（制御用）

## 必要なソフトウェア
- Python 3.x
- 必要なPythonパッケージ:
  - gspread
  - oauth2client
  - requests
  - natsort

## セットアップ
1. 必要なPythonパッケージのインストール:
```bash
pip install gspread oauth2client requests natsort
```

2. Google Cloud認証情報の設定:
   - Google Cloud Consoleでプロジェクトを作成
   - サービスアカウントを作成し、認証情報をダウンロード
   - 認証情報ファイルを適切な場所に配置

## 使用方法
1. 測定条件の設定:
   - 温度範囲
   - スキャンレート
   - 待機時間

2. 測定の実行:
```bash
python Q1Yes.py
```

3. データの確認:
   - ローカルのCSVファイル
   - Google Spreadsheet

## 注意事項
- 機密情報（認証情報など）は.gitignoreに記載されているファイルに保存
- 測定前に機器の接続状態を確認
- 温度制御の設定値を慎重に確認

## ライセンス
このプロジェクトは非公開です。無断での使用・複製を禁じます。
