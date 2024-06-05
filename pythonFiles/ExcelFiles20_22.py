import random
from faker import Faker
from unidecode import unidecode

fake = Faker('pl_PL')

#Excel sheet1
address = ["Gdansk", "Gdynia", "Sopot", "Wejherowo", "Straszyn"]
employee = 1
cooks_cloakroom_staff = 1
idSubject = 1
Excel = []
emp_id = ""
with open("excel/Excel1_20_22.txt", "w+", encoding="UTF-8") as file:
    while employee < 58:
        pesel_number = ''.join([str(random.randint(0, 9)) for _ in range(11)])

        if random.randint(0,2)%2==0:
            name = unidecode(fake.first_name_male())
            gender = "male"
        else:
            name = unidecode(fake.first_name_female())
            gender = "female"
        
        surname = unidecode(fake.unique.last_name())
        street = unidecode(fake.street_address())
        city = random.choice(address)
        postcode = fake.postalcode()
        phonenumber = ''.join([str(random.randint(0, 9)) for _ in range(9)])
        email = str(emp_id) + "@school.com"
        date_of_employment = fake.date_between(start_date='-7y', end_date='-5y')
        date_of_dissmisal= ""

        if employee <= 48: position = "teacher"
        elif employee <= 54: position = "cook"
        elif employee <= 57: position = "cloakroom staff"
        elif employee <= 62: position = "cleaner"
        elif employee <= 63: position = "director"
        elif employee <= 65: position = "psychologist"
        elif employee <= 67: position = "nurse"
        elif employee <= 70: position = "school caretaker"

        if position == "teacher":
            if idSubject <= 5: emp_id = fake.numerify('e####m') #mathematic
            elif idSubject <=10: emp_id = fake.numerify('e####o') #polish
            elif idSubject <=15: emp_id = fake.numerify('e####e') #english
            elif idSubject <=20: emp_id = fake.numerify('e####s') #science
            elif idSubject <=25: emp_id = fake.numerify('e####g') #german
            elif idSubject <=30: emp_id = fake.numerify('e####w') #wos
            elif idSubject <=35: emp_id = fake.numerify('e####h') #history
            elif idSubject <=40: emp_id = fake.numerify('e####p') #pe
            elif idSubject <=45: emp_id = fake.numerify('e####i') #it
            elif idSubject <=46: emp_id = fake.numerify('e####m') #music
            elif idSubject <=47: emp_id = fake.numerify('e####a') #art
            elif idSubject <=48: emp_id = fake.numerify('e####r') #religion

            idSubject+=1
        else:
            emp_id = fake.numerify('e#####')

        row = (str(pesel_number) + "|" + str(emp_id) + "|" + str(name) + "|" + str(surname) + "|" + 
            str(gender) + "|" + str(position) + "|" + str(street) + "|" + str(city) + "|" + str(postcode) + "|" + 
            str(phonenumber) + "|" + str(email) + "|" + str(date_of_employment) + "|" + str(date_of_dissmisal))
        Excel.append(row)

        employee += 1
    x = ('\n'.join(Excel))
    file.write(x)


#Excel sheet2
address = ["Gdansk", "Gdynia", "Sopot", "Wejherowo", "Straszyn", "Bogatka", "Borkowo"]
students = 1
classID=1
Excel2 = []
entityStudent = []
dateOfBirth = ""
listOfStID = []

with open("excel/Excel2_20_22.txt", "w+", encoding="UTF-8") as file:
    while students <= 432:
        pesel_number = ''.join([str(random.randint(0, 9)) for _ in range(11)])
        stu_id = fake.numerify('s#####')
        while stu_id in listOfStID:
            stu_id = fake.numerify('s#####')
        listOfStID.append(stu_id)

        if random.randint(0,2)%2==0:
            name = unidecode(fake.first_name_male())
            gender = "male"
        else:
            name = unidecode(fake.first_name_female())
            gender = "female"
            
        surname = unidecode(fake.unique.last_name())
        
        if students<73: dateOfBirth = fake.date_of_birth(minimum_age=13, maximum_age=13)
        elif students<145: dateOfBirth = fake.date_of_birth(minimum_age=14, maximum_age=14)
        elif students<217: dateOfBirth = fake.date_of_birth(minimum_age=15, maximum_age=15)
        elif students<289: dateOfBirth = fake.date_of_birth(minimum_age=16, maximum_age=16)
        elif students<361: dateOfBirth =fake.date_of_birth(minimum_age=17, maximum_age=17)
        elif students<433: dateOfBirth = fake.date_of_birth(minimum_age=12, maximum_age=12)


        placeOfBirth = unidecode(fake.city())
        street = unidecode(fake.street_address())
        city = random.choice(address)

        if city==address[4] or city==address[5] or city==address[6]:
            placeOfLiv = "countryside"
        else:
            placeOfLiv = "city"

        postcode = fake.postalcode()
        parentPhonenumber = ''.join([str(random.randint(0, 9)) for _ in range(9)])
        parentEmail = fake.email()

        row = (str(pesel_number) + "|" + str(stu_id) + "|" + str(name) + "|" + str(surname) + "|" + str(dateOfBirth) + "|" + str(placeOfBirth) + 
            "|" + str(gender) + "|"  + str(street) + "|" + str(city) + "|" + str(postcode) + "|" + str(placeOfLiv) + 
            "|" + str(parentPhonenumber) + "|" + str(parentEmail))
        Excel2.append(row)

        students += 1
    z = ('\n'.join(Excel2))
    file.write(z)