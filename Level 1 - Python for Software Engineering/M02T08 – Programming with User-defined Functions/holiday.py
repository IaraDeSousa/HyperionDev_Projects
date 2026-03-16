# Defining the three functions to get the hotel cost, plane cost and car rental cost.
def hotel_cost(nights):
    total = nights * 50
    return total


def plane_cost(city):
    if city == "barcelona":
        total = 150
        return total
    elif city == "madeira":
        total = 200
        return total
    elif city == "lima":
        total = 600
        return total
    else:
        print(
            "Please enter one of the three destinations.")


def car_rental(days):
    total = days * 25
    return total


# Defining the function to get the total holiday cost.
def holiday_cost(
        flight_total, rental_total, hotel_total):
    total_cost = flight_total + rental_total + hotel_total
    return total_cost


# Taking the user's inputs about their holidays.
city_flight = input(
    'What city will you be flying to?\nBarcelona\nMadeira\nLima')
# Using lowercase for the input to avoid errors.
city_flight = city_flight.lower()
num_nights = int(
    input(
        "How many nights will you be staying at the hotel?"))
rental_days = int(
    input("How many days will you be hiring a car?"))


# Creating variables to storage each total.
flight_total = plane_cost(city_flight)
hotel_total = hotel_cost(num_nights)
rental_total = car_rental(rental_days)


# Printing the full holiday information in a readable way.
print(
    f"Your holiday will cost" 
    f"£{holiday_cost(flight_total, rental_total, hotel_total)}"
    f" in total.\nThe hotel cost will be £{hotel_total}."
    f"\nThe plane cost will be £{flight_total}."
    f"\nThe car_rental will be £{rental_total}.")
