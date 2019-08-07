from db import db_hfuncts

class DB_Inventory(db_hfuncts.DB_Helpers):
    def __init__(self):
        self.db_directory = "db/data/inventory.db"
    
    def get_background(self, user_id):
        try:
            fetched = self.fetch_row(
                "inventory",
                owner_id=user_id,
                is_equipped=True,
            )

            if len(fetched) == 0:
                return None
            
            bg_id = fetched[0][1]

            bg = self.fetch_row(
                "items",
                item_id=bg_id
            )

            return bg[0][0]
        except Exception as e:
            print(e)
    
    def put_background(self, user_id, item_id):
        try:
            self.append_row(
                "inventory",
                owner_id=user_id,
                item_id=item_id,
                is_equipped=False,
            )
        except Exception as e:
            print(e)
    
    def get_user_item(self, user_id, item_id):
        try:
            fetched = self.fetch_row(
                "inventory",
                owner_id=user_id,
                item_id=item_id
            )

            return fetched
        except Exception as e:
            print(e)
    
    def get_user_badge(self, user_id, item_id):
        try:
            fetched = self.fetch_row(
                "badges",
                owner_id=user_id,
                badge_id=item_id
            )

            return fetched
        except Exception as e:
            print(e)
    
    def get_item(self, item_id):
        try:
            fetched = self.fetch_row(
                "items",
                item_id=item_id
            )

            return fetched
        except Exception as e:
            print(e)
    
    def equip_item(self, user_id, item_id):
        try:
            self.update_data(
                "inventory",
                "is_equipped",
                True,
                owner_id=user_id,
                item_id=item_id
            )

            return True
        except Exception as e:
            print(e)
    
    def unequip_item(self, user_id, item_id):
        try:
            self.update_data(
                "inventory",
                "is_equipped",
                False,
                owner_id=user_id,
                item_id=item_id
            )

            return True
        except Exception as e:
            print(e)
    
    def get_user_items(self, user_id):
        try:
            fetched = self.fetch_row(
                "inventory",
                owner_id=user_id
            )

            item_ids = []
            user_items = []

            for i in fetched:
                item_ids.append(i[1]) 
            
            badges = self.fetch_row(
                "badges",
                owner_id=user_id
            )

            for x in badges:
                item_ids.append(x[1])
            
            return item_ids  
        except Exception as e:
            print(e)

    def delete_user_item(self, user_id, item_id):
        try:
            self.purge_row(
                "inventory",
                owner_id=user_id,
                item_id=item_id
            )
        except Exception as e:
            print(e)
    
    def item_exist(self, item_id):
        try:
            item = self.get_item(item_id)
            if len(item) == 0:
                return False
            else:
                return True
        except Exception as e:
            print(e)
    
    def equipped_badge(self, user_id):
        try:
            fetched = self.fetch_row(
                "badges",
                owner_id=user_id,
                is_equipped=1
            )
            if len(fetched) == 0:
                return None
            else:
                return fetched[0][1]
        except Exception as e:
            print(e)
    
    def equip_badge(self, user_id, item_id):
        try:
            self.update_data(
                "badges",
                "is_equipped",
                True,
                owner_id=user_id,
                badge_id=item_id
            )

            return True
        except Exception as e:
            print(e)
    
    def unequip_badge(self, user_id, item_id):
        try:
            self.update_data(
                "badges",
                "is_equipped",
                False,
                owner_id=user_id,
                badge_id=item_id
            )

            return True
        except Exception as e:
            print(e)
    
    def store_badge(self, user_id, item_id):
        try:
            self.append_row(
                "badges",
                owner_id=user_id,
                badge_id=item_id,
                is_equipped=False,
            )
        except Exception as e:
            print(e)
    
    def purge_user_badge(self, user_id, item_id):
        try:
            self.purge_row(
                "badges",
                owner_id=user_id,
                badge_id=item_id
            )
        except Exception as e:
            print(e)
    
    def user_badges(self, user_id):
        try:
            fetched = self.fetch_row(
                "badges",
                owner_id=user_id,
            )
            if len(fetched) == 0:
                return None
            else:
                badges = []
                for badge in fetched:
                    badges.append(badge[1])
                
                return badges
        except Exception as e:
            print(e)