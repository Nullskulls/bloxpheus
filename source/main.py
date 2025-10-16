import os
from slack_bolt import App
from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode import SocketModeHandler
import home, db, validation

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
        else:
            client.views_publish(user_id=user_id, view=home.unknown_user())

    @app.action("edit_email")
    def edit_email(client, body, ack):
        ack()
        client.views_open(
            trigger_id=body["trigger_id"],
            view=home.edit_email()
        )

    @app.action("edit_api_key")
    def edit_api_key(client, body, ack):
        ack()
        client.views_open(
            trigger_id=body["trigger_id"],
            view=home.edit_api_key()
        )

    @app.view("edit_email_submit")
    def edit_email_submit(client, body, ack):
        ack()
        user_id = body["user"]["id"]
        email = body["view"]["state"]["values"]["email_block"]["email_input"]["value"]
        if not validation.valid_email_address(email):
            ack(response_action="errors", errors={"email_block": "Entering an invalid email address could result in prizes being lost."})
            return
        db.update_email(user_id, email)
        user_data = db.query_by_slack_id(user_id)
        client.views_publish(user_id=user_id, view=home.return_user_home(user_data))

    @app.view("edit_key_submit")
    def edit_api_key_submit(client, body, ack):
        ack()
        user_id = body["user"]["id"]
        api_key = body["view"]["state"]["values"]["key_block"]["key_input"]["value"]
        if not validation.valid_api_key(api_key):
            ack(response_action="errors", errors={"key_block": "Entering an invalid API Key may lead to hours not being counted"})
            return
        db.update_api_key(user_id, api_key)
        user_data = db.query_by_slack_id(user_id)
        client.views_publish(user_id=user_id, view=home.return_user_home(user_data))


    return app

if __name__ == "__main__":
    app = build_app(slack_api_key, slack_signing_secret)
    handler = SocketModeHandler(app, socket_id)
    handler.start()
