import os
from slack_bolt import App
from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode import SocketModeHandler
import home, db

load_dotenv()
slack_api_key = os.getenv("SLACK_API_KEY")
slack_signing_secret = os.getenv("SLACK_SIGNING_SECRET")
socket_id = os.getenv("SOCKET_ID")

def build_app(api_key, signing_secret):
    app = App(token=api_key, signing_secret=signing_secret)


    @app.event("app_home_opened")
    def show_home(client, event):
        user_id = event["user"]
        user_data = db.query_by_slack_id(user_id)
        if user_data is not None:
            client.views_publish(user_id=user_id, view=home.return_user_home(user_data))
            return
    return app

if __name__ == "__main__":
    app = build_app(slack_api_key, slack_signing_secret)
    handler = SocketModeHandler(app, socket_id)
    handler.start()
