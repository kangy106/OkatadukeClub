import cv2
import datetime
import requests
import base64
import json


#server URLが決まったら書き換える
raspyId = "user1"
server_url = "http://163.221.29.44:8000/upload"

def take_photo():
    # カメラを初期化
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("カメラを開けませんでした")
        return

    # 画像を取得
    ret, frame = cap.read()

    if ret:
        # 現在の日時を取得してファイル名に使用
        now = datetime.datetime.now()
        filename = now.strftime("%Y%m%d_%H%M%S") + ".jpg"

        # 画像を保存
        cv2.imwrite(filename, frame)
        print(f"写真を保存しました: {filename}")

        cap.release()

        return filename
    else:
        print("画像の取得に失敗しました")
        cap.release()

        return None

def send_content(filename):
    timestamp = str(datetime.datetime.now().timestamp())
    if filename:
        with open(filename, "rb") as filename:
            encoded_string = base64.b64encode(filename.read()).decode("utf-8")
        payload = {"raspiId": raspyId, "file": encoded_string, "time": timestamp, "error_code": 200}

    else:
        payload = {"raspiId": raspyId, "file": None, "time": timestamp, "error_code": 500}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(server_url, json=payload ,headers=headers, timeout=600)
    print(response.text)
    print("Response:", response.status_code)


if __name__ == "__main__":
    filename = take_photo()
    send_content(filename)