from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import base64
import ollama

app = FastAPI()

class ImageData(BaseModel):
    raspiId: str
    file: str
    # time: int
    time: str
    error_code: int

def ollma_image_process(data: ImageData):
    try:
        # Base64エンコードされた画像をデコード
        image_bytes = base64.b64decode(data.file)
        file_name = f"{data.raspiId}_{data.time}.jpg"
        file_path = "./images/" + file_name
        
        # 画像を保存
        with open(file_path, "wb") as f:
            f.write(image_bytes)

        # プロンプト
        # prompt = f"この画像には何が映っていますか？"
        prompt = f"This is picture of desk. Can you represent how messy the desk is by number?"

        # LLaVAに問い合わせ
        response = ollama.chat(
            model="llava:13b",
            messages=[
                {"role": "system", "content": prompt, "images": [file_path]},
            ]
        )

        # 結果を出力
        print("LLaVAの回答:")
        print(response["message"]["content"])

        with open('file.txt', 'w', encoding='utf-8') as f:
            f.write(response["message"]["content"])

        
        return True


    except Exception as e:
        raise False


@app.get("/hello")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/upload")
async def upload_image(data: ImageData, background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(ollma_image_process, data)
        
        return {"message": "Image processed successfully", "raspiId": data.raspiId, "timestamp": data.time}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
