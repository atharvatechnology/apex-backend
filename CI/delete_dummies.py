import os

from accounts.models import User

cur_path = os.getcwd()
file_path = os.path.join(cur_path, "CI", "dummies.csv")

with open(file_path, "r") as f:
    for line in f:
        username, password = line.split(",")
        user = User.objects.get(username=username)
        user.delete()
# delete the file
os.remove(file_path)
