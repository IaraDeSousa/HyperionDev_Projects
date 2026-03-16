menu = ['latte', 'cappucino', 'croissant', 'muffin']
stock = {'latte': 20, 'cappucino': 30, 'croissant': 5, 'muffin': 2}
price = {'latte': 3.50, 'cappucino': 4.00, 'croissant': 3.00, 'muffin': 3.50}

total_stock = 0
for item in menu: 
    item_value = stock[item] * price[item]
    total_stock += item_value

print(total_stock)
