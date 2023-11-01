from telethon import Button
from global_data import global_data
from telethon import types


def generate_sources_kb(sub_id):
    sub_sources = global_data.get_items(
        'sub_preferences', filter1='subscriber_id', value1=sub_id, to_dict=True)
    del sub_sources[0]['subscriber_id']

    sources_name = dict(global_data.get_items(
        'channels', columns='channel_id, channel_name'))

    # inline_keyboard = types.InlineKeyboardMarkup()
    inline_keyboard = []
    for channel_id, channel_follow_status in sub_sources[0].items():
        emodji = '❌'
        if channel_follow_status:
            emodji = '✅'
        channel_id = int(channel_id)
        button = types.KeyboardButtonCallback(
            emodji+sources_name[channel_id], data=str(channel_id))
        inline_keyboard.append([button])

    return inline_keyboard


administrator_kb = [[Button.text('Обновить список каналов', resize=True)],
                    [Button.text('Обновить список подписчиков', resize=True)],
                    [Button.text(
                        'Обновить список администраторов', resize=True)],
                    [Button.text('Обновить список модераторов', resize=True)],
                    [Button.text('Обновить все списки', resize=True)],
                    [Button.text('Добавить администратора', resize=True)],
                    [Button.text('Добавить модератора', resize=True)],
                    [Button.text('Добавить канал для перессылки', resize=True)],
                    [Button.text('Добавить/изменить подписчика', resize=True)],
                    [Button.text('Удалить канал для перессылки', resize=True)],
                    [Button.text('Удалить подписчика', resize=True)],
                    [Button.text('Удалить администратора', resize=True)],
                    [Button.text('Удалить модератора', resize=True)]
                    ]

administrator_labels = [line[0].button.text for line in administrator_kb]

moderator_kb = [[Button.text('Обновить список каналов', resize=True)],
                [Button.text('Обновить список подписчиков', resize=True)],
                [Button.text('Обновить все списки', resize=True)],
                [Button.text('Добавить канал для перессылки', resize=True)],
                [Button.text('Удалить канал для перессылки', resize=True)],
                [Button.text('Удалить подписчика', resize=True)]
                ]

moderator_labels = [line[0].button.text for line in moderator_kb]

cancel_kb = [
    [Button.text('Отмена', resize=True)]]

yes_no_cancel_kb = [[Button.text('Да', resize=True), Button.text('Нет', resize=True)],
                    [Button.text('Отмена', resize=True)]]


def generate_topics_kb(topics):
    inline_keyboard = []
    print(topics)
    for topic_title in topics:
        print(topic_title)
        button = Button.text(topic_title, resize=True)
        print(button)
        inline_keyboard.append([button])

    inline_keyboard.append([Button.text('Отмена', resize=True)])
    return inline_keyboard


def generate_channel_list_kb():
    inline_keyboard = []
    for channel in global_data.listen_channels:
        button = Button.text(
            global_data.listen_channels[channel]['name'], resize=True)
        inline_keyboard.append([button])

    inline_keyboard.append([Button.text('Отмена', resize=True)])
    return inline_keyboard
