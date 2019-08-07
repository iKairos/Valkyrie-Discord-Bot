from db import db_channel

class Channel:
    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.db = db_channel.DB_Channel()
    
    @property
    def is_Registered(self):
        return self.db.is_registered(self.channel_id)
    
    @property
    def is_NSFW(self):
        return self.db.is_nsfw(self.channel_id)

    @property
    def persistence(self):
        return self.db.get_persistence(self.channel_id)
    
    @property
    def info(self):
        return self.db.channel_info(self.channel_id)
    
    @property
    def is_log_blocked(self):
        return self.db.is_log_blocked(self.channel_id)
    
    def append_channel(self):
        return self.db.append_channel(self.channel_id)
    
    def remove_channel(self):
        return self.db.remove_channel(self.channel_id)
    
    def toggle_nsfw(self, option):
        return self.db.toggle_nsfw(self.channel_id, option)
    
    def set_persistence(self, value):
        return self.db.set_persistence(self.channel_id, value)
    
    def toggle_log_block(self, option):
        return self.db.set_log_block(self.channel_id, option)
