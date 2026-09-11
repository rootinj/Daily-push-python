print("Welcome To My Expense Tracker")
expenses = [
            {"Description": "Coffee", "Amount": 100},
            {"Description": "Burger", "Amount": 200},
            {"Description": "Cold Dring", "Amount": 50},
            {"Description": "Hot Cake", "Amount": 210}
]
total = 0
item_name = (input("Enter your item name here: "))
item_amount = int(input("Enter your item's value here: "))

new_expenses = {"Description": item_name, "Amount": item_amount}
expenses.append(new_expenses)

for expense in expenses:
    print(expense["Description"], expense["Amount"])
    total = total +expense["Amount"]
print("Total", total)