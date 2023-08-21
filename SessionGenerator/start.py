from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from config import OWNER_ID


def filter(cmd: str):
    return filters.private & filters.incoming & filters.command(cmd)

@Client.on_message(filter("start"))
async def start(bot: Client, msg: Message):
    me2 = (await bot.get_me()).mention
    await bot.send_message(
        chat_id=msg.chat.id,
        text=f"""Halo Mek {msg.from_user.mention},

Ini Bot {me2},
Bot buat bantu lu pada ngambil STRING PYROGRAM V2 & TELETHON.

Insyaallah Botnya aman mek ga kedeak, tapi kalo kedeak yah lagi sial lu berarti.

Made by : [Si Arab Polos](tg://user?id={OWNER_ID}) !""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Mulai Buat String", callback_data="generate")
                ],
                [
                    InlineKeyboardButton("Support", url="https://t.me/SiArabGroup"),
                    InlineKeyboardButton("Owner", user_id=OWNER_ID)
                ]
                [
                    InlineKeyboardButton(text="Jasa Store Si Arab", url="https://t.me/JasaSiArab")
                ],
            ]
        ),
        disable_web_page_preview=True,
    )
