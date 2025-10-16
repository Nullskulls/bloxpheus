import os, datetime
import db
from slack_sdk import WebClient
from fastapi import FastAPI, status, Depends, HTTPException, Request
from dotenv import load_dotenv

from source.db import query_by_slack_id

load_dotenv()
api_key = os.getenv("API_KEY")
bot_token = os.getenv("SLACK_API_KEY")
app = FastAPI()
client = WebClient(token=bot_token)

async def verify_api_key(request):
    key = request.headers.get("key")
    if key != api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@app.post("/api/v1/users/signup/{slack_id}/get/verification")
async def get_slack_account(slack_id, request: Request):
    user = query_by_slack_id(slack_id)
    if user and user.get("roblox_user"):
        return {"response": "User already exists", "ok": True}
    else:
        body = await request.body()
        temp_code = db.add_verification_request(body.get("roblox_user"), slack_id)
        if not temp_code:
            return {"response": "A request has already been sent", "ok": True}
        client.chat_postMessage(
            channel=slack_id,
            text=f"A verification request has been sent by {user.get('roblox_user')} \nPlease use the following code to verify account ownership, Don't share it with anyone! `{temp_code}`",
        )
        return {"response": "Message sent", "ok": True}

@app.post("/api/v1/users/signup/{slack_id}/verify")
async def verify_slack_account(slack_id, request: Request):
    data = db.get_verification_data(slack_id)
    body = await request.body()
    if (datetime.now < data["request_time"]) > datetime.timedelta(minutes=30):
        return {"response": "Verification code expired", "ok": True}
    elif body.get("verification_code") == data["verification_code"]:
        result = client.users_info(user=slack_id)
        user = result.get("user", {})
        profile = user.get("profile", {})
        name = profile.get("display_name") or profile.get("real_name")
        db.add_user(slack_id=slack_id, roblox_user=body.get("roblox_user", name=name))
        return {"response": "User verified", "ok": True}
    else:
        return {"response": "Invalid verification code", "ok": True}

@app.get("/api/v1/users/{slack_id}/data")
async def get_data(slack_id):
    return {"response": db.query_by_slack_id(slack_id), "ok": True}

@app.post("/api/v1/users/{slack_id}/balance")
async def get_balance(slack_id, request: Request):
    body = await request.body()
    db.update_balance(slack_id=slack_id, balance=body.get("balance"))
    return {"response": "Balance updated", "ok": True}