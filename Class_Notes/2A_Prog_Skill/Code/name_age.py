import re
while 1:
    username = input("Please input your name: ")
    if re.search("[^a-zA-Z ]", username):
        print("Please remove those special characters")
    else:
        break
print("Hello, %s"%username)

import dateutil.parser
import datetime
import dateutil.relativedelta
while 1:
    userdob = input("Please input your date of birth: ")
    try:
        dob_parsed = dateutil.parser.parse(userdob)
    except:
        print("Your date information could not be parsed")
        continue
    today = datetime.datetime.today()
    age = dateutil.relativedelta.relativedelta(today, dob_parsed)
    print("Your current age is: %s years, %s months, %s days"%(age.years, age.months, age.days))
    time_to_100 = (dateutil.relativedelta.relativedelta(years=+100) - age)
    print("You will turn 100 years old in %s years, %s months, %s days"%(time_to_100.years, time_to_100.months, time_to_100.days))
    break

