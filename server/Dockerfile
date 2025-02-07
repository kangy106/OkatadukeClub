# 基本イメージ（Ubuntu 22.04 ベースの公式 Ollama イメージを使用）
FROM ollama/ollama:latest

# 作業ディレクトリを作成
WORKDIR /app

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    unzip \
    git \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Python ライブラリをインストール（必要に応じて追加）
RUN pip install --no-cache-dir requests numpy pillow

# LLaVA モデルをダウンロード
RUN ollama pull llava

# ポートを公開（Ollama の API 用）
EXPOSE 11434

# コンテナ起動時に Ollama サーバーを開始
CMD ["ollama", "serve"]