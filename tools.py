
# ------------------------- #
# Don't Remove Credit
# Owner @Mr_Mohammed_29
# ------------------------- #

from pyrogram import Client, filters, StopPropagation
from pyrogram.enums import ParseMode
from gtts import gTTS
from urllib.parse import quote
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery 
from config import WEATHER_API, OWNER_ID 
from database import users, db

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

MAINTENANCE = {
    "enabled": False,
    "reason": "No reason provided"
}

# ==============================
# ADMIN VARIABLES
# ==============================

BOT_START = datetime.now()

CACHE = {}

FEEDBACK_IMAGE = "https://graph.org/file/ac5e24a6243bfbbbecca2-7210d817a7005a0f56.jpg"
DB_IMAGE = "https://graph.org/file/faf795187aa693e1024a4-746b376c8dcc889d4f.jpg"
CACHE_IMAGE = "https://graph.org/file/a49a09e10235fc020e604-289b1b02951a23f44b.jpg"

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

import os
import qrcode
import requests
import pytz
import imageio
import psutil
import shutil

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

WEATHER_CACHE = {}
QR_CACHE = {}
LAST_CACHE_CLEAR = "Never"

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

def register_tools(bot):

    # ---------------- TTS ----------------- #
    @bot.on_message(filters.command("tts"))
    async def tts(_, message):
        if len(message.command) < 2:
            return await message.reply_text(
                "Usage:\n/tts ʏᴏᴜʀ ᴛᴇxᴛ"
            )
        text = message.text.split(None, 1)[1]
        wait = await message.reply_text(
            "🎙 <b>Gᴇɴᴇʀᴀᴛɪɴɢ Vᴏɪᴄᴇ...</b>\n"
            "⏳ Pʟᴇᴀsᴇ ᴡᴀɪᴛ ᴀ sᴇᴄ...",
            parse_mode=ParseMode.HTML
        )
        try:
            file = f"tts_{message.from_user.id}.mp3"
            tts = gTTS(
                text=text,
                lang="en",
                slow=False
            )
            tts.save(file)
            await wait.delete()
            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "• ᴅᴇᴠᴇʟᴏᴘᴇʀ •",
                            url="https://t.me/Mr_Mohammed_29"
                        ),
                        InlineKeyboardButton(
                            "• ᴄʟᴏsᴇ •",
                            callback_data="close"
                        )
                    ]
                ]
            )
            await message.reply_audio(
                audio=file,
                title="Tᴇxᴛ Tᴏ Sᴘᴇᴇᴄʜ",
                performer="ʙʏ @Aero_Unity",
                caption=(
                    f"🎙 <b>Tᴇxᴛ Tᴏ Sᴘᴇᴇᴄʜ</b>\n\n"
                    f"<code>{text}</code>"
                ),
                parse_mode=ParseMode.HTML,
                reply_markup=buttons
            )
            os.remove(file)
        except Exception as e:
            try:
                await wait.edit_text(
                    f"❌ Error:\n{e}"
                )
            except:
                pass

    # ---------------- QR CODE ---------------- #
    @bot.on_message(filters.command("qrcode"))
    async def qrcode_cmd(_, message):
        if len(message.command) < 2:
            return await message.reply_text(
                "Usage:\n/qrcode ʏᴏᴜʀ ᴛᴇxᴛ ᴏʀ ʟɪɴᴋ"
            )
        text = message.text.split(None, 1)[1]
        QR_CACHE[message.from_user.id] = text
        wait = await message.reply_text(
            "📱 <b>Gᴇɴᴇʀᴀᴛɪɴɢ Qʀ Cᴏᴅᴇ...</b>\n"
            "⏳ Pʟᴇᴀsᴇ ᴡᴀɪᴛ ᴀ sᴇᴄ...",
            parse_mode=ParseMode.HTML
        )
        try:
            qr = qrcode.QRCode(
               version=1,
               error_correction=qrcode.constants.ERROR_CORRECT_H,
               box_size=10,
               border=4
            )
            qr.add_data(text)
            qr.make(fit=True)
            
            img = qr.make_image(
                fill_color="black",
                back_color="white"
            )
            file = f"qrcode_{message.from_user.id}.png"
            img.save(file)
            
            await wait.delete()
            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "• ɴᴇᴡ ǫʀ ᴄᴏᴅᴇ •",
                            callback_data="new_qr"
                        ),
                        InlineKeyboardButton(
                            "• ᴄʟᴏsᴇ •",
                            callback_data="close"
                        )
                    ]
                ]
            )
            await message.reply_photo(
                photo=file,
                caption=(
                    "📱 <b>Qʀ Cᴏᴅᴇ Gᴇɴᴇʀᴀᴛᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ</b>\n"
                    " ʙʏ @Aero_Unity\n\n"
                    f"<code>{text}</code>"
                ),
                parse_mode=ParseMode.HTML,
                reply_markup=buttons
            )

            os.remove(file)

        except Exception as e:

            await wait.edit_text(
                f"❌ Error:\n{e}"
            )

    # ---------------- NEW QR ---------------- #
    @bot.on_callback_query(filters.regex("^new_qr$"))
    async def new_qr(_, query):

        user_id = query.from_user.id

        text = QR_CACHE.get(user_id)
        
        if not text:
            return await query.answer(
                "Nᴏ ᴘʀᴇᴄɪᴏᴜs ǫʀ ᴄᴏᴅᴇ ғᴏᴜɴᴅ.",
                show_alert=True
            )
        await query.answer()

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4
        )
        
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(
            fill_color="black",
            back_color="white"
        )
        file = f"qrcode_{user_id}.png"
        img.save(file)
        
        await query.message.reply_photo(
            photo=file,
            caption=(
                "📱 <b>Qʀ Cᴏᴅᴇ Gᴇɴᴇʀᴀᴛᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ</b>\n"
                " ʙʏ @Aero_Unity\n\n"
                f"<code>{text}</code>"
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "• ɴᴇᴡ ǫʀ ᴄᴏᴅᴇ •",
                            callback_data="new_qr"
                        ),
                        InlineKeyboardButton(
                            "• ᴄʟᴏsᴇ •",
                            callback_data="close"
                        )
                    ]
                ]
            )
        )
        os.remove(file)

    # ---------------- DATETIME ---------------- #
    @bot.on_message(filters.command("datetime"))
    async def datetime_cmd(_, message):

        wait = await message.reply_text(
            "🕒 <b>Gᴇᴛᴛɪɴɢ Cᴜʀʀᴇɴᴛ Dᴀᴛᴇ & Tɪᴍᴇ...</b>\n"
            "⏳ Pʟᴇᴀsᴇ ᴡᴀɪᴛ ᴀ sᴇᴄ..",
            parse_mode=ParseMode.HTML
        )
        try:
            zones = {
                "🇬🇧 UTC": "UTC",
                "🇮🇳 IST": "Asia/Kolkata",
                "🇦🇪 GST": "Asia/Dubai",
                "🇸🇬 SGT": "Asia/Singapore",
                "🇯🇵 JST": "Asia/Tokyo",
                "🇺🇸 EST": "America/New_York",
                "🇺🇸 PST": "America/Los_Angeles",
                "🇪🇺 CET": "Europe/Paris",
                "🇷🇺 MSK": "Europe/Moscow",
                "🇦🇺 AEST": "Australia/Sydney"
            }
            text = "🕐 <b>Cᴜʀʀᴇɴᴛ Dᴀᴛᴇ & Tɪᴍᴇ</b>\n\n"
            for name, zone in zones.items():

                tz = pytz.timezone(zone)
                now = datetime.now(tz)

                offset = now.strftime("%z")

                if offset:
                    hrs = int(offset[:3])
                    mins = int(offset[3:]) // 60

                    if mins == 0:
                        utc = f"UTC{hrs:+d}"
                    else:
                        utc = f"UTC{hrs:+d}.{mins}"
                else:
                    utc = "UTC"

                text += (
                    f"» {name}: "
                    f"<code>{now.strftime('%d/%m/%Y %H:%M')}</code> "
                    f"{utc}\n"
                )

            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "• ʀᴇғʀᴇsʜ •",
                            callback_data="refresh_datetime"
                        ),
                        InlineKeyboardButton(
                            "• ᴄʟᴏsᴇ •",
                            callback_data="close"
                        )
                    ]
                ]
            )

            await wait.delete()

            await message.reply_text(
                text,
                parse_mode=ParseMode.HTML,
                reply_markup=buttons
            )
        except Exception as e:

            await wait.edit_text(
                f"❌ Error:\n{e}"
            )

    # ---------------- REFRESH DATETIME ---------------- #
    @bot.on_callback_query(filters.regex("^refresh_datetime$"))
    async def refresh_datetime(_, query):

        await query.answer()
        zones = {
            "🇬🇧 UTC": "UTC",
            "🇮🇳 IST": "Asia/Kolkata",
            "🇦🇪 GST": "Asia/Dubai",
            "🇸🇬 SGT": "Asia/Singapore",
            "🇯🇵 JST": "Asia/Tokyo",
            "🇺🇸 EST": "America/New_York",
            "🇺🇸 PST": "America/Los_Angeles",
            "🇪🇺 CET": "Europe/Paris",
            "🇷🇺 MSK": "Europe/Moscow",
            "🇦🇺 AEST": "Australia/Sydney"
        }
        text = "🕐 <b>Cᴜʀʀᴇɴᴛ Dᴀᴛᴇ & Tɪᴍᴇ</b>\n\n"

        for name, zone in zones.items():

            tz = pytz.timezone(zone)
            now = datetime.now(tz)

            offset = now.strftime("%z")

            if offset:
                hrs = int(offset[:3])
                mins = int(offset[3:]) // 60

                if mins == 0:
                    utc = f"UTC{hrs:+d}"
                else:
                    utc = f"UTC{hrs:+d}.{mins}"
            else:
                utc = "UTC"

            text += (
                f"» {name}: "
                f"<code>{now.strftime('%d/%m/%Y %H:%M')}</code> "
                f"{utc}\n"
            )

        try:
            await query.message.edit_text(
                text,
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "• ʀᴇғʀᴇsʜ •",
                                callback_data="refresh_datetime"
                            ),
                            InlineKeyboardButton(
                                "• ᴄʟᴏsᴇ •",
                                callback_data="close"
                            )
                        ]
                    ]
                )
            )
        except Exception:
            pass
        
    # ---------------- TEXT TO GIF ---------------- #
    @bot.on_message(filters.command("text2gif"))
    async def text2gif(_, message):

        if len(message.command) < 2:
            return await message.reply_text(
                "Usage:\n/text2gif ʏᴏᴜʀ ᴛᴇxᴛ"
            )
        text = message.text.split(None, 1)[1]
        wait = await message.reply_text(
            "🎞 <b>Gᴇɴᴇʀᴀᴛɪɴɢ Gɪғ...</b>\n"
            "⏳ Pʟᴇᴀsᴇ ᴡᴀɪᴛ ᴀ sᴇᴄ...",
            parse_mode=ParseMode.HTML
        )
        try:
            frames = []

            for i in range(15):

                img = Image.new(
                    "RGB",
                    (800, 300),
                    (25, 25, 25)
                )

                draw = ImageDraw.Draw(img)

                try:
                    font = ImageFont.truetype(
                        "arial.ttf",
                        45
                    )
                except:
                    font = ImageFont.load_default()

                x = 30 + (i * 15)

                draw.text(
                    (x, 120),
                    text,
                    fill=(255, 255, 255),
                    font=font
                )

                frames.append(img)

            gif_file = f"textgif_{message.from_user.id}.gif"

            imageio.mimsave(
                gif_file,
                frames,
                duration=0.10
            )
            await wait.delete()

            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "• ᴜᴘᴅᴀᴛᴇs •",
                            url="https://t.me/Aero_Unity"
                        ),
                        InlineKeyboardButton(
                            "• ᴄʟᴏsᴇ •",
                            callback_data="close"
                        )
                    ]
                ]
            )
            await message.reply_animation(
                animation=gif_file,
                caption=(
                    "🎞 <b>Tᴇxᴛ Tᴏ Gɪғ</b>\n\n"
                    f"<code>{text}</code>"
                ),
                parse_mode=ParseMode.HTML,
                reply_markup=buttons
            )
            os.remove(gif_file)

        except Exception as e:

            await wait.edit_text(
                f"❌ Error:\n{e}"
            )

    # ---------------- WEATHER ---------------- #
    @bot.on_message(filters.command("weather"))
    async def weather_cmd(_, message):

        if len(message.command) < 2:
            return await message.reply_text(
                "Usage:\n/weather ᴄɪᴛʏ ɴᴀᴍᴇ"
            )
        city = message.text.split(None, 1)[1].strip()
        WEATHER_CACHE[message.from_user.id] = city
        wait = await message.reply_text(
            "🌦 <b>Fᴇᴛᴄʜɪɴɢ Wᴇᴀᴛʜᴇʀ...</b>\n"
            "⏳ Pʟᴇᴀsᴇ ᴡᴀɪᴛ ᴀ sᴇᴄ...",
            parse_mode=ParseMode.HTML
        )
        try:
            # -------- GEO SEARCH -------- #

            geo_url = (
                f"http://api.openweathermap.org/geo/1.0/direct"
                f"?q={quote(city)}"
                f"&limit=1"
                f"&appid={WEATHER_API}"
            )

            geo = requests.get(
                geo_url,
                timeout=20
            ).json()

            if not geo:
                return await wait.edit_text(
                    "‼️ ᴄʜᴇᴄᴋ ᴛʜᴇ sᴘᴇʟʟɪɴɢ ᴛʀʏ ᴀɢᴀɪɴ ᴏʀ ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛᴇᴅ ᴄɪᴛʏ ɴᴏᴛ ғᴏᴜɴᴅ"
                )

            place = geo[0]

            lat = place["lat"]
            lon = place["lon"]

            city_name = place["name"]
            state = place.get("state", "")
            country = place["country"]   
      
            # -------- CURRENT WEATHER -------- #
            current_url = (
                f"https://api.openweathermap.org/data/2.5/weather"
                f"?lat={lat}"
                f"&lon={lon}"
                f"&appid={WEATHER_API}"
                f"&units=metric"
            )
            current = requests.get(
                current_url,
                timeout=20
            ).json()
        
            # -------- FORECAST -------- #
            forecast_url = (
                f"https://api.openweathermap.org/data/2.5/forecast"
                f"?lat={lat}"
                f"&lon={lon}"
                f"&appid={WEATHER_API}"
                f"&units=metric"
            )

            forecast = requests.get(
                forecast_url,
                timeout=20
            ).json()

            temp = round(current["main"]["temp"])
            feels = round(current["main"]["feels_like"])

            temp_f = round((temp * 9 / 5) + 32)
            feels_f = round((feels * 9 / 5) + 32)

            condition = current["weather"][0]["main"]

            humidity = current["main"]["humidity"]

            wind = round(current["wind"]["speed"] * 3.6)

            visibility = round(current["visibility"] / 1000)

            pressure = current["main"]["pressure"]

            clouds = current["clouds"]["all"]

            uv = "0"
            uv_text = "Low"

            days = {}

            for item in forecast["list"]:

                day = item["dt_txt"].split()[0]

                if day not in days:

                    days[day] = {
                        "min": item["main"]["temp_min"],
                        "max": item["main"]["temp_max"],
                        "weather": item["weather"][0]["main"]
                    }

                else:

                    days[day]["min"] = min(
                        days[day]["min"],
                        item["main"]["temp_min"]
                    )

                    days[day]["max"] = max(
                        days[day]["max"],
                        item["main"]["temp_max"]
                    )

            forecast_text = ""

            count = 0

            for day, value in days.items():

                if count == 3:
                    break

                name = datetime.strptime(
                    day,
                    "%Y-%m-%d"
                ).strftime("%a")

                forecast_text += (
                    f"» {name}: "
                    f"{round(value['min'])}°C ~ "
                    f"{round(value['max'])}°C "
                    f"({value['weather']})\n"
                )

                count += 1

            text = f"""
 ☀️ <b>ᴡᴇᴀᴛʜᴇʀ ɪɴ {city_name}, {state}, {country}</b>

 🌡️ ᴛᴇᴍᴘᴇʀᴀᴛᴜʀᴇ : <code>{temp}°C / {temp_f}°F</code>
 🤔 ғᴇᴇʟs ʟɪᴋᴇ : <code>{feels}°C / {feels_f}°F</code>
 ☁️ ᴄᴏɴᴅɪᴛɪᴏɴ : <code>{condition}</code>
 💧 ʜᴜᴍɪᴅɪᴛʏ : <code>{humidity}%</code>
 💨 ᴡɪɴᴅ : <code>{wind} km/h</code>
 👁️ ᴠɪsɪʙɪʟɪᴛʏ : <code>{visibility} km</code>
 ☀️ ᴜᴠ ɪɴᴅᴇx : <code>{uv} ({uv_text})</code>
 ☁️ ᴄʟᴏᴜᴅ ᴄᴏᴠᴇʀ : <code>{clouds}%</code>
 📊 ᴘʀᴇssᴜʀᴇ : <code>{pressure} mb</code>

 📅 <b>Fᴏʀᴇᴄᴀsᴛ:</b>
 {forecast_text}
 """

            await wait.delete()

            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "• ʀᴇғʀᴇsʜ •",
                            callback_data="weather_refresh"
                        ),
                        InlineKeyboardButton(
                            "• ᴜᴘᴅᴀᴛᴇs •",
                            url="https://t.me/Aero_Unity"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "• ᴄʟᴏsᴇ •",
                            callback_data="close"
                        )
                    ]
                ]
            )

            await message.reply_text(
                text,
                parse_mode=ParseMode.HTML,
                reply_markup=buttons
            )

        except Exception as e:
            await wait.edit_text(
                f"❌ Error:\n{e}"
            )

    # ---------------- WEATHER REFRESH ---------------- #
    @bot.on_callback_query(filters.regex("^weather_refresh$"))
    async def weather_refresh(_, query):

        await query.answer(
            "Rᴇғʀᴇsʜɪɴɢ..."
        )
        city = WEATHER_CACHE.get(query.from_user.id)

        if not city:
            return await query.answer(
                "ᴡᴇᴀᴛʜᴇʀ ᴇxᴘɪʀᴇᴅ",
                show_alert=True
            )

        class FakeMessage:
            command = ["weather", city]
            text = f"/weather {city}"
            from_user = query.from_user

            async def reply_text(self, *args, **kwargs):
                return await query.message.reply_text(*args, **kwargs)

        await weather_cmd(_, FakeMessage())

    # ---------------- IMAGINE ---------------- #
    @bot.on_message(filters.command("imagine"))
    async def imagine(_, message):

        if len(message.command) < 2:
            return await message.reply_text(
                "Usage:\n/imagine ʏᴏᴜʀ ᴛᴇxᴛ ᴏʀ ᴘʀᴏᴍᴘᴛ"
            )

        prompt = message.text.split(None, 1)[1]

        wait = await message.reply_text(
            "🎨 Gᴇɴᴇʀᴀᴛɪɴɢ Iᴍᴀɢᴇ...\n"
            "Pʟᴇᴀsᴇ Wᴀɪᴛ A Sᴇᴄ..."
        )
        try:
            url = f"https://image.pollinations.ai/prompt/{quote(prompt)}"

            img = requests.get(url, timeout=120)

            if img.status_code != 200:
                return await wait.edit_text(
                    "‼️ Fᴀɪʟᴇᴅ Tᴏ Gᴇɴᴇʀᴀᴛᴇ ɪᴍᴀɢᴇ , ᴛʀʏ ᴀɢᴀɪɴ."
                )

            file = "imagine.png"

            with open(file, "wb") as f:
                f.write(img.content)

            await wait.delete()

            await message.reply_photo(
                photo=file,
                caption=(
                    f"🎨 <b>Iᴍᴀɢᴇ Gᴇɴᴇʀᴀᴛᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ</b>\n"
                    " ʙʏ @Aero_Unity\n\n"
                    f"📝 <code>{prompt}</code>"
                ),
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "• Rᴇɢᴇɴᴇʀᴀᴛᴇ •",
                                callback_data=f"regen_{prompt}"
                            ),
                            InlineKeyboardButton(
                                "• ᴄʟᴏsᴇ •",
                                callback_data="close_imagine"
                            )
                        ]
                    ]
                )
            )
            os.remove(file)

        except Exception as e:
            await wait.edit_text(
                f"❌ Error:\n{e}"
            )

    # ---------------- REGENERATE BUTTON ---------------- #
    @bot.on_callback_query(filters.regex("^regen_"))
    async def regenerate_image(_, query):

        prompt = query.data.replace("regen_", "")

        wait = await query.message.reply_text(
            "🔄 Rᴇɢᴇɴᴇʀᴀᴛɪɴɢ Iᴍᴀɢᴇ...\n"
            "Pʟᴇᴀsᴇ Wᴀɪᴛ..."
        )
        try:
            url = f"https://image.pollinations.ai/prompt/{quote(prompt)}"

            img = requests.get(url, timeout=120)

            if img.status_code != 200:
                return await wait.edit_text(
                    "‼️ Fᴀɪʟᴇᴅ Tᴏ Rᴇɢɴᴇʀᴀᴛᴇ ɪᴍᴀɢᴇ , ᴛʀʏ ᴀɢᴀɪɴ."
                )
            file = "regen.png"

            with open(file, "wb") as f:
                f.write(img.content)

            await wait.delete()

            await query.message.reply_photo(
                photo=file,
                caption=(
                    f"🎨 <b>Iᴍᴀɢᴇ Rᴇɢᴇɴᴇʀᴀᴛᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ</b>\n"
                    "ʙʏ @Aero_Unity\n\n"
                    f"📝 <code>{prompt}</code>"
                ),
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "• Rᴇɢᴇɴᴇʀᴀᴛᴇ •",
                                callback_data=f"regen_{prompt}"
                            ),
                            InlineKeyboardButton(
                                "• ᴄʟᴏsᴇ •",
                                callback_data="close_imagine"
                            )
                        ]
                    ]
                )
            )
            os.remove(file)

        except Exception as e:
            await wait.edit_text(
                f"❌ Error:\n{e}"
            )

    # ---------------- CLOSE BUTTON ---------------- #
    @bot.on_callback_query(filters.regex("^close_imagine$"))
    async def close_imagine(_, query):

        try:
            await query.message.delete()
        except:
            pass

        await query.answer("• ᴄʟᴏsᴇᴅ • ✅️")

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

    # ==========================================
    # FEEDBACK
    # ==========================================

    @bot.on_message(filters.command("feedback") & filters.private)
    async def feedback_cmd(client, message):

        keyboard = InlineKeyboardMarkup(
            [
                 [
                    InlineKeyboardButton(
                        "• Cᴏɴᴛᴀᴄᴛ Oᴡɴᴇʀ •",
                        url="https://t.me/Mr_Mohammed_29"
                    )
                 ],
                 [
                    InlineKeyboardButton(
                        "• ᴄʟᴏsᴇ •",
                        callback_data="close_feedback"
                    )
                 ]
            ]
        )

        await message.reply_photo(
            photo=FEEDBACK_IMAGE,
            caption=(
                "**Aɴʏ Fᴇᴇᴅʙᴀᴄᴋ**\n\n"
                "**- Fᴏᴜɴᴅ A Bᴜɢ?**\n"
                "**- Hᴀᴠᴇ A Sᴜɢɢᴇsᴛɪᴏɴ?**\n"
                "**- Nᴇᴇᴅ ʜᴇʟᴘ?**\n\n"
                "ᴄʟɪᴄᴋ **Contact Owner** Bᴇʟᴏᴡ."
            ),
            reply_markup=keyboard
        )

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

    # ==========================================
    # CLOSE FEEDBACK
    # ==========================================

    @bot.on_callback_query(filters.regex("^close_feedback$"))
    async def close_feedback(client, query):

        await query.answer()

        try:
            await query.message.delete()
        except:
            pass

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

    # ==========================================
    # DATABASE SIZE
    # ==========================================

    @bot.on_message(filters.command("dbsize") & filters.private)
    async def dbsize_cmd(client, message):

        if message.from_user.id != OWNER_ID:
            return await message.reply_text(
                "<b>ʙᴀᴋᴋᴀ ! ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ꜱᴇɴᴘᴀɪ!!</b>",
                quote=True
            )

        try:
            total_users = await users.count_documents({})
  
            renamed_users = await users.count_documents(
                {"rename_count": {"$gt": 0}}
            )

            total_renames = 0

            async for user in users.find({}, {"rename_count": 1}):
                total_renames += user.get("rename_count", 0)

            try:
                stats = await db.command("dbStats")
                db_used = round(stats["dataSize"] / (1024 * 1024), 2)
                collections = stats["collections"]
            except:
                db_used = 0
            collections = 0

            cache_entries = len(CACHE)

            text = (
                "📊 <b>Dᴀᴛᴀʙᴀsᴇ Sᴛᴀᴛɪsᴛɪᴄs</b>\n\n"
                f"👥 <b>Tᴏᴛᴀʟ Usᴇʀs</b> : <code>{total_users}</code>\n"
                f"🎬 <b>Usᴇʀs Rᴇɴᴀᴍᴇᴅ</b> : <code>{renamed_users}</code>\n"
                f"📁 <b>Tᴏᴛᴀʟ Rᴇɴᴀᴍᴇs</b> : <code>{total_renames}</code>\n"
                f"💾 <b>Dᴀᴛᴀʙᴀsᴇ Usᴇᴅ</b> : <code>{db_used:.2f} MB</code>\n"
                f"🗂 <b>Cᴏʟʟᴇᴄᴛɪᴏɴs</b> : <code>{collections}</code>\n"
                f"⚡ <b>Cᴀᴄʜᴇ Eɴᴛʀɪᴇs</b> : <code>{cache_entries}</code>\n"
                f"🕒 <b>Lᴀsᴛ Uᴘᴅᴀᴛᴇᴅ</b> : "
                f"<code>{datetime.now().strftime('%d-%m-%Y %I:%M %p')}</code>"
            )

            keyboard = InlineKeyboardMarkup(
                [
                     [
                        InlineKeyboardButton(
                            "• ᴄʟᴏsᴇ •",
                            callback_data="close_dbsize"
                        )
                     ]
                ]
            )

            await message.reply_photo(
                photo=DB_IMAGE,
                caption=text,
                reply_markup=keyboard
            )

        except Exception as e:
            await message.reply_text(str(e))

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

    # ==========================================
    # CLOSE DBSIZE
    # ==========================================

    @bot.on_callback_query(filters.regex("^close_dbsize$"))
    async def close_dbsize(client, query):

        await query.answer()

        try:
            await query.message.delete()
        except:
            pass
  
# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

    # ==========================================
    # CLEAR CACHE
    # ==========================================

    @bot.on_message(filters.command("clearcache") & filters.private)
    async def clearcache_cmd(client, message):

        if message.from_user.id != OWNER_ID:
            return await message.reply_text(
                "<b>ʙᴀᴋᴋᴀ ! ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ꜱᴇɴᴘᴀɪ!!</b>",
                quote=True
            )

        try:
            global LAST_CACHE_CLEAR

            cache_before = len(CACHE)

            last_clear = LAST_CACHE_CLEAR

            CACHE.clear()

            LAST_CACHE_CLEAR = datetime.now().strftime("%d-%m-%Y %I:%M %p")

            keyboard = InlineKeyboardMarkup(
                [
                     [
                        InlineKeyboardButton(
                            "• ᴄʟᴏsᴇ •",
                            callback_data="close_cache"
                        )
                     ]
                ]
            )

            await message.reply_photo(
                photo=CACHE_IMAGE,
                caption=(
                    "<b>🧹 Cᴀᴄʜᴇ Cʟᴇᴀʀᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ</b>\n\n"
                    f"🗑 <b>Cʟᴇᴀʀᴇᴅ Cᴀᴄʜᴇ</b> : <code>{cache_before}</code>\n"
                    f"⚡ <b>Cᴜʀʀᴇɴᴛ Cᴀᴄʜᴇ</b> : <code>{len(CACHE)}</code>\n"
                    f"🕒 <b>Pʀᴇᴠɪᴏᴜs Cʟᴇᴀʀ</b> : <code>{last_clear}</code>\n"
                    f"✅ <b>Cᴜʀʀᴇɴᴛ Cʟᴇᴀʀ</b> : <code>{LAST_CACHE_CLEAR}</code>"
                ),
                reply_markup=keyboard
            )

        except Exception as e:
            await message.reply_text(f"❌ {e}")
        
# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

    # ==========================================
    # CLOSE CACHE
    # ==========================================

    @bot.on_callback_query(filters.regex("^close_cache$"))
    async def close_cache(client, query):

        await query.answer()

        try:
            await query.message.delete()
        except:
            pass

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

    # ==========================================
    # MAINTENANCE COMMAND
    # ==========================================
 
    @bot.on_message(filters.command("maintenance") & filters.private)
    async def maintenance_cmd(client, message):

        if message.from_user.id != OWNER_ID:
            return await message.reply_text(
                "<b>ʙᴀᴋᴋᴀ ! ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ꜱᴇɴᴘᴀɪ!!</b>"
            )

        if len(message.command) < 2:

            status = "🟢 Eɴᴀʙʟᴇᴅ" if MAINTENANCE["enabled"] else "🔴 Dɪsᴀʙʟᴇᴅ"

            return await message.reply_text(
                f"""<b>Mᴀɪɴᴛᴇɴᴀɴᴄᴇ Pᴀɴɴᴇʟ</b>

    <b>• Sᴛᴀᴛᴜs :</b> {status}
    <b>• Rᴇᴀsᴏɴ :</b> <code>{MAINTENANCE["reason"]}</code>
 
    <b>Usage</b>
    /maintenance on Bot Updating...
    /maintenance off"""
            )

        args = message.text.split(maxsplit=2)
        mode = args[1].lower()

        if mode == "on":

            reason = "No reason provided"

            if len(args) >= 3:
                reason = args[2]

            MAINTENANCE["enabled"] = True
            MAINTENANCE["reason"] = reason

            await message.reply_text(
                f"""✅ <b>Mᴀɪɴᴛᴇɴᴀɴᴄᴇ Eɴᴀʙʟᴇᴅ</b>

    📝 <b>Rᴇᴀsᴏɴ</b> : <code>{reason}</code>"""
            )

        elif mode == "off":

            MAINTENANCE["enabled"] = False
            MAINTENANCE["reason"] = "No reason provided"

            await message.reply_text(
                "✅ <b>Mᴀɪɴᴛᴇɴᴀɴᴄᴇ Dɪsᴀʙʟᴇᴅ</b>"
            )

        else:

            await message.reply_text(
                "Usage:\n"
                "/maintenance on Bot Updating...\n"
                "/maintenance off"
            )


    # ==========================================
    # BLOCK USERS DURING MAINTENANCE
    # ==========================================

    @bot.on_message(filters.private, group=-100)
    async def maintenance_checker(client, message):

        if message.from_user.id == OWNER_ID:
            return

        if not MAINTENANCE["enabled"]:
            return

        await message.reply_text(
            f"""<b>Bᴏᴛ Uɴᴅᴇʀ Mᴀɪɴᴛᴇɴᴀɴᴄᴇ</b>

    • Bᴏᴛ Is Uᴘᴅᴀᴛɪɴɢ, Fɪxɪɴɢ Bᴜɢs, Eʀʀᴏʀs ᴀɴᴅ Aᴅᴅɪɴɢ Nᴇᴡ Fᴇᴀᴛᴜʀᴇs

    📝 <b>Rᴇᴀsᴏɴ</b> : <code>{MAINTENANCE["reason"]}</code>"""
        )

        raise StopPropagation

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #