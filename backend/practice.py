# li = [
#     "shashank",
#     "kishan",
#     "saurabh",
#     "siddharth",
#     "prashant",
#     "sachin",
#     "shubham",
#     "ankit",
#     "abhishek",
#     "ankit",
#     "abhishek",
# ]

# for i in li:
#     if i == "kishan":
#         print(f"found", "You Searched :", i, "in list", "at index", li.index(i))
#         break
# else:
#     print("not found", li)


# def Calculater():
#     productname = str(input("Enter ProductName :"))
#     quantity = int(input("Enter quantity :"))
#     price = int(input("Enter price :"))
#     billamount = quantity * price
#     discount_percent = 0

#     if billamount <= 1000:
#         print(
#             f"you are not eligible for discount because your billamount is {billamount}"
#         )

#     elif 1000 < billamount <= 5000:
#         discount_percent = 20
#         print(f"you are only eligible for 20% because your billamount is {billamount}")

#     elif 5000 < billamount <= 10000:
#         discount_percent = 35
#         print(f"you are only eligible for 35% because your billamount is {billamount}")

#     elif billamount > 10000:
#         discount_percent = 50
#         print(f"you are only eligible for 50% because your billamount is {billamount}")

#     else:
#         print("You are not eligible for discount")

#     discount_amount = billamount * discount_percent / 100
#     final_amount = billamount - discount_amount

#     print(
#         f"{productname} your Product Name, {billamount} is your bill amount",
#         "Your Discount Amount is :",
#         {discount_amount},
#         "Your Final Amount is :",
#         {final_amount},
#     )

#     return Calculater()


# Calculater()


# def rajesh(n):
#     if n == 0 or n == 1:
#         return 1
#     else:
#         return n * rajesh(n - 1)


# result = rajesh(n=5)

# print(result)


def rajesh(n):
    if n < 10 or n < 0:
        return "Your discount percent is 10%"

    elif n >= 10 and n < 50:
        return "Your discount percent is 50%"

    else:
        return "Your discount percent is 80%"

    return rajesh


price = int(input("Enter the price of the product: "))
discount = rajesh(price)

print(f"The discount on the product is: {discount}")
