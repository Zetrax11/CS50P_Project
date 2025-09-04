from my_classes import MainWindow
import sys
import json
import os
import getpass
from PyQt5.QtWidgets import QApplication


def save_file(path, expenses):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(expenses, f, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Failed to save a file {e}" 
    
def load_expenses(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return f"Failed to load a file"

def log_in():
    count = 0
    while count < 3:
        username = input("username: ").lower().strip()
        password = getpass.getpass()
        with open("users.txt", "r") as f:
            for line in f.readlines():
                user, passw = line.strip().split("|")
                if username == user and password == passw:
                    return username
        print(f"Invalid credentials {count+1} time")
        count += 1
    return False

def main():
    user = log_in()
    if user:
        json_file = f"expenses_{user}.json"

        app = QApplication(sys.argv)
        expenses = load_expenses(json_file)
        window = MainWindow(init_expenses=expenses)
        window.show()
        
        ret = app.exec_()
        save_file(json_file, window.get_expenses())
        sys.exit(ret)
    else:
        sys.exit()

if __name__ == "__main__":
    main()