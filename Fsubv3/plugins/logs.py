from os import remove
from os.path import exists
from Fsubv3 import Bot
from pyrogram import filters, types
from Fsubv3.config import LOGGER, ADMINS

@Bot.on_message(filters.command("log") & filters.user(ADMINS))
async def logs(_, m: types.Message):
    logs_path = "logs.txt"
    if exists(logs_path):
        try:
            await m.reply_document(
                logs_path,
                quote=True,
            )
        except Exception as e:
            remove(logs_path)
            LOGGER(__name__).warning(e)
    elif not exists(logs_path):
        await m.reply_text("Tidak ada logs yang ditemukan!")
