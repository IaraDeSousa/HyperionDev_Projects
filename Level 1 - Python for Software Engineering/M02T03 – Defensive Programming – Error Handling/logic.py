# Program to find out the average age of three friends. 

friend_one = int(input("What is your first friend's age?"))
friend_two = int(input("What is your second friend's age?"))
friend_three = int(input("What is your third friend's age?"))

average_age = friend_one + friend_two + friend_three / 3 # This is a logical error as it only divides the third friend's age, not all friend's ages together.

print(f"Your friends' average ages is {average_age}!")