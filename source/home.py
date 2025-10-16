def return_user_home(user_data):
    name = user_data['name']
    slack_id = user_data['slack_id']
    coding_time = user_data['coding_time']
    email_address = user_data['email_address']
    api_key = user_data['api_key']
    roblox_user = user_data['roblox_user']
    bobux_balance = user_data['bobux_balance']
    if not api_key:
        api_key = "xxxxxxxx"
    home = {
        "type": "home",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Hackaverse Home",
                    "emoji": True
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Name*: {name}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Bobux Balance*: {bobux_balance}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Slack ID*: {slack_id}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Hours coded in Hackaverse*: {coding_time}"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Email*: {email_address}"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Edit",
                        "emoji": True
                    },
                    "value": user_data["slack_id"],
                    "action_id": "edit_email"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "Used for issuing grants and contacting you if we run into issues reviewing your projects!"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Hackatime API Key*: {api_key[0:8]}-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Edit",
                        "emoji": True
                    },
                    "value": "click_me_123",
                    "action_id": "edit_api_key"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "User for tracking time you've spent making games on Hackaverse!"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Roblox Username*:  {roblox_user}"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Remove",
                        "emoji": True
                    },
                    "value": "click_me_123",
                    "action_id": "remove_roblox_account"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "Roblox account associated with your Slack ID!"
                    }
                ]
            },
            {
                "type": "divider"
            }
        ]
    }
    if not roblox_user:
        home["blocks"].pop(11)
        home["blocks"].pop(11)
    return home

def unknown_user():
    return {
	"type": "home",
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Hackaverse Home",
				"emoji": True
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Uh oh it looks like you're not part of the hackaverse :( \n <https://www.roblox.com/games/121862977119677/Hackaverse-Onboarding | Join the hackaverse today>"
			}
		},
		{
			"type": "divider"
		}
	]
}


def edit_email():
    return {
        "type": "modal",
        "callback_id": "edit_email_submit",
        "title": {"type": "plain_text", "text": "Hackaverse"},
        "submit": {"type": "plain_text", "text": "Submit"},
        "close": {"type": "plain_text", "text": "Cancel"},
        "blocks": [
            {"type": "divider"},
            {
                "type": "input",
                "block_id": "email_block",
                "label": {"type": "plain_text", "text": "Edit Email Address"},
                "element": {
                    "type": "plain_text_input",
                    "action_id": "email_input"
                }
            }
        ]
    }

def edit_api_key():
    return {
        "type": "modal",
        "callback_id": "edit_key_submit",
        "title": {"type": "plain_text", "text": "Hackaverse"},
        "submit": {"type": "plain_text", "text": "Submit"},
        "close": {"type": "plain_text", "text": "Cancel"},
        "blocks": [
            {"type": "divider"},
            {
                "type": "input",
                "block_id": "key_block",
                "label": {"type": "plain_text", "text": "Edit Hackatime API Key"},
                "element": {
                    "type": "plain_text_input",
                    "action_id": "key_input"
                }
            }
        ]
    }

