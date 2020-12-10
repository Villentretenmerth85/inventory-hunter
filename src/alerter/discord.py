import logging
import requests
import traceback

from alerter.common import Alerter, AlerterFactory


@AlerterFactory.register
class DiscordAlerter(Alerter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.webhook_url = kwargs.get('webhook_url')

    @classmethod
    def from_args(cls, args):
        webhook_url = args.webhook_url
        return cls(webhook_url=webhook_url)

    @classmethod
    def from_config(cls, config):
        webhook_url = config['webhook_url']
        return cls(webhook_url=webhook_url)

    @staticmethod
    def get_alerter_type():
        return 'discord'

    def __call__(self, **kwargs):
        _discord_embed_generated = {
            "content": None,
            "embeds": [
                {"title": "Alert", "description": kwargs.get("content"), "color": 5832569}
            ],
            "username": "Inventory Hunter",
            "avatar_url": "https://i.imgur.com/X1o5j0N.jpeg",
        }
        try:
            logging.debug(f"Discord Webhook URL: {self.webhook_url}")
            send_request = requests.post(
                self.webhook_url,
                json=_discord_embed_generated,
            )
            if send_request.status_code != 204:
                logging.error(
                    f"There was an issue sending to discord due to an invalid status code back -> {send_request.status_code}"
                )
        except Exception:
            logging.error(
                f"Issue with sending webhook to discord. {traceback.format_exc()}"
            )
