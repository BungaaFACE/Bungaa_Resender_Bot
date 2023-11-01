import bot_utils.events_handlers
import bot_utils.bot_administration
import bot_utils.subscribe
from telethon import functions, types
from global_data import global_data

resender_bot = global_data.resender_bot

USER_COMMANDS = [
    types.BotCommand(
        command='start',
        description='Открыть меню'),
    types.BotCommand(
        command='status',
        description='Узнать статус подписки'),
    types.BotCommand(
        command='subscribe',
        description='Купить подписку'),
    types.BotCommand(
        command='sources',
        description='Доступные источники'),
    types.BotCommand(
        command='change_sources',
        description='Изменить список источников')
]


def start_resender_bot():

    # Добавление подсказок при вводе команды
    resender_bot.loop.run_until_complete(
        resender_bot(functions.bots.SetBotCommandsRequest(
            scope=types.BotCommandScopeDefault(),
            lang_code='',
            commands=USER_COMMANDS)))

    resender_bot.run_until_disconnected()


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    start_resender_bot()
