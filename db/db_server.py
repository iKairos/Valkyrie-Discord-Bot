import sqlite3 as sql
from db import db_hfuncts

class DB_Server(db_hfuncts.DB_Helpers):
    def __init__(self):
        self.db_directory = "db/data/mainconfigs.db"
    
    def append_server(self, server_id):
        try:
            self.append_row(
                "mainconfigs",
                server_id=server_id,
                log_activities=0,
                log_sanctions=0,
                strict_nrt=0,
                mute_role=None,
                logging_channel=None,
                vc_role=None,
                cmd_channel=None
            )
            return True
        except:
            return False
    
    def remove_server(self, server_id):
        try:
            self.purge_row(
                "mainconfigs",
                server_id=server_id
            )
            return True
        except:
            return False
    
    def toggle_act_logging(self, server_id, logging):
        try:
            self.update_data(
                "mainconfigs",
                "log_activities",
                logging,
                server_id=server_id
            )
            return True
        except:
            return False
    
    def toggle_sanction_logging(self, server_id, logging):
        try:
            self.update_data(
                "mainconfigs",
                "log_sanctions",
                logging,
                server_id=server_id
            )
            return True
        except:
            return False
    
    def toggle_strict_nrt(self, server_id, strict):
        try:
            self.update_data(
                "mainconfigs",
                "strict_nrt",
                strict,
                server_id=server_id
            )
            return True
        except:
            return False
    
    def is_registered(self, server_id):
        try:
            fetched = self.fetch_row(
                "mainconfigs",
                server_id=server_id
            )

            if len(fetched) == 0:
                return False
            
            return True
        except:
            return False
    
    def logging_allowed(self, server_id):
        try:
            fetched = self.fetch_row(
                "mainconfigs",
                server_id=server_id
            )

            if fetched[0][1] == 1:
                return True
            else:
                return False
        except:
            return False
    
    def logging_sanctions_allowed(self, server_id):
        try:
            fetched = self.fetch_row(
                "mainconfigs",
                server_id=server_id
            )

            if fetched[0][2] == 1:
                return True
            else:
                return False
        except:
            return False
    
    def is_strict_nrt(self, server_id):
        try:
            fetched = self.fetch_row(
                "mainconfigs",
                server_id=server_id
            )

            if fetched[0][3] == 1:
                return True
            else:
                return False
        except:
            return False

    def set_mute_role(self, server_id, role):
        try:
            self.update_data(
                "mainconfigs",
                "mute_role",
                role,
                server_id=server_id
            )
            return True
        except:
            return False
    
    def get_mute_role(self, server_id):
        """ Note: This stores a role id """
        try:
            fetched = self.fetch_row(
                "mainconfigs",
                server_id=server_id
            )

            mute_role = fetched[0][4]
            return mute_role
        except:
            return False
    
    def set_logs_channel(self, server_id, channel):
        try:
            self.update_data(
                "mainconfigs",
                "logging_channel",
                channel,
                server_id=server_id
            )
            return True
        except:
            return False
    
    def get_logs_channel(self, server_id):
        """ Note: This stores a channel id """
        try:
            fetched = self.fetch_row(
                "mainconfigs",
                server_id=server_id
            )

            logs_channel = fetched[0][5]
            return logs_channel
        except:
            return False
    
    def get_vc_role(self, server_id):
        try:
            fetched = self.fetch_row(
                "mainconfigs",
                server_id=server_id
            )

            vc_role = fetched[0][6]
            return vc_role
        except:
            return False
    
    def set_vc_role(self, server_id, role):
        try:
            self.update_data(
                "mainconfigs",
                "vc_role",
                role,
                server_id=server_id
            )
            return True
        except:
            return False
    
    def get_cmd_channel(self, server_id):
        try:
            fetched = self.fetch_row(
                "mainconfigs",
                server_id=server_id
            )

            cmd_channel = fetched[0][7]
            return cmd_channel
        except:
            return False
    
    def set_cmd_channel(self, server_id, channel):
        try:
            self.update_data(
                "mainconfigs",
                "cmd_channel",
                channel,
                server_id=server_id
            )
            return True
        except:
            return False
    
    def set_mod_role(self, server_id, role):
        try:
            self.update_data(
                "mainconfigs",
                "mod_role",
                role,
                server_id=server_id
            )
            return True
        except:
            return False
    
    def get_mod_role(self, server_id):
        """ Note: This stores a channel id """
        try:
            fetched = self.fetch_row(
                "mainconfigs",
                server_id=server_id
            )

            mod_role = fetched[0][8]
            return mod_role
        except:
            return False

    def get_welcome_message(self, server_id):
        try:
            fetched = self.fetch_row(
                "mainconfigs",
                server_id=server_id
            )

            message = fetched[0][9]
            return message
        except:
            return False
    
    def set_welcome_message(self, server_id, msg):
        try:
            self.update_data(
                "mainconfigs",
                "welcome_message",
                msg,
                server_id=server_id
            )
            return True
        except:
            return False
    
    def remove_welcome_message(self, server_id):
        try:
            self.update_data(
                "mainconfigs",
                "welcome_message",
                None,
                server_id=server_id
            )
            return True
        except:
            return False
    
    def get_suggest_channel(self, server_id):
        try:
            fetched = self.fetch_row(
                "mainconfigs",
                server_id=server_id
            )

            suggest = fetched[0][10]
            return suggest
        except:
            return False
    
    def set_suggest_channel(self, server_id, channel):
        try:
            self.update_data(
                "mainconfigs",
                "suggest_channel",
                channel,
                server_id=server_id
            )
            return True
        except:
            return False
    
    def remove_suggest_channel(self, server_id):
        try:
            self.update_data(
                "mainconfigs",
                "suggest_channel",
                None,
                server_id=server_id
            )
            return True
        except:
            return False

    def toggle_public_suggest(self, server_id, public):
        try:
            self.update_data(
                "mainconfigs",
                "public_suggest",
                public,
                server_id=server_id
            )
            return True
        except:
            return False
    
    def get_bool_public(self, server_id):
        try:
            fetched = self.fetch_row(
                "mainconfigs",
                server_id=server_id
            )

            if fetched[0][11] == 1:
                return True
            else:
                return False
        except:
            return False
    
    def set_public_suggest(self, server_id, channel):
        try:
            self.update_data(
                "mainconfigs",
                "public_suggest_chan",
                channel,
                server_id=server_id
            )
            return True
        except:
            return False
    
    def get_public_suggest(self, server_id):
        try:
            fetched = self.fetch_row(
                "mainconfigs",
                server_id=server_id
            )

            suggest = fetched[0][12]
            return suggest
        except:
            return False
    
    def remove_suggest_channel(self, server_id):
        try:
            self.update_data(
                "mainconfigs",
                "public_suggest_chan",
                None,
                server_id=server_id
            )
            return True
        except:
            return False
    
    def add_assignable_role(self, server_id, role_id):
        try:
            self.append_row(
                "assignable_roles",
                server_id=server_id,
                role_id=role_id
            )
            return True
        except:
            return False
    
    def revoke_assignable_role(self, server_id, role_id):
        try:
            self.purge_row(
                "assignable_roles",
                server_id=server_id,
                role_id = role_id
            )
            return True
        except:
            return False

    def assignable_roles(self, server_id):
        try:
            fetched = self.fetch_row(
                "assignable_roles",
                server_id=server_id,
            )

            roles = []

            for data in fetched:
                roles.append(data[1])

            return roles
        except:
            return False