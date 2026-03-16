# Triathlon award program

swimming_time = int(input("What was your swimming time in minutes?"))
cycling_time = int(input("What was your cycling time in minutes?"))
running_time = int(input("What was your running time in minutes?"))

triathlon_time = swimming_time + cycling_time + running_time
print(f"Total time taken for the triathlon: {triathlon_time} minutes")

if triathlon_time <= 100: 
    print("You will receive the pronvincial colours award")
elif (triathlon_time >= 101) and (triathlon_time <= 105):
    print("You will receive the pronvincial half colours award")
elif (triathlon_time >= 106) and (triathlon_time <= 110):
    print("You will receive the pronvincial scroll award")
else: 
    print("You do not receive any award")
