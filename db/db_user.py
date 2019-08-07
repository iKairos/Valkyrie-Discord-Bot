from db import db_hfuncts
from settings import *

class DB_User(db_hfuncts.DB_Helpers):
    def __init__(self):
        self.db_directory = "db/data/users.db"
        self.configs = Configs()
    
    def register_user(self, user_id):
        try:
            self.append_row(
                "users",
                user_id=user_id,
                money=self.configs.BASE_MONEY,
                experience=self.configs.BASE_EXP,
                level=self.configs.BASE_LEVEL,
                reputation=self.configs.BASE_REP
            )

            self.append_row(
                "userconfigs",
                user_id=user_id,
                toggle_exp=True,
                toggle_inter=True,
                total_warnings=0
            )

            return True
        except:
            return False
     
    def is_registered(self, user_id):
        try:
            fetched = self.fetch_row(
                "users",
                user_id=user_id
            )

            fetched2 = self.fetch_row(
                "userconfigs",
                user_id=user_id
            )

            if len(fetched) == 0 and len(fetched2) == 0:
                return False
            
            return True
        except:
            return False

    def get_money(self, user_id):
        try:
            fetched = self.fetch_row(
                "users",
                user_id=user_id,
            )

            money = fetched[0][1]
            return money
        except:
            return False
    
    def get_experience(self, user_id):
        try:
            fetched = self.fetch_row(
                "users",
                user_id=user_id,
            )

            exp = fetched[0][2]
            return exp
        except:
            return False
    
    def get_level(self, user_id):
        try:
            fetched = self.fetch_row(
                "users",
                user_id=user_id,
            )

            lvl = fetched[0][3]
            return lvl
        except:
            return False
    
    def get_reputation(self, user_id):
        try:
            fetched = self.fetch_row(
                "users",
                user_id=user_id,
            )

            rep = fetched[0][4]
            return rep
        except:
            return False
    
    def get_warnings(self, user_id):
        try:
            fetched = self.fetch_row(
                "userconfigs",
                user_id=user_id
            )

            warnings = fetched[0][3]
            return warnings
        except:
            return False
    
    def add_money(self, user_id, value):
        try:
            current = self.get_money(user_id)
            new = current + value
        except:
            return False

        self.update_data(
            "users",
            "money",
            new,
            user_id=user_id
        )

        return True

    def add_experience(self, user_id, value):
        try:
            current = self.get_experience(user_id)
            new = current + value
        except:
            return False
        
        self.update_data(
            "users",
            "experience",
            new,
            user_id=user_id
        )

        return True
    
    def level_up(self, user_id):
        try:
            current = self.get_level(user_id)
            new = current + 1
        except:
            return False
        
        self.update_data(
            "users",
            "level",
            new,
            user_id=user_id
        )

        return True
    
    def add_reputation(self, user_id):
        try:
            current = self.get_reputation(user_id)
            new = current + 1
        except:
            return False
        
        self.update_data(
            "users",
            "reputation",
            new,
            user_id=user_id
        )

        return True
    
    def add_warning(self, user_id):
        try:
            current = self.get_warnings(user_id)
            new = current + 1
        except:
            return False
        
        self.update_data(
            "userconfigs",
            "total_warnings",
            new,
            user_id=user_id
        )

        return True
    
    def toggle_exp(self, user_id, option):
        try:
            self.update_data(
                "userconfigs",
                "toggle_exp",
                option,
                user_id=user_id
            )

            return True
        except:
            return False
    
    def toggle_inter(self, user_id, option):
        try:
            self.update_data(
                "userconfigs",
                "toggle_inter",
                option,
                user_id=user_id
            )

            return True
        except:
            return False
    
    def is_exp_toggled(self, user_id):
        try:
            fetched = self.fetch_row(
                "userconfigs",
                user_id=user_id
            )

            if fetched[0][1] == 0:
                return False
            else:
                return True
        except:
            return False
    
    def is_interact_toggled(self, user_id):
        try:
            fetched = self.fetch_row(
                "userconfigs",
                user_id=user_id
            )

            if fetched[0][2] == 0:
                return False
            else:
                return True
        except:
            return False
    
    def get_about(self, user_id):
        try:
            fetched = self.fetch_row(
                "users",
                user_id=user_id
            )
            
            if fetched[0][5] is None:
                return ""
            else:
                return fetched[0][5]
        except:
            return False
        
    def set_about(self, user_id, string):
        try:
            self.update_data(
                "users",
                "about",
                string,
                user_id=user_id
            )

            return True
        except:
            return False
    
    def set_level(self, user_id, level):
        try:
            self.update_data(
                "users",
                "level",
                level,
                user_id=user_id
            )

            return True
        except:
            return False
    
    def set_experience(self, user_id, exp):
        try:
            self.update_data(
                "users",
                "experience",
                exp,
                user_id=user_id
            )

            return True
        except:
            return False
    
    def set_warnings(self, user_id, number):
        try:
            self.update_data(
                "userconfigs",
                "total_warnings",
                number,
                user_id=user_id
            )

            return True
        except:
            return False