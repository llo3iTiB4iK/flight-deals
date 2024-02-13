import sheety

print("Welcome to Ivan's Flight Club.\nWe find the best flight deals and email them to you.")
first_name = input("What is your first name?\n")
last_name = input("What is your last name?\n")
email = input("What is your email?\n")
if email == input("Type your email again to confirm.\n"):
    sheety.add_new_user(first_name, last_name, email)
    print("You're in the club!")
else:
    print("Emails do not match!")
