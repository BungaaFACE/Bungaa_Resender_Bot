from DbInteractor import DbInteractor


class LoadedDbData(DbInteractor):
    def __init__(self):
        super().__init__()
        self.update_data()

    def update_channels(self):
        listen_channels = self.get_items('channels', to_dict=True)
        self.listen_channels = {channel['channel_id']: {
            'id': channel['telegram_id'],
            'name': channel['channel_name'],
            'reply_id': channel['reply_id']}
            for channel in listen_channels}
        self.listen_channels_id = {
            channel['telegram_id']: channel['channel_id'] for channel in listen_channels}

    def update_subscribers(self):
        self.subscribers = self.get_items('subscribers', to_dict=True)
        self.subscribers_id = self.get_items(
            'subscribers', columns='subscriber_id', to_list=True)

    def update_administrators(self):
        self.administrators_id = self.get_items(
            'administrators', columns='administrator_id', to_list=True)

    def update_moderators(self):
        self.moderators_id = self.get_items(
            'moderators', columns='moderator_id', to_list=True)

    def update_data(self):
        self.update_channels()
        self.update_subscribers()
        self.update_administrators()
        self.update_moderators()


if __name__ == '__main__':
    db = LoadedDbData()
