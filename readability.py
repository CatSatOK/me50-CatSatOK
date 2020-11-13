from cs50 import get_string

#get input
text = get_string("Text: \n")

letters = sentances = words = 0

#count letters
for char in text:
    if char.isalpha():
        letters += 1

#count words
words = len(text.split())

#count sentances
sentances = text.count(".") + text.count("!") + text.count("?")

#find L and S
L = (float(letters) / float(words)) * 100
S = (float(sentances) / float(words)) * 100

#work out grade
grade = int(round(0.0588 * L - 0.296 * S - 15.8))

#print grade, or qualifiers for -1st and 16+
if grade < 1:
    print("Before Grade 1\n")
elif grade >= 16:
    print("Grade 16+\n")
else:
    print(f"Grade, {grade}")
