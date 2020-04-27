from tkinter import *
import json, os, requests, time

SAVE_PATH = os.path.dirname(os.path.realpath(__file__)) + "/user.json"

class User:
    id = None
    public_key = None
    private_key = None
    ## TODO: More fields? Should the user have a local
    ## record of what groups he's in?
    def __init__(self, id, public_key, privat_key):
        self.id = id
        self.public_key = public_key
        self.private_key = private_key

def new_user():
    data = {'name': 'hello', 'value': 'world'}
    ## TODO: Request new user from server.
    fout = open(SAVE_PATH, "w")
    ##json.dump(data)
    fout.close()
    return data

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
            if "id" in data and "public_key" in data and "private_key" in data:
                user = User(data["in"], data["public_key"], data["private_key"])
            else:
                user = new_user()
        fin.close()
    else:
        user = new_user()

    ## Initialize window.
    window = Tk()
    #window.mainloop()

if __name__ == "__main__":
    main()
