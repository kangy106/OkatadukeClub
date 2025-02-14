import json
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# .env の読み込み
load_dotenv()
SLACK_TOKEN = os.getenv("SLACK_TOKEN")

# 🔹 Slack チャンネル ID
CHANNEL = "C08CW80V7AB"

def load_ip_to_name(filename="ip_to_name.json"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("エラー: IPアドレスの対応表が見つかりません。")
        return {}

def send_slack_message(ip_address: str, score: int, image_path: str):
    ip_to_name = load_ip_to_name()
    name = ip_to_name.get(ip_address, "不明なユーザー")
    message_text = f"{name} の机の汚さは {score} 点です。📢"

    client = WebClient(token=SLACK_TOKEN)

    try:
        client.chat_postMessage(channel=CHANNEL, text=message_text)
        with open(image_path, "rb") as file:
            client.files_upload_v2(
                channel=CHANNEL,
                file=file,
                title="机の状態",
                initial_comment="📸 机の状態の画像を送ります！"
            )
        print("メッセージと画像を送信しました！")
    except SlackApiError as e:
        print(f"エラー発生: {e.response['error']}")

if __name__ == "__main__":
    send_slack_message("192.168.1.100", 80, "test.png")
