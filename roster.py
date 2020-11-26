import cs50
from sys import argv

if len(argv) !=2:
    print('Usage: python roster.py [NAME OF HOUSE]')
    exit(1)

db = cs50.SQL("sqlite:///students.db")
rows = db.execute('SELECT * FROM students WHERE house = ? ORDER BY last, first', argv[-1])

for row in rows:
    #format
    print(row['first'] + '' + (row['middle'] + '' if row['middle'] else '') + row['last'] + ', born' + str(row['birth']))
