import os

from accounts.models import User

num_of_dummies = 2
base_number = 9000000000
cur_path = os.getcwd()
file_path = os.path.join(cur_path, "CI", "dummies.csv")
print(file_path, cur_path)


with open(file_path, "a") as f:
    for i in range(num_of_dummies):
        new_user = User.objects.create(
            username=f"{base_number + i}",
        )
        new_user.set_password("shrestha")
        new_user.save()
        # user activation is automatic
        # write the user details in csv file
        f.write(f"{new_user.username},shrestha")
        f.write("\n")
        # write in new line


# # create user
# user = User.objects.create(
#     username="9840000000",
#     password="shrestha")
