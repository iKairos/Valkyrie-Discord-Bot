from db import db_user
from db import db_inventory

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.db = db_user.DB_User()
        self.inventory = db_inventory.DB_Inventory()
    
    @property
    def is_Registered(self):
        return self.db.is_registered(self.user_id)
    
    @property
    def money(self):
        return self.db.get_money(self.user_id)
    
    @property
    def experience(self):
        return self.db.get_experience(self.user_id)
    
    @property
    def level(self):
        return self.db.get_level(self.user_id)
    
    @property
    def reputation(self):
        return self.db.get_reputation(self.user_id)

    @property
    def append_user(self):
        return self.db.register_user(self.user_id)
    
    @property
    def level_up(self):
        return self.db.level_up(self.user_id)
    
    @property
    def increment_rep(self):
        return self.db.add_reputation(self.user_id)
    
    @property
    def warnings(self):
        return self.db.get_warnings(self.user_id)
    
    @property
    def exp_toggled(self):
        return self.db.is_exp_toggled(self.user_id)
    
    @property
    def inter_toggled(self):
        return self.db.is_interact_toggled(self.user_id)
    
    @property
    def increment_warning(self):
        return self.db.add_warning(self.user_id)

    @property
    def about(self):
        return self.db.get_about(self.user_id)
    
    @property
    def equipped_background(self):
        return self.inventory.get_background(self.user_id)
    
    @property
    def user_items(self):
        return self.inventory.get_user_items(self.user_id)
    
    @property
    def equipped_badge(self):
        return self.inventory.equipped_badge(self.user_id)
    
    @property
    def warnings(self):
        return self.db.get_warnings(self.user_id)
    
    @property
    def badges(self):
        return self.inventory.user_badges(self.user_id)
    
    def delete_user_item(self, item_id):
        return self.inventory.delete_user_item(self.user_id, item_id)

    def equip_item(self, item_id):
        return self.inventory.equip_item(self.user_id, item_id)
    
    def unequip_item(self, item_id):
        return self.inventory.unequip_item(self.user_id, item_id)
    
    def get_user_item(self, item_id):
        return self.inventory.get_user_item(self.user_id, item_id)

    def put_background(self, item_id):
        return self.inventory.put_background(self.user_id, item_id)
    
    def set_about(self, string):
        return self.db.set_about(self.user_id, string)

    def add_experience(self, value):
        return self.db.add_experience(self.user_id, value)
    
    def add_money(self, value):
        return self.db.add_money(self.user_id, value)
    
    def toggle_exp(self, option):
        return self.db.toggle_exp(self.user_id, option)
    
    def toggle_inter(self, option):
        return self.db.toggle_inter(self.user_id, option)
    
    def store_badge(self, badge):
        return self.inventory.store_badge(self.user_id, badge)
    
    def equip_badge(self, badge):
        return self.inventory.equip_badge(self.user_id, badge)
    
    def unequip_badge(self, badge):
        return self.inventory.unequip_badge(self.user_id, badge)
    
    def get_user_badge(self, badge):
        return self.inventory.get_user_badge(self.user_id, badge)
    
    def purge_user_badge(self, badge):
        return self.inventory.purge_user_badge(self.user_id, badge)
    
    def set_level(self, level):
        return self.db.set_level(self.user_id, level)
    
    def set_experience(self, exp):
        return self.db.set_experience(self.user_id, exp)
    
    def set_warnings(self, warnings):
        return self.db.set_warnings(self.user_id, warnings)
