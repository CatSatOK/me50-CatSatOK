from cs50 import get_float

#get positive change amount
while True:
    dollars = get_float("How much change is due?\n")
    if dollars > 0:
        break

#round dollars to cents
cents = int(dollars*100)

#use largest coins first
quarters = cents // 25
a = cents % 25

dimes = a // 10
b = a % 10

nickles = b // 5
c = b % 5

pennies = c // 1
d = c % 1

#keep track of coins used
coins = quarters + dimes + nickles + pennies

#print number of coins
print(coins)
