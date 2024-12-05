import random
from faker import Faker
from datetime import datetime
from unidecode import unidecode

fake = Faker('pl_PL')

#Excel sheet1
address = ["Gdansk", "Gdynia", "Sopot", "Wejherowo", "Straszyn"]
employee = 1
cooks_cloakroom_staff = 1
idSubject = 1
Excel = []
emp_id = ""
newList2=[]
    

with open("excel/Excel1_22_23.txt", "w+", encoding="UTF-8") as file:
    while employee <= 10:
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

        start_date = datetime(2022, 1, 1)
        end_date = datetime(2022, 8, 31)
        date_of_employment =fake.date_between_dates(date_start=start_date, date_end=end_date)
        date_of_dissmisal= ""

        if employee <= 5: position = "teacher"
        elif employee == 6: position = "cook"
        elif employee == 7: position = "cloakroom staff"
        elif employee == 8: position = "cleaner"
        elif employee == 9: position = "psychologist"
        elif employee == 10: position = "school caretaker"

        if position == "teacher":
            if idSubject == 1: emp_id = fake.numerify('e####m') #mathematic
            elif idSubject ==2: emp_id = fake.numerify('e####o') #polish
            elif idSubject ==3: emp_id = fake.numerify('e####e') #english
            elif idSubject ==4: emp_id = fake.numerify('e####w') #wos
            elif idSubject ==5: emp_id = fake.numerify('e####p') #pe

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
studID=[]
with open("excel/Excel2_22_23.txt", "w+", encoding="UTF-8") as file:
    while students <= 72 :
        pesel_number = ''.join([str(random.randint(0, 9)) for _ in range(11)])
        stu_id = fake.numerify('s#####')

        with open("excel/Excel2_20_22.txt") as file2:
            while stu_id in file2.read() or stu_id in studID:
                stu_id = fake.numerify('s#####')
            
            studID.append(stu_id)
                    

        if random.randint(0,2)%2==0:
            name = unidecode(fake.first_name_male())
            gender = "male"
        else:
            name = unidecode(fake.first_name_female())
            gender = "female"
            
        surname = unidecode(fake.unique.last_name())
        dateOfBirth = fake.date_of_birth(minimum_age=11, maximum_age=11) 
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