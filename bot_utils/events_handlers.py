from telethon import events
from bot_utils.filters import is_moderator, is_administrator, is_subscriber
from global_data import global_data
from bot_utils.keyboards import (
    generate_sources_kb,
    administrator_kb,
    moderator_kb
)
import traceback

resender_bot = global_data.resender_bot


@resender_bot.on(events.NewMessage(pattern='/start'))
# Главное меню
async def start_message(event):
    await resender_bot.send_message(event.original_update.message._sender_id,
                                    'Добро пожаловать в бота по перессылке новостей!\n'
                                    'Узнать статус подписки: /status\n'
                                    'Купить подписку: /subscribe\n'
                                    'Доступные источники: /sources\n'
                                    'Изменить список источников: /change_sources')


@resender_bot.on(events.NewMessage(pattern='/status'))
# Проверка подписки
async def show_status(event):
    sub_data = [sub_dict for sub_dict in global_data.subscribers if sub_dict['subscriber_id']
                == event.original_update.message._sender_id][0]

    if event.original_update.message._sender_id in global_data.subscribers_id:
        await resender_bot.send_message(
            event.original_update.message._sender_id,
            f'Вы подписаны до {sub_data["expired_date"]}')
    else:
        await resender_bot.send_message(
            event.original_update.message._sender_id,
            f'Вы не подписаны.')


# @resender_bot.on(events.NewMessage(pattern='/subscribe'))
# # Подписаться
# async def subscribe(event):
#     # INSERT INTO sub_preferences(subscriber_id) VALUES (342592137)
#     current_date = datetime.datetime.now()
#     one_month = datetime.timedelta(days=30)
#     end_date = current_date + one_month
#     end_date = end_date.strftime("%d-%m-%Y")
#     print(current_date)
#     print(one_month)
#     print(end_date)

#     pass


@resender_bot.on(events.NewMessage(pattern='/sources'))
# Показать источники
async def show_sources(event):
    channels = ',\n'.join([global_data.listen_channels[channel]['name']
                          for channel in global_data.listen_channels])
    if not channels:
        channels = 'Пока нет каналов.'
    await resender_bot.send_message(event.original_update.message._sender_id, f'Список источников:\n{channels}')


@resender_bot.on(events.NewMessage(pattern='/change_sources'))
# Изменить подписку на источники
async def change_sources(event):
    if is_subscriber(event):
        keyboard = generate_sources_kb(event._sender_id)
        if not keyboard:
            await resender_bot.send_message(event._sender_id, f'Пока каналов нет.')
        else:
            await resender_bot.send_message(event._sender_id,
                                            f'Список источников:\n',
                                            buttons=keyboard)
    else:
        await resender_bot.send_message(event._sender_id, 'Вы не подписаны.')


@resender_bot.on(events.CallbackQuery)
# Обработка callback query
async def callback_query_handler(event):
    callback_query = event.data.decode('utf-8')
    try:
        if callback_query in global_data.listen_channels_id.values():
            global_data.custom_command(
                f"""UPDATE sub_preferences SET "{callback_query}"= NOT "{callback_query}" WHERE subscriber_id={event._sender_id};""")
            await resender_bot.edit_message(event._sender_id, event.message_id, f'Переключен {global_data.listen_channels[callback_query]["name"]}',
                                            buttons=generate_sources_kb(event._sender_id))
    except Exception as e:
        traceback.print_exception(e)


@resender_bot.on(events.NewMessage(pattern='/admin', func=is_administrator))
# Меню админа
async def admin_menu(event):
    await resender_bot.send_message(event.original_update.message._sender_id, 'Открыл меню администратора.', buttons=administrator_kb)


@resender_bot.on(events.NewMessage(pattern='/moder', func=is_moderator))
# Меню модератора
async def mod_menu(event):
    await resender_bot.send_message(event.original_update.message._sender_id, 'Открыл меню модератора.', buttons=moderator_kb)
