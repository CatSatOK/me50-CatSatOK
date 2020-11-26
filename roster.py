import cs50
from sys import argv

if len(argv) !=2:
    print('Usage: python roster.py [NAME OF HOUSE]')
    exit(1)

db = cs50.SQL("sqlite:///students.db")
rows = db.execute('SELECT * FROM students WHERE house = ? ORDER BY last, first', argv[-1])

for row in rows:
    #format
    if row['middle'] is None:
        print(row['first'] + ' ' + row['last'] + ', born' + str(row['birth']))
    else:
        print(row['first'] + ' ' + row['middle'] + ' ' + row['last'] + ', born' + str(row['birth']))

