from db import db_inventory

class Item:
    def __init__(self, item_id):
        self.id = item_id
        self.db = db_inventory.DB_Inventory()
    
    @property
    def exists(self):
        return self.db.item_exist(self.id)
    
    @property
    def name(self):
        return self.db.get_item(self.id)[0][2]
    
    @property
    def kind(self):
        return self.db.get_item(self.id)[0][1]
    
    @property
    def cost(self):
        return self.db.get_item(self.id)[0][3]
    
    @property
    def key(self):
        return self.db.get_item(self.id)[0][4]