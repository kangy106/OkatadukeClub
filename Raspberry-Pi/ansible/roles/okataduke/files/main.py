import cv2
import datetime

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
    else:
        print("画像の取得に失敗しました")
    
    # カメラを解放
    cap.release()

if __name__ == "__main__":
    take_photo()
