from telethon import TelegramClient
from CONFIGURATION import ACCOUNTS_FOLDER, API_ID, API_HASH, RESENDER_API_KEY


class BotEntities:
    def __init__(self):
        self.real_account_bot = TelegramClient(ACCOUNTS_FOLDER+'real_account', API_ID, API_HASH,
                                               device_model="Linux 5.15.0", system_version="Ubuntu 22").start()
        self.resender_bot = TelegramClient(
            ACCOUNTS_FOLDER+'resender_bot', API_ID, API_HASH).start(bot_token=RESENDER_API_KEY)

        super().__init__()

    async def start_bots(self):
        await self.real_account_bot.start()
        await self.resender_bot.start()


if __name__ == '__main__':
    bots = BotEntities()
