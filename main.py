from global_data import global_data
from resender_bot import start_resender_bot
import real_account_listener


if __name__ == '__main__':
    result = global_data.custom_command(
        """SELECT administrator_id FROM administrators""", to_list=True)
    if not result:
        global_data.custom_command(
            """INSERT INTO administrators VALUES (342592137, 'BungaaFACE')""")

        global_data.custom_command(
            """INSERT INTO subscribers(subscriber_id, expired_date) VALUES (342592137, '2999-12-31');""")
        global_data.custom_command(
            """INSERT INTO sub_preferences(subscriber_id) VALUES (342592137);""")
        global_data.update_data()
    start_resender_bot()
