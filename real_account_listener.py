from bot_utils.filters import is_listen_channel, is_administrator, is_listen_reply_id
from telethon import events
from global_data import global_data
from telethon import functions
from transliterate import translit
import emoji


real_client = global_data.real_account_bot
resender_bot = global_data.resender_bot


@real_client.on(events.NewMessage(pattern='1', func=is_administrator))
# test
async def test_function(event):
    print('got it')
    dialogs = await real_client.get_dialogs()
    for dialog in dialogs:
        if 'лул' in dialog.name.lower():
            channel_id = dialog.entity.id
            channel_name = dialog.name
            break
    result = await real_client(functions.channels.GetForumTopicsRequest(
        channel=channel_id,
        offset_date=None,
        offset_id=0,
        offset_topic=0,
        limit=100,
        # q='some string here'
    ))

    channel_str_id = translit(emoji.replace_emoji(
        channel_name), reversed=True).lower()
    print(channel_str_id)
    # message = (await real_client.get_messages(
    #     channel_id, search='Закрыл позицию, не уверен', limit=1))[0]
    # print(message.stringify())
    # print()
    # print(message.reply_to.reply_to_top_id)


@real_client.on(events.NewMessage(func=is_listen_channel))
async def handler(event):
    # На случай, если в сообщении несколько фотографий/видео
    if event.grouped_id:
        return
    telegram_id = event.chat_id
    channel_id = global_data.listen_channels[telegram_id]
    channel_name = global_data.listen_channels_id[channel_id]['name']

    if is_listen_reply_id(telegram_id):
        event.message.message = f"{channel_name}:\n" + event.message.message

        channel_subscribed_ids = global_data.custom_command(
            f'SELECT subscriber_id FROM sub_preferences WHERE "{channel_id}" = True', to_list=True)
        for subscriber in channel_subscribed_ids:
            await resender_bot.send_message(subscriber, event.message)


@real_client.on(events.Album(func=is_listen_channel))
async def handler(event):
    # Обработка сообщения с несколькими картинками/видео
    telegram_id = event.chat_id
    channel_id = global_data.listen_channels[telegram_id]
    channel_name = global_data.listen_channels[telegram_id]['name']
    # event.original_update.message.reply_to.reply_to_msg_id

    if is_listen_reply_id(channel_id):
        channel_subscribed_ids = global_data.custom_command(
            f'SELECT subscriber_id FROM sub_preferences WHERE "{channel_id}" = True', to_list=True)
        for subscriber in channel_subscribed_ids:
            if is_listen_reply_id(channel_id):
                await resender_bot.send_message(
                    subscriber,
                    file=event.messages,  # event.messages is a List - meaning we're sending an album
                    message=f"{channel_name}:\n" + \
                    event.original_update.message.message,
                )


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    real_client.run_until_disconnected()
