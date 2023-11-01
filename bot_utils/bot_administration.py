from telethon import events, functions
from transliterate import translit
import emoji
from global_data import global_data
from bot_utils.filters import is_moderator, is_administrator, is_admin_action, is_moder_action
from bot_utils.keyboards import (
    generate_sources_kb,
    administrator_kb,
    moderator_kb,
    cancel_kb,
    yes_no_cancel_kb,
    generate_topics_kb,
    generate_channel_list_kb
)

resender_bot = global_data.resender_bot
real_account_bot = global_data.real_account_bot


@resender_bot.on(events.NewMessage(func=is_administrator))
# Обработка админ меню
async def admin_menu_actions(event):
    if is_admin_action(event):
        match event.message.message:
            case 'Обновить список каналов':
                global_data.update_channels()
                await resender_bot.send_message(event._sender_id, 'Обновлено.', buttons=administrator_kb)

            case 'Обновить список подписчиков':
                global_data.update_subscribers()
                await resender_bot.send_message(event._sender_id, 'Обновлено.', buttons=administrator_kb)

            case 'Обновить список администраторов':
                global_data.update_administrators()
                await resender_bot.send_message(event._sender_id, 'Обновлено.', buttons=administrator_kb)

            case 'Обновить список модераторов':
                global_data.update_moderators()
                await resender_bot.send_message(event._sender_id, 'Обновлено.', buttons=administrator_kb)

            case 'Обновить все списки':
                global_data.update_data()
                await resender_bot.send_message(event._sender_id, 'Обновлено.', buttons=administrator_kb)

            case 'Добавить администратора':
                response_event = await wait_for_response(event,
                                                         'Отправьте @username администратора в чат.')
                if response_event:
                    if response_event.text[0] == '@':
                        username = response_event.text[1:]
                        entity = await resender_bot.get_entity(username)
                        user_id = entity.id
                        global_data.custom_command(
                            sql_exec=f"""INSERT INTO administrators(administrator_id, account_name) VALUES({user_id}, '{username}');""")
                        global_data.update_data()
                        await resender_bot.send_message(event._sender_id, f'Добавлен администратор @{username}.', buttons=administrator_kb)
                    elif response_event.text == 'Отмена':
                        await resender_bot.send_message(event._sender_id, f'Добавление отменено.', buttons=administrator_kb)
                    else:
                        await resender_bot.send_message(event._sender_id, f'Некорректный формат @username.', buttons=administrator_kb)

            case 'Добавить модератора':
                response_event = await wait_for_response(event,
                                                         'Отправьте @username модератора в чат.')
                if response_event:
                    if response_event.text[0] == '@':
                        username = response_event.text[1:]
                        entity = await resender_bot.get_entity(username)
                        user_id = entity.id
                        global_data.custom_command(
                            sql_exec=f"""INSERT INTO moderators(moderator_id, account_name) VALUES({user_id}, '{username}');""")
                        global_data.update_data()
                        await resender_bot.send_message(event._sender_id, f'Добавлен модератор @{username}.', buttons=administrator_kb)
                    elif response_event.text == 'Отмена':
                        await resender_bot.send_message(event._sender_id, f'Добавление отменено.', buttons=administrator_kb)
                    else:
                        await resender_bot.send_message(event._sender_id, f'Некорректный формат @username.', buttons=administrator_kb)

            case 'Добавить канал для перессылки':
                # Имя канала
                response_event = await wait_for_response(event,
                                                         'Введите название канала для добавления.')
                if response_event:
                    if response_event.text == 'Отмена':
                        await resender_bot.send_message(event._sender_id, f'Добавление отменено.', buttons=administrator_kb)
                        return
                    channel_name = response_event.text.lower()
                    dialogs = await global_data.real_account_bot.get_dialogs()
                    for dialog in dialogs:
                        if channel_name in dialog.name.lower():
                            telegram_id = dialog.entity.id
                            channel_name = dialog.name
                            break
                # Несколько чатов или нет?
                response_event = await wait_for_response(event,
                                                         'У канала несколько чатов?', keyboard=yes_no_cancel_kb)
                if response_event:
                    if response_event.text == 'Отмена':
                        await resender_bot.send_message(event._sender_id, f'Добавление отменено.', buttons=administrator_kb)
                        return
                    elif response_event.text == 'Да':
                        multichat = True
                    elif response_event.text == 'Нет':
                        multichat = False
                    else:
                        await resender_bot.send_message(event._sender_id, f'Некорректный формат ответа.', buttons=administrator_kb)
                        return

                # Обработка случая нескольких чатов в канале
                if multichat:
                    topics_response = await global_data.real_account_bot(functions.channels.GetForumTopicsRequest(
                        channel=telegram_id,
                        offset_date=None,
                        offset_id=0,
                        offset_topic=0,
                        limit=100
                    ))
                    topics = {
                        topic.title: topic.id for topic in topics_response.topics}
                    response_event = await wait_for_response(event,
                                                             'Выберите название чата для перессылки.', keyboard=generate_topics_kb(topics))
                    if response_event:
                        if response_event.text == 'Отмена':
                            await resender_bot.send_message(event._sender_id, f'Добавление отменено.', buttons=administrator_kb)
                            return
                        else:
                            if response_event.text in topics:
                                topic_name = response_event.text
                                reply_id = topics[topic_name]
                                channel_name = channel_name + ': ' + topic_name
                            else:
                                await resender_bot.send_message(event._sender_id, f'Такого чата нет. Добавление отменено.', buttons=administrator_kb)
                                return

                # replace_emoji - delete emojis from channel name, translit - transliterate russian (or any) name to eng letters
                channel_id = translit(emoji.replace_emoji(
                    channel_name), reversed=True).lower().replace(':', '').replace(' ', '_')

                if channel_id in global_data.listen_channels:
                    await resender_bot.send_message(event._sender_id, f'Этот канал/чат уже добавлен.', buttons=administrator_kb)
                    return
                else:
                    add_channel_sql = f"""INSERT INTO channels VALUES ('{channel_id}', {telegram_id}, '{channel_name}'"""
                    if multichat:
                        add_channel_sql += f""", {reply_id}"""
                    add_channel_sql += ');'

                global_data.custom_command(add_channel_sql)
                global_data.update_channels()
                add_sub_preferences_column = f"""ALTER TABLE sub_preferences ADD {channel_id} BOOLEAN DEFAULT TRUE;"""
                global_data.custom_command(add_sub_preferences_column)

                global_data.update_channels()
                await resender_bot.send_message(event._sender_id, f'Канал добавлен.', buttons=administrator_kb)

            case 'Добавить/изменить подписчика':
                pass
                """
                INSERT INTO subscribers(subscriber_id, expired_date) VALUES (6127217856, '2999-12-31');
                INSERT INTO sub_preferences(subscriber_id) VALUES (6127217856);
                """

            case 'Удалить канал для перессылки':
                response_event = await wait_for_response(event, 'Выберите канал для удаления.', keyboard=generate_channel_list_kb())
                if response_event:
                    if response_event.text == 'Отмена':
                        await resender_bot.send_message(event._sender_id, f'Добавление отменено.', buttons=administrator_kb)
                        return
                    else:
                        for channel_id in global_data.listen_channels:
                            if response_event.text == global_data.listen_channels[channel_id]['name']:
                                delete_sub_preferences_column = f"""ALTER TABLE sub_preferences DROP COLUMN {channel_id};"""
                                delete_channel = f"""DELETE FROM channels WHERE channel_id = "{channel_id}";"""

                                global_data.custom_command(
                                    delete_sub_preferences_column)
                                global_data.custom_command(delete_channel)
                                break
                        else:
                            await resender_bot.send_message(event._sender_id, f'Канал не найден.', buttons=administrator_kb)

                    global_data.update_channels()
                    await resender_bot.send_message(event._sender_id, f'Канал удален.', buttons=administrator_kb)

            case 'Удалить подписчика':
                pass

            case 'Удалить администратора':
                response_event = await wait_for_response(event,
                                                         'Отправьте @username для удаления в чат.')
                if response_event:
                    if response_event.text[0] == '@':
                        username = response_event.text[1:]
                        entity = await resender_bot.get_entity(username)
                        user_id = entity.id
                        global_data.custom_command(
                            sql_exec=f"""DELETE FROM administrators WHERE administrator_id = '{user_id}';""")
                        global_data.update_data()
                        await resender_bot.send_message(event._sender_id, f'Удален администратор @{username}.', buttons=administrator_kb)
                    elif response_event.text == 'Отмена':
                        await resender_bot.send_message(event._sender_id, f'Удаление отменено.', buttons=administrator_kb)
                    else:
                        await resender_bot.send_message(event._sender_id, f'Некорректный формат @username.', buttons=administrator_kb)

            case 'Удалить модератора':
                response_event = await wait_for_response(event,
                                                         'Отправьте @username для удаления в чат.')
                if response_event:
                    if response_event.text[0] == '@':
                        username = response_event.text[1:]
                        entity = await resender_bot.get_entity(username)
                        user_id = entity.id
                        global_data.custom_command(
                            sql_exec=f"DELETE FROM moderators WHERE moderator_id = {user_id}")
                        global_data.update_data()
                        await resender_bot.send_message(event._sender_id, f'Удален модератор @{username}.', buttons=administrator_kb)
                    elif response_event.text == 'Отмена':
                        await resender_bot.send_message(event._sender_id, f'Удаление отменено.', buttons=administrator_kb)
                    else:
                        await resender_bot.send_message(event._sender_id, f'Некорректный формат @username.', buttons=administrator_kb)

    # Если бот перезапустился, а менюшка осталась - даем администратору возможность выйти в меню
    elif event.message.message == 'Отмена':
        await resender_bot.send_message(event._sender_id, f'Отмена.', buttons=administrator_kb)


@resender_bot.on(events.NewMessage(func=is_moderator))
# Обработка модер меню
async def moder_menu_actions(event):
    if is_moder_action(event) and not is_administrator(event):
        client = event.client
        await client.send_message(event.original_update.message._sender_id, 'Открыл админ-меню.', buttons=administrator_kb)


async def wait_for_response(event, message, photo=None, keyboard=cancel_kb):
    import asyncio
    client = event.client
    chat_id = event.message.chat.id
    async with client.conversation(chat_id) as conv:

        # Сообщение и кнопка отмены
        await conv.send_message(message, file=photo, buttons=keyboard)

        # Ожидание ответа
        tasks = [conv.get_response()]
        done, pendind = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        event = done.pop().result()
        return event
