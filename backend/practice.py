# a = [
#     {"id": 1, "UserName": "test_user"},
#     {"id": 2, "UserName": "test_user2"},
#     {"id": 3, "UserName": "test_user3"},
#     {"id": 4, "UserName": "test_user4"},
#     {"id": 5, "UserName": "test_user5"},
#     {"id": 6, "UserName": "test_user6"},
#     {"id": 7, "UserName": "test_user7"},
#     {"id": 8, "UserName": "test_user8"},
#     {"id": 9, "UserName": "test_user9"},
#     {"id": 10, "UserName": "test_user10"},
# ]

sort = [(user["id"], -1) for user in a]
print(sort)

try:
    num1 = int(input("Enter a number: "))
    num2 = int(input("Enter a number to divide by: "))
    result = num1 / num2
    print("Result:", result)
except ZeroDivisionError:
    print("Error: You can't divide by zero!")
except ValueError:
    print("Error: Please enter valid numbers.")


# class usercart:
#     def __init__(self):
#         self.cart = []
#         for i in range(self.cart.append(0), 5):
#             item = input("Enter the item you want to add: ")
#             self.add_item(item)

#     def add_item(self, item):
#         self.cart.append(item)
#         if self.cart > 5:
#             print("You have added 5 items to your cart.")
#         else:
#             print("You have added an item to your cart.")


# print("Welcome to the shopping cart!")
# cart = usercart()


a = ["a", "b", "c", "d", "e"]

print(len.a[1])
