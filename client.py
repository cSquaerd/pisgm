from pathlib import Path
from core import *
from PIL import Image
import json, os, sys

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
    test_dir = MODULE_DIR + "/server/testingData"
    ukey_path = Path(test_dir + "/8270950596653088861-U.pem")
    rkey_path = Path(test_dir + "/8270950596653088861-R.pem")
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

def print_prog():
    print(sys.argv[0], end = "")

def print_usage():
    print_prog()
    print(" -h")
    print("    shows this help message")
    print_prog()
    print(" -e <text> <path>")
    print("    encrypts <text>, stores result in <path>")
    print_prog()
    print(" -e <path>")
    print("    encrypts text from stdin, stores result in <path>")
    print_prog()
    print(" -d <path>")
    print("    decrypts image at <path>, prints result to stdout")

def encrypt(user, text, img_path):
    rkey = rsa.privateKey(user.private_key.encode())
    reply = makeRequest(rkey, user.id, user.group)
    img = makeImage(text, user.id, reply)
    img.save(img_path)

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

    ## Dispatch based on command-line arguments.
    args = sys.argv
    if len(args) == 1 or args[1] == "-h" or args[1] == "--help":
        print("Usage:")
        print_usage()
    elif len(args) == 4 and args[1] == "-e":
        text = args[2]
        img_path = args[3]
        encrypt(user, text, img_path)
    elif len(args) == 3 and args[1] == "-e":
        text = "\n".join(sys.stdin.readlines())
        img_path = args[2]
        encrypt(user, text, img_path)
    elif len(args) == 3 and args[1] == "-d":
        img_path = args[2]
        img = Image.open(img_path)
        rkey = rsa.privateKey(user.private_key.encode())
        text = decodeImage(img, rkey, user.id, user.group)
        print(text)
    else:
        print("Usage:")
        print_usage()

if __name__ == "__main__":
    main()
