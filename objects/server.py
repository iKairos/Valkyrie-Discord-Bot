from db import db_server

class Server:
    """
    Server object: Pass server id to make it work lol ty.
    """
    def __init__(self, server_id):
        self.server_id = server_id
        self.db = db_server.DB_Server()

    @property
    def is_Registered(self):
        return self.db.is_registered(self.server_id)
    
    @property
    def logging_allowed(self):
        return self.db.logging_allowed(self.server_id)
    
    @property
    def sanction_logs_allowed(self):
        return self.db.logging_sanctions_allowed(self.server_id)
    
    @property
    def is_strict_nrt(self):
        return self.db.is_strict_nrt(self.server_id)
    
    @property
    def mute_role(self):
        return self.db.get_mute_role(self.server_id)
    
    @property
    def logs_channel(self):
        return self.db.get_logs_channel(self.server_id)
    
    @property
    def vc_role(self):
        return self.db.get_vc_role(self.server_id)
    
    @property
    def cmd_channel(self):
        return self.db.get_cmd_channel(self.server_id)

    @property
    def welcome_message(self):
        return self.db.get_welcome_message(self.server_id)
    
    @property
    def mod_role(self):
        return self.db.get_mod_role(self.server_id)
    
    @property
    def suggest_channel(self):
        return self.db.get_suggest_channel(self.server_id)
    
    @property
    def is_public_suggest(self):
        return self.db.get_bool_public(self.server_id)
    
    @property
    def public_suggest_channel(self):
        return self.db.get_public_suggest(self.server_id)
    
    @property
    def assignable_roles(self):
        return self.db.assignable_roles(self.server_id)
    
    def append_server(self):
        return self.db.append_server(self.server_id)
    
    def remove_server(self):
        return self.db.remove_server(self.server_id)

    def toggle_logging(self, option):
        return self.db.toggle_act_logging(self.server_id, option)
    
    def toggle_sanctions(self, option):
        return self.db.toggle_sanction_logging(self.server_id, option)
    
    def toggle_strict_nrt(self, option):
        return self.db.toggle_strict_nrt(self.server_id, option)
    
    def set_mute_role(self, role_id):
        return self.db.set_mute_role(self.server_id, role_id)
    
    def set_logs_channel(self, channel_id):
        return self.db.set_logs_channel(self.server_id, channel_id)
    
    def set_vc_role(self, role):
        return self.db.set_vc_role(self.server_id, role)
    
    def set_cmd_channel(self, channel):
        return self.db.set_cmd_channel(self.server_id, channel)
    
    def set_mod_role(self, role):
        return self.db.set_mod_role(self.server_id, role)
    
    def set_welcome_message(self, string):
        return self.db.set_welcome_message(self.server_id, string)
    
    def remove_welcome_message(self):
        return self.db.remove_welcome_message(self.server_id)
    
    def set_suggest_channel(self, channel):
        return self.db.set_suggest_channel(self.server_id, channel)
    
    def remove_suggest_channel(self):
        return self.db.remove_suggest_channel(self.server_id)
    
    def toggle_public_suggest(self, choice):
        return self.db.toggle_public_suggest(self.server_id, choice)
    
    def set_public_suggest(self, channel):
        return self.db.set_public_suggest(self.server_id, channel)
    
    def remove_public_suggest(self):
        return self.db.remove_public_suggest(self.server_id)
    
    def add_assignable_role(self, role):
        return self.db.add_assignable_role(self.server_id, role)
    
    def remove_assignable_role(self, role):
        return self.db.revoke_assignable_role(self.server_id, role)