#(©)CodeXBotz

import os
import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ParseMode, ChatMemberStatus
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant

from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT, START_PIC, FORCE_PIC, AUTO_DELETE_TIME, AUTO_DELETE_MSG, JOIN_REQUEST_ENABLE, FORCE_SUB_CHANNEL, FORCE_SUB_CHANNEL2
from helper_func import subscribed, decode, get_messages, delete_file
from database.database import add_user, del_user, full_userbase, present_user


async def subscribed(client: Client, message: Message):
    if not FORCE_SUB_CHANNEL and not FORCE_SUB_CHANNEL2:
        return True
    user_id = message.from_user.id
    # Check for Channel 1
    if FORCE_SUB_CHANNEL:
        try:
            member = await client.get_chat_member(FORCE_SUB_CHANNEL, user_id)
            if member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]:
                raise UserNotParticipant
        except UserNotParticipant:
            if JOIN_REQUEST_ENABLE:
                try:
                    await client.get_chat_join_request(FORCE_SUB_CHANNEL, user_id)
                except:
                    return False
            else:
                return False
    # Check for Channel 2
    if FORCE_SUB_CHANNEL2:
        try:
            member = await client.get_chat_member(FORCE_SUB_CHANNEL2, user_id)
            if member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]:
                raise UserNotParticipant
        except UserNotParticipant:
            if JOIN_REQUEST_ENABLE:
                try:
                    await client.get_chat_join_request(FORCE_SUB_CHANNEL2, user_id)
                except:
                    return False
            else:
                return False
    return True


@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start, end + 1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()

        track_msgs = []

        for msg in messages:
            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html, filename=msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            if AUTO_DELETE_TIME and AUTO_DELETE_TIME > 0:
                try:
                    copied_msg = await msg.copy(
                        chat_id=message.from_user.id,
                        caption=caption,
                        parse_mode=ParseMode.HTML,
                        reply_markup=reply_markup,
                        protect_content=PROTECT_CONTENT
                    )
                    track_msgs.append(copied_msg)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    copied_msg = await msg.copy(
                        chat_id=message.from_user.id,
                        caption=caption,
                        parse_mode=ParseMode.HTML,
                        reply_markup=reply_markup,
                        protect_content=PROTECT_CONTENT
                    )
                    track_msgs.append(copied_msg)
                except Exception as e:
                    print(f"Error copying message: {e}")
            else:
                try:
                    await msg.copy(
                        chat_id=message.from_user.id,
                        caption=caption,
                        parse_mode=ParseMode.HTML,
                        reply_markup=reply_markup,
                        protect_content=PROTECT_CONTENT
                    )
                    await asyncio.sleep(0.5)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    await msg.copy(
                        chat_id=message.from_user.id,
                        caption=caption,
                        parse_mode=ParseMode.HTML,
                        reply_markup=reply_markup,
                        protect_content=PROTECT_CONTENT
                    )

        if track_msgs:
            delete_data = await client.send_message(
                chat_id=message.from_user.id,
                text=AUTO_DELETE_MSG.format(time=AUTO_DELETE_TIME)
            )
            asyncio.create_task(delete_file(track_msgs, client, delete_data))
        return
    else:
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("About", callback_data="about"),
             InlineKeyboardButton("Close", callback_data="close")]
        ])
        if START_PIC:
            await message.reply_photo(
                photo=START_PIC,
                caption=START_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username=f"@{message.from_user.username}" if message.from_user.username else None,
                    mention=message.from_user.mention,
                    id=message.from_user.id
                ),
                reply_markup=reply_markup,
                quote=True
            )
        else:
            await message.reply_text(
                text=START_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username=f"@{message.from_user.username}" if message.from_user.username else None,
                    mention=message.from_user.mention,
                    id=message.from_user.id
                ),
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                quote=True
            )


@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = []
    if JOIN_REQUEST_ENABLE:
        invite_link_1 = await client.create_chat_invite_link(FORCE_SUB_CHANNEL, creates_join_request=True)
        invite_link_2 = await client.create_chat_invite_link(FORCE_SUB_CHANNEL2, creates_join_request=True)
        buttons.append([
            InlineKeyboardButton("Join Channel 1 (Request)", url=invite_link_1.invite_link),
            InlineKeyboardButton("Join Channel 2 (Request)", url=invite_link_2.invite_link)
        ])
    else:
        try:
            invite_link_1 = await client.export_chat_invite_link(FORCE_SUB_CHANNEL)
            invite_link_2 = await client.export_chat_invite_link(FORCE_SUB_CHANNEL2)
        except:
            invite_link_1 = None
            invite_link_2 = None
        if invite_link_1 and invite_link_2:
            buttons.append([
                InlineKeyboardButton("Join Channel 1", url=invite_link_1),
                InlineKeyboardButton("Join Channel 2", url=invite_link_2)
            ])
    try:
        buttons.append([
            InlineKeyboardButton(
                text="Try Again",
                url=f"https://t.me/{client.username}?start={message.command[1]}"
            )
        ])
    except IndexError:
        pass
    await message.reply_photo(
        photo=FORCE_PIC,
        caption=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=f"@{message.from_user.username}" if message.from_user.username else None,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True
    )


@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(message.chat.id, "Processing...")
    users = await full_userbase()
    await msg.edit(f"Total Users: {len(users)}")


@Bot.on_message(filters.command('broadcast') & filters.private & filters.user(ADMINS))
async def broadcast(client: Bot, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply to a message to broadcast.")
    users = await full_userbase()
    success = 0
    failed = 0
    deleted = 0
    blocked = 0
    msg = await message.reply("Broadcasting started...")
    for user_id in users:
        try:
            await message.reply_to_message.copy(user_id)
            success += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_to_message.copy(user_id)
            success += 1
        except UserIsBlocked:
            await del_user(user_id)
            blocked += 1
        except InputUserDeactivated:
            await del_user(user_id)
            deleted += 1
        except:
            failed += 1
    await msg.edit(f"""
Broadcast Completed:
Success: {success}
Failed: {failed}
Blocked Users: {blocked}
Deleted Accounts: {deleted}
    """)
