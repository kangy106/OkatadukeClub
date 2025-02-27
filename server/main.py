from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import base64
from opeai import OpenAI
from dotenv import load_dotenv
import os
import re

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

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
        prompt = f"This is picture of desk. Can you represent how messy the desk is by number on a scale of 0 to 100? Just give me a number"

        client = OpenAI(
            api_key = OPENAI_API_KEY,
            organization = "org-sUHbkxwO4EfNkTR5gCs7ZLei",
            project = "proj_jVxUUNlUPysqMsLfmWzfRU5V"
        )

        res = client.chat.completions.create(
            model="gpt-4-turbo-2024-04-09",
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
        comment = res.choices[0].message.content
        score_pattern = r'\b\d{2}\b'
        score = int(re.findall(score_pattern, comment))
        if score == []:
            score = 0
        else:
            score = score[0]

        
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