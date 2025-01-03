import sys
from pyrogram import Client
from Fsubv import config

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_id=config.APP_ID,
            api_hash=config.API_HASH,
            plugins={"root": "Fsubv/plugins"},
            bot_token=config.BOT_TOKEN,
            in_memory=True,
        )
        self.LOGGER = config.LOGGER

    async def start(self):
        try:
            await super().start()
            is_bot = await self.get_me()
            self.username = is_bot.username
            self.namebot = is_bot.first_name
            self.LOGGER(__name__).info(
                f"BOT_TOKEN detected!\n"
                f"Username: @{self.username}\n\n"
            )
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            sys.exit()

        for key, channel_id in config.FORCE_SUB_.items():
            try:
                info = await self.get_chat(channel_id)
                link = info.invite_link
                if not link:
                    await self.export_chat_invite_link(channel_id)
                    link = info.invite_link
                setattr(self, f"invitelink{key}", link)
                self.LOGGER(__name__).info(
                    f"FORCE_SUB_{key} Detected!\n"
                    f"Title: {info.title}\n"
                    f"Chat ID: {info.id}\n\n"
                )
            except Exception as e:
                self.LOGGER(__name__).warning(e)
                self.LOGGER(__name__).warning(
                    f"Pastikan @{self.username} "
                    f"menjadi Admin di FORCE_SUB_{key}\n\n"
                )
                sys.exit()

        try:
            db_channel = await self.get_chat(config.CHANNEL_DB)
            self.db_channel = db_channel
            await self.send_message(chat_id=db_channel.id, text="Bot Aktif!\n\n")
            self.LOGGER(__name__).info(
                "CHANNEL_DB Detected!\n"
                f"Title: {db_channel.title}\n"
                f"Chat ID: {db_channel.id}\n\n"
            )
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(
                f"Pastikan @{self.username}\n "
                f"menjadi Admin di CHANNEL_DB\n\n"
            )
            sys.exit()

        self.LOGGER(__name__).info(
            "🔥 Bot Aktif! 🔥\n\n"
        )

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot Berhenti!\n\n")
