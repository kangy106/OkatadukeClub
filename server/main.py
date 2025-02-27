from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import base64
from opeai import OpenAI

app = FastAPI()

class ImageData(BaseModel):
    raspiId: str
    file: str
    # time: int
    time: str
    error_code: int

def openai_image_process(data: ImageData):
    try:

        # プロンプト
        # prompt = f"この画像には何が映っていますか？"
        prompt = f"This is picture of desk. Can you represent how messy the desk is by number?"

        client = OpenAI(
            api_key = "api-key"
        )

        res = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a person who judge the messiness of desks."},
                {"role": "user", "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url":{
                          "url": f"data:image/jpeg;base64,{data.file}",
                      },
                    }
                ]}
            ],
            reponse_format ={"type": "json"}
        )

        # 結果を出力
        print("GPTの回答:")
        print(res.choices[0].message.content)

        
        return True


    except Exception as e:
        raise False


@app.get("/hello")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/upload")
async def upload_image(data: ImageData, background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(openai_image_process, data)
        
        return {"message": "Image processed successfully", "raspiId": data.raspiId, "timestamp": data.time}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)