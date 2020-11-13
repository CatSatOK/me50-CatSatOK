from cs50 import get_int

#get positive int 1-8
#ask agin if not pos or over 8
while True:
    answer = get_int("Height:\n")
    if answer > 0 and answer < 9:
        break

#make and allign pyramid
for row in range(1, answer +1):
    print(" " * (answer - row) + "#" * row)


