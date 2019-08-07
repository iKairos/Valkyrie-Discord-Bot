import sqlite3 as sql
from db_hfuncts import DB_Helpers

channel_str = "CREATE TABLE IF NOT EXISTS channels(channel_id TEXT, is_nsfw BOOLEAN, persistence INTEGER DEFAULT 0)"

user_str = "CREATE TABLE IF NOT EXISTS users(user_id TEXT, money INTEGER, experience INTEGER DEFAULT 0, level INTEGER DEFAULT 0, reputation INTEGER DEFAULT 0)"

inventory_str = "CREATE TABLE IF NOT EXISTS inventory(owner_id TEXT, item_id TEXT, is_equipped BOOLEAN)"

userconfigs_str = "CREATE TABLE IF NOT EXISTS userconfigs(user_id TEXT, toggle_exp BOOLEAN, toggle_inter BOOLEAN, total_warnings INTEGER DEFAULT 0)"

mainconfigs_str = "CREATE TABLE IF NOT EXISTS mainconfigs(server_id TEXT, log_activities BOOLEAN DEFAULT 0, log_sanctions BOOLEAN DEFAULT 0, strict_nrt BOOLEAN DEFAULT 0, mute_role TEXT, logging_channel TEXT)"

database_fragments = ["channels", "users", "inventory", "userconfigs", "mainconfigs"]

def spawn_database():
    for fragment in database_fragments:
        if fragment == "channels":
            directory = "data/channels.db"
            runner = channel_str
        elif fragment == "users":
            directory = "data/users.db"
            runner = user_str
        elif fragment == "inventory":
            directory = "data/inventory.db"
            runner = inventory_str
        elif fragment == "userconfigs":
            directory = "data/users.db"
            runner = userconfigs_str
        elif fragment == "mainconfigs":
            directory = "data/mainconfigs.db"
            runner = mainconfigs_str

        helpers = DB_Helpers(directory)
        connection = helpers.connect()
        if connection is not None:
            helpers.spawn_table(runner)
            print(f"Successful creation of {fragment}.")
        else:
            print("Error! cannot create the database connection.")
            break
        

if __name__ == '__main__':
    spawn_database()
