def return_user_home(user_data):
    name = user_data['name']
    slack_id = user_data['slack_id']
    coding_time = user_data['coding_time']
    email_address = user_data['email_address']
    api_key = user_data['api_key']
    roblox_user = user_data['roblox_user']
    bobux_balance = user_data['bobux_balance']
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
                    "value": "click_me_123",
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