import real_account_listener
from resender_bot import start_resender_bot
from global_data import global_data


if __name__ == '__main__':
    result = global_data.custom_command(
        """SELECT administrator_id FROM administrators""", to_list=True)
    if not result:
        global_data.custom_command(
            """INSERT INTO administrators VALUES (342592137, 'BungaaFACE')""")
        global_data.update_administrators()
    start_resender_bot()
