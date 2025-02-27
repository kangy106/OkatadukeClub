import ollama
import requests
from PIL import Image
from io import BytesIO
import base64

# 画像のURL（サンプルとして無料画像サイトから取得）
IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/3/3f/JPEG_example_flower.jpg"

# 画像をダウンロード
response = requests.get(IMAGE_URL)
if response.status_code == 200:
    image = Image.open(BytesIO(response.content))
    image.save("downloaded_image.jpg")  # 保存
    print("画像をダウンロードしました: downloaded_image.jpg")
else:
    print("画像のダウンロードに失敗しました")
    exit()

# 画像をBase64エンコード
with open("downloaded_image.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode("utf-8")

# プロンプト
prompt = "この画像には何が映っていますか？"

# LLaVAに問い合わせ
response = ollama.chat(
    model="llava:13b",
    messages=[
        {"role": "system", "content": f"あなたは画像認識のアシスタントです。{prompt}", "images": ["./downloaded_image.jpg"]},
    ]
)

# 結果を出力
print("LLaVAの回答:")
print(response["message"]["content"])
