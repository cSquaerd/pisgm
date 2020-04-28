from pathlib import Path
import json, os, requests, time

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
SAVE_PATH = MODULE_DIR + "/user.json"

class User:
    def __init__(self, id, public_key, private_key, group):
        self.id = id
        self.public_key = public_key
        self.private_key = private_key
        self.group = group

def json_to_user(data):
    id = int(data["id"]);
    uk = data["public_key"]
    rk = data["private_key"]
    group = int(data["group"])
    return User(id, uk, rk, group)

def new_user():
    ## TODO: Right now this is test data, eventually this should communicate
    ## with the server to register a new user.
    ukey_path = Path(MODULE_DIR + "/../server/testingData/8270950596653088861-U.pem")
    rkey_path = Path(MODULE_DIR + "/../server/testingData/8270950596653088861-R.pem")
    data = {"id": "8270950596653088861", \
            "group": "3911253593270387734", \
            "public_key": ukey_path.read_text(), \
            "private_key": rkey_path.read_text() }
    
    ## TODO: Don't save user to local storage until we have "new user"
    ## functionality in server working.
    #fout = open(SAVE_PATH, "w")
    #json.dump(data)
    #fout.close()
    
    return json_to_user(data)

def main():
    ## Initialize user.
    user = None
    if (os.path.exists(SAVE_PATH)):
        fin = open(SAVE_PATH, "r")
        try:
            data = json.load(fin)
        except json.JSONDecodeError:
            user = new_user();
        else:
            if "id" in data and  "public_key" in data and \
               "private_key" in data and "group" in data:
                try:
                    user = json_to_user(data)
                except ValueError:
                    user = new_user()
            else:
                user = new_user()
        fin.close()
    else:
        user = new_user()

    print(user.id)
    print("\n")
    print(user.public_key)
    print("\n")
    print(user.private_key)
    print("\n")
    print(user.group)
    print("\n")

if __name__ == "__main__":
    main()
