from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
import requests
import json
import os

app = FastAPI()

# 비밀번호 목록 불러오기 (예: {"Rendezvous": "abc123", "ProjectY": "xyz789"})
with open("passwords.json", "r", encoding="utf-8") as f:
    PASSWORDS = json.load(f)

@app.get("/image/{viewer_name}/{image_id}")
async def proxy_image(viewer_name: str, image_id: str, request: Request):
    input_password = request.query_params.get("pw", "")

    # 비밀번호 체크
    if viewer_name not in PASSWORDS or PASSWORDS[viewer_name] != input_password:
        raise HTTPException(status_code=403, detail="Invalid password")

    # 이미지 가져오기
    google_url = f"https://drive.google.com/uc?export=download&id={image_id}"
    res = requests.get(google_url, stream=True)

    if res.status_code != 200:
        raise HTTPException(status_code=404, detail="Image not found")

    return StreamingResponse(res.raw, media_type="image/jpeg")
