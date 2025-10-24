import os
from datetime import datetime, timedelta, timezone
import uvicorn
import db
from slack_sdk import WebClient
from fastapi import FastAPI, status, Depends, HTTPException, Body, Request
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
bot_token = os.getenv("SLACK_API_KEY")
app = FastAPI()
client = WebClient(token=bot_token)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    db.initialize_database()

async def verify_api_key(request: Request):
    key = request.headers.get("key")
    if key != api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API key")

@app.post("/api/v1/users/signup/{slack_id}/get/verification", dependencies=[Depends(verify_api_key)])
async def get_slack_account(slack_id, payload: dict = Body(...)):
    if not (payload.get("roblox_user") and slack_id):
        return {"response": "Invalid parameters", "ok" : False}
    user = db.query_by_slack_id(slack_id)
    if user is not None and user.get("roblox_user") is not None:
        return {"response": "User already exists", "ok": True}
    else:
        temp_code = db.add_verification_request(payload.get("roblox_user"), slack_id)
        if not temp_code:
            return {"response": "A request has already been sent", "ok": True}
        client.chat_postMessage(
            channel=slack_id,
            text=f"A verification request has been sent by {payload.get('roblox_user')} \nPlease use the following code to verify account ownership, Don't share it with anyone! `{temp_code}`",
        )
        return {"response": "Message sent", "ok": True}

@app.post("/api/v1/users/signup/{slack_id}/verify", dependencies=[Depends(verify_api_key)])
async def verify_slack_account(slack_id, payload: dict = Body(...)):
    data = db.get_verification_data(slack_id)
    req_time = data["request_time"]
    req_time = req_time.replace(tzinfo=timezone.utc)
    if (datetime.now(timezone.utc) - req_time) > timedelta(minutes=30):
        return {"response": "Verification code expired", "ok": True}
    elif payload.get("verification_code") == data["verification_code"]:
        result = client.users_info(user=slack_id)
        user = result.get("user", {})
        profile = user.get("profile", {})
        name = profile.get("display_name") or profile.get("real_name")
        db.add_user(slack_id=slack_id, roblox_user=payload.get("roblox_user"), name=name)
        return {"response": "User verified", "ok": True}
    else:
        return {"response": "Invalid verification code", "ok": True}

@app.get("/api/v1/users/{slack_id}/data", dependencies=[Depends(verify_api_key)])
async def get_data(slack_id):
    return {"response": db.query_by_slack_id(slack_id), "ok": True}

@app.post("/api/v1/users/{slack_id}/balance", dependencies=[Depends(verify_api_key)])
async def get_balance(slack_id, payload: dict = Body(...)):
    db.update_balance(slack_id=slack_id, balance=payload.get("balance"))
    return {"response": "Balance updated", "ok": True}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=45000)