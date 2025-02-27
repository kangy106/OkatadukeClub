import requests
import base64
from datetime import datetime
import json

def send_image(image_path, raspi_id, server_url):
    # 画像をBase64エンコード
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    # 現在時刻を取得
    current_time = datetime.utcnow().isoformat() + "Z"

    # JSONデータを構築
    data = {
        "raspiId": raspi_id,
        "file": encoded_string,
        "time": current_time,
        "error_code": 200
    }

    # POSTリクエストを送信
    headers = {'Content-Type': 'application/json'}
    response = requests.post(server_url, data=json.dumps(data), headers=headers)

    # レスポンスを処理
    if response.status_code == 200:
        print("画像が正常に送信されました。")
        print("サーバーレスポンス:", response.json())
    else:
        print("エラーが発生しました。ステータスコード:", response.status_code)
        print("エラーメッセージ:", response.text)

# 使用例
if __name__ == "__main__":
    image_path = "/home/okataduke/test/downloaded_image.jpg"  # 実際の画像ファイルのパスに変更してください
    raspi_id = "raspi001"
    server_url = "http://163.221.29.44:8000/upload"  # サーバーのURLに合わせて変更してください

    send_image(image_path, raspi_id, server_url)
