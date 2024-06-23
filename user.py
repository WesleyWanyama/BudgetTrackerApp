import csv
import hashlib

class User:
    def __init__(self, username, password, income):
        self.username = username
        self.password = self.hash_password(password)
        self.income = income

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        return self.hash_password(password) == self.password

    def __repr__(self):
        return f"<User: {self.username}, Income: ${self.income:.2f}>"

def register_user(username, password, income, user_file_path="users.csv"):
    with open(user_file_path, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([username, hashlib.sha256(password.encode()).hexdigest(), income])

def login_user(username, password, user_file_path="users.csv"):
    with open(user_file_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            stored_username, stored_password, stored_income = row
            if stored_username == username and hashlib.sha256(password.encode()).hexdigest() == stored_password:
                return User(username, password, float(stored_income))
    return None
