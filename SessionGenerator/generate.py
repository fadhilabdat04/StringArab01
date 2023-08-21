from pyrogram.types import Message
from telethon import TelegramClient
from pyrogram import Client, filters
from asyncio.exceptions import TimeoutError
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)

import config



ask_ques = "**» Please first choose the python library for generating string :**"
buttons_ques = [
    [
        InlineKeyboardButton("Pyrogram V2", callback_data="pyrogram"),
        InlineKeyboardButton("Telethon", callback_data="telethon"),
    ],
    [
        InlineKeyboardButton("Pyrogram Bot", callback_data="pyrogram_bot"),
        InlineKeyboardButton("Telethon Bot", callback_data="telethon_bot"),
    ],
]

gen_button = [
    [
        InlineKeyboardButton(text="Generate Session", callback_data="generate")
    ]
]




@Client.on_message(filters.private & ~filters.forwarded & filters.command(["generate", "gen", "string", "str"]))
async def main(_, msg):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))


async def generate_session(bot: Client, msg: Message, telethon=False, is_bot: bool = False):
    if telethon:
        ty = "Telethon"
    else:
        ty = "Pyrogram"
    if is_bot:
        ty += "Bot"
    await msg.reply(f"» Lagi Mulai Ambil String **{ty}** Ngambil String lu  ...")
    user_id = msg.chat.id
    api_id_msg = await msg.chat.ask("Kirimin **API_ID** Lu Mek Buat Ngambil String.\n\nAtau Klik /skip Buat Make Bot Api String Arab.", filters=filters.text)
    if await cancelled(api_id_msg):
        return
    if api_id_msg.text == "/skip":
        api_id = config.API_ID
        api_hash = config.API_HASH
    else:
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            await api_id_msg.reply("**API_ID** Harus bilangan bulat, Coba lagi untuk menghasilkan.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
            return
        api_hash_msg = await msg.chat.ask("» Masukin **API_HASH** Buat Ngelanjutin Mek", filters=filters.text)
        if await cancelled(api_hash_msg):
            return
        api_hash = api_hash_msg.text
    if not is_bot:
        t = "» Kirimin No **PHONE_NUMBER** dengan kode negara yang ingin Anda hasilkan sesi string. \nContoh : `+6283671768877`'"
    else:
        t = "Kirimin No **BOT_TOKEN** Buat Ngelanjutin Mek.\nContoh : `5432198765:fagrr42F35AEG4_32G`'"
    phone_number_msg = await msg.chat.ask(t, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text
    if not is_bot:
        await msg.reply("» Lagi Ngirim OTP ke Akun Lu Mek...")
    else:
        await msg.reply("» Mencoba masuk melalui Bot Token...")
    if telethon and is_bot:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = Client(name="bot", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)
    else:
        client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()
    try:
        code = None
        if not is_bot:
            if telethon:
                code = await client.send_code_request(phone_number)
            else:
                code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply("» Kombinasi **API_ID** Dan **API_HASH** Lu engga cocok dengan sistem Aplikasi Telegram Mek. \n\nAmbil String Lagi Mek.", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply("» No **PHONE_NUMBER** Bukan No Akun Tele Lu Mek.\n\Ambil String Lagi Mek.", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    try:
        phone_code_msg = None
        if not is_bot:
            phone_code_msg = await msg.chat.ask("» Sekarang kirimin **OTP** yang lu dapetin dari pesan akun telegram.\nJika OTP adalah `52839`, **Kirimkan sebagai celah antara nomor seperti** `5 2 8 3 9`.", filters=filters.text, timeout=600)
            if await cancelled(phone_code_msg):
                return
    except TimeoutError:
        await msg.reply("» Batas waktu 10 menit tercapai.\n\nMulai buat String Lu lagi setelah beberapa saat.", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    if not is_bot:
        phone_code = phone_code_msg.text.replace(" ", "")
        try:
            if telethon:
                await client.sign_in(phone_number, phone_code, password=None)
            else:
                await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        except (PhoneCodeInvalid, PhoneCodeInvalidError):
            await msg.reply("» OTP yang Lu Kasih **salah.**\n\nBikin Lagi Dah Mek.", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (PhoneCodeExpired, PhoneCodeExpiredError):
            await msg.reply("» Kode Otp Lu Udah **EXPIRED.**\n\nBikin lagi dah Mek.", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (SessionPasswordNeeded, SessionPasswordNeededError):
            try:
                two_step_msg = await msg.chat.ask("» Masukin Password **TWO STEP VERIFICATION** Buat Dapetin Stringnya Mek.", filters=filters.text, timeout=300)
            except TimeoutError:
                await msg.reply("» Batas waktu mencapai 5 mnt.\n\nMulai membuat setelah beberapa saat.", reply_markup=InlineKeyboardMarkup(gen_button))
                return
            try:
                password = two_step_msg.text
                if telethon:
                    await client.sign_in(password=password)
                else:
                    await client.check_password(password=password)
                if await cancelled(api_id_msg):
                    return
            except (PasswordHashInvalid, PasswordHashInvalidError):
                await two_step_msg.reply("» Password lu salah Mek.\n\nBikin lagi dah.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
                return
    else:
        if telethon:
            await client.start(bot_token=phone_number)
        else:
            await client.sign_in_bot(phone_number)
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = f"**Nih udah jadi {ty} String Session** \n\n`{string_session}` \n\n**generated by :** @StringRabRobot\n **Note :** Jangan Lu Kasih Ke siapa-siapa meki"
    try:
        if not is_bot:
            await client.send_message("me", text)
        else:
            await bot.send_message(msg.chat.id, text)
    except KeyError:
        pass
    await client.disconnect()
    await bot.send_message(msg.chat.id, "» Udah Jadi nih {} STRING SESSION.\n\nCek Pesan Tersimpan lu dah yang banyak Papnya ! \n\n**Minimal Bilang Makasih Mek ke :** @Dhilnihnge".format("Telethon" if telethon else "Pyrogram"))


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("**» Canceled the ongoing process !**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("**» Successfully restarted the bot !**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/skip" in msg.text:
        return False
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("**» Canceled the ongoing process !**", quote=True)
        return True
    else:
        return False
