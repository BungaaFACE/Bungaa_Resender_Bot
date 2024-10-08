from global_data import global_data, REAL_ACCOUNT_ID
from bot_utils.keyboards import administrator_labels, moderator_labels
from telethon import utils


def is_administrator(event):
    try:
        return event.original_update.message.peer_id.user_id in global_data.administrators_id
    except:
        return event.original_update.user_id in global_data.administrators_id


def is_moderator(event):
    try:
        return event.original_update.message.peer_id.user_id in global_data.moderators_id
    except:
        return event.original_update.user_id in global_data.moderators_id


def is_admin_action(event):
    try:
        if event.message.message in administrator_labels:
            return True
    except:
        return False


def is_moder_action(event):
    try:
        if event.message.message in moderator_labels:
            return True
    except:
        return False


def is_listen_channel(event):
    real_id, peer_type = utils.resolve_id(event.chat_id)
    return real_id in global_data.listen_channels_id


def is_listen_reply_id(channel_id, message):
    if global_data.listen_channels[channel_id]['reply_id'] != 'NONE':
        return message.reply_to.reply_to_top_id == global_data.listen_channels[channel_id]['reply_id'] or \
            message.reply_to.reply_to_msg_id == global_data.listen_channels[channel_id]['reply_id']
    else:
        return True


def is_subscriber(event):
    return event._sender_id in global_data.subscribers_id


def is_real_account(event):
    return event._sender_id in REAL_ACCOUNT_ID
