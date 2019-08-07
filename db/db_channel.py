import sqlite3 as sql
from db import db_hfuncts

class DB_Channel(db_hfuncts.DB_Helpers):
    def __init__(self):
        self.db_directory = "db/data/channels.db"
    
    def append_channel(self, channel_id):
        try:
            self.append_row(
                "channels",
                channel_id=channel_id,
                is_nsfw=False,
                persistence=0,
                block_log=False
            )
            return True
        except:
            return False
    
    def remove_channel(self, channel_id):
        try:
            self.purge_row(
                "channels",
                channel_id=channel_id
            )
            return True
        except:
            return False
    
    def toggle_nsfw(self, channel_id, nsfw):
        try:
            self.update_data(
                "channels",
                "is_nsfw",
                nsfw,
                channel_id=channel_id
            )
            return True
        except:
            return False
    
    def set_persistence(self, channel_id, persistence):
        try:
            self.update_data(
                "channels",
                "persistence",
                persistence,
                channel_id=channel_id
            )
            return True
        except:
            return False
    
    def is_registered(self, channel_id):
        try:
            fetched = self.fetch_row(
                "channels",
                channel_id=channel_id
            )

            if len(fetched) == 0:
                return False
            
            return True
        except:
            return False
    
    def is_nsfw(self, channel_id):
        try:
            fetched = self.fetch_row(
                "channels",
                channel_id=channel_id
            )

            if fetched[0][1] == 0:
                return False
            else:
                return True
        except:
            return False
    
    def get_persistence(self, channel_id):
        try:
            fetched = self.fetch_row(
                "channels",
                channel_id=channel_id
            )

            return fetched[0][2]
        except:
            return False
    
    def channel_info(self, channel_id):
        try:
            fetched = self.fetch_row(
                "channels",
                channel_id=channel_id
            )

            return fetched
        except:
            return False
    
    def is_log_blocked(self, channel_id):
        try:
            fetched = self.fetch_row(
                "channels",
                channel_id=channel_id
            )

            if fetched[0][3] == 0:
                return False
            else:
                return True
        except:
            return False
    
    def set_log_block(self, channel_id, option):
        try:
            self.update_data(
                "channels",
                "block_log",
                option,
                channel_id=channel_id
            )
        except:
            raise("An error occurred, channel might not be registered yet.")
