import random
from faker import Faker
import ExcelFiles22_23
import sqlData20_22
from datetime import datetime
from dateFiles import date22_23 
fake = Faker('pl_PL')

#Teachers
myList = []
TEACHER = []
with open("data22_23_bulk/teachers22_23.bulk", "w+", encoding="UTF-8") as file:
    myList = [item.split("|") for item in ExcelFiles22_23.Excel]

    id=0
    for i in myList:
        if myList[id][5]=="teacher":
            dataEntity = (str(myList[id][1]) + "|" + myList[id][2] + "|" + myList[id][3] + "|" + myList[id][0])
            TEACHER.append(dataEntity)
        id+=1
    
    t = ('\n'.join(TEACHER))
    file.write(t)


#Students
myList = []
STUDENTS = []
with open("data22_23_bulk/students22_23.bulk", "w+", encoding="UTF-8") as file:
    myList = [item.split("|") for item in ExcelFiles22_23.Excel2]

    id=0
    classID=sqlData20_22.classIDstud
    for i in myList:
        dataEntity = (str(myList[id][1]) + "|" + myList[id][2] + "|" + myList[id][3] + "|" + myList[id][0] + "|" + str(classID))
        STUDENTS.append(dataEntity)
        
        if (id+1)%24==0 : classID+=1
        id+=1
    
    t = ('\n'.join(STUDENTS))
    file.write(t)


#Classes
CLASSES = []
with open("data22_23_bulk/classes22_23.bulk", "w+", encoding="UTF-8") as file:
    letter = ["A","B","C"]
    
    yearOfStart = sqlData20_22.yearOfStart
    numOfNewClasses = 1 # in 22/23 3 additional 4th grade -> which is one level
    for i in range(numOfNewClasses):
        letterID = 0
        for j in range(3):
            row = ("|" + str(yearOfStart) + "|" + str(letter[letterID]))
            CLASSES.append(row)
            letterID+=1
        yearOfStart += 1

    t = ('\n'.join(CLASSES))
    file.write(t)


#Teaching
def remove_column(nums, n):
   result = [i.pop(n) for i in nums]
   return result 

TEACHING = []
with open("data22_23_bulk/teaching22_23.bulk", "w+", encoding="UTF-8") as file:

    index = 0
    numOfAdditionalClasses = 3 # in 22/23 3 additional 4th grade -> which is one level
    numOfNewYears = 1
    for i in range(numOfNewYears):
        for i in range(numOfAdditionalClasses):
            change_subject = 0 #we change teacher of a subject - they are separated by 5 rows
            for j in range(sqlData20_22.SUBJECT.__len__()):
                if j < 9:
                    teacher = sqlData20_22.teacherList[sqlData20_22.id_teacher_subject[index]+change_subject]
                    subject_id = j
                    row = ("|" + str(sqlData20_22.classID) + "|" + str(teacher) + "|" + str(subject_id + 1))
                    TEACHING.append(row)

                    change_subject+=5
                    if j==8: change_subject=9*5
                else:
                    teacher = sqlData20_22.teacherList[change_subject]
                    subject_id = j
                    row = ("|" + str(sqlData20_22.classID) + "|" + str(teacher) + "|" + str(subject_id + 1))
                    TEACHING.append(row)

                    change_subject+=1
            sqlData20_22.classID+=1
        sqlData20_22.id_teacher_subject.insert(0, sqlData20_22.id_teacher_subject.pop())
    
    
    t = ('\n'.join(TEACHING))
    file.write(t)


#Marks
MARKS = []
with open("data22_23_bulk/marks22_23.bulk", "w+", encoding="UTF-8") as file:
    listOfTeachings = []
    listOfStudents = []
    list = []
    activity = ["exam", "test", "homework"]

    myList2 = [item.split("|") for item in sqlData20_22.STUDENTS]
    newList2 = remove_column(myList2, 0)
    myList3 = [item.split("|") for item in STUDENTS]
    newList3 = remove_column(myList3, 0)
    listOfStudents.extend(newList2)
    listOfStudents.extend(newList3)


    startYear=sqlData20_22.startYear
    endYear=sqlData20_22.endYear
    #while generating previous file we ended on 7th (from 20/21) but in 21/22 they happened to be 8th graded (so to get to the 
    #right id we need to skip old 8th (from 20/21) and old 4th (from 21/22 -> which now in 22/23 will be 5th)) -> thats why 2levels* 3classesOnLvl* 24pupils
    studentIdFirst=sqlData20_22.studentIdFirst + (2*3*24) 
    studentIdLast=sqlData20_22.studentIdLast + (2*3*24)
    teachingFirst=sqlData20_22.teachingFirst + (2*3*12)
    teachingLast=sqlData20_22.teachingLast + (2*3*12)
    timeSlots = 1

    
    for m in range(5*3):
        if(m==sqlData20_22.newClasses): 
            teachingFirst = 0; teachingLast=12
            studentIdFirst = 0; studentIdLast=24
        elif(m==3):
            teachingFirst -= (3*2*12); teachingLast -= (3*2*12)
            studentIdFirst -= (3*2*24); studentIdLast -= (3*2*24)
        for i in range(teachingFirst,teachingLast): #number of teachings
            numOfGrades = random.randint(15,20)

            firstSem=int(numOfGrades/2)
            secondSem=numOfGrades-firstSem

            semester = firstSem
            startMonth = 9; endMonth = 1
            startDay=1; endDay=31
            for k in range(2):

                for j in range(semester):
                    start_date = datetime(startYear, startMonth, startDay)
                    end_date = datetime(endYear, endMonth, endDay)
                    valid_date = False
                    while not valid_date:
                        date_of_assesment =fake.date_between_dates(date_start=start_date, date_end=end_date)

                        if date_of_assesment <= datetime.now().date():
                            valid_date=True
                        
                    type_of_act = random.choice(activity)

                    for l in range(studentIdFirst,studentIdLast):
                        score = random.randint(1,6)
                        row = ("|" + str(score) + "|" + str(date_of_assesment) + "|" + str(type_of_act) + "|" + str(i+1) +
                            "|"+ str(listOfStudents[l]))
                            
                        MARKS.append(row)

                if k == 0:
                    startYear=endYear
                    startMonth = 2; endMonth = 6
                    startDay=1; endDay=30
                    semester=secondSem
                
            startYear-=1
            
        teachingFirst+=12
        teachingLast+=12

        studentIdFirst+=24
        studentIdLast+=24
                
    t = ('\n'.join(MARKS))
    file.write(t)


#Schedule Lessons
SCHEDULE_LESSONS = []
with open("data22_23_bulk/schedule_lessons22_23.bulk", "w+", encoding="UTF-8") as file:
    startYear=sqlData20_22.startYearSchedule
    endYear=sqlData20_22.endYearSchedule
    teachingFirst=sqlData20_22.teachingFirstSchedule + (2*3*12)
    teachingLast=sqlData20_22.teachingLastSchedule + (2*3*12)
    semester = ""
    
    for m in range(5*3):
        if(m==sqlData20_22.newClasses): 
            teachingFirst = 1; teachingLast=12
        elif(m==3):
            teachingFirst -= (3*2*12); teachingLast -= (3*2*12)
            
        for sem in range(2): #2 semesters
            for i in range(5): #5 days of lessons
                for j in range(7): #7 lessons per day
                    teaching = random.randint(teachingFirst,teachingLast)
                    if sem == 0: semester = "1"
                    else : semester = "2"
                    row = ("|" + str(sqlData20_22.dayList[i]) + "|" + str(sqlData20_22.hourStart[j]) + "|" + str(sqlData20_22.endHour[j]) + 
                           "|" + str(semester) + "|" + str(startYear)+"/"+str(endYear) + "|" + str(teaching))

                    SCHEDULE_LESSONS.append(row)
            
        teachingFirst+=12
        teachingLast+=12

    t = ('\n'.join(SCHEDULE_LESSONS))
    file.write(t)


#Lessons
LESSONS = []
with open("data22_23_bulk/lessons22_23.bulk", "w+", encoding="UTF-8") as file:
    dateList = [item.split(",") for item in date22_23.output_string.split("\n")]
    scheduleListSub = [item.split("|") for item in SCHEDULE_LESSONS]

    idLesson = sqlData20_22.idLesson
    for i in range(scheduleListSub.__len__()):
        partsSchedDate = scheduleListSub[i][5].split("/")
        for j in range(len(dateList)):
            partsDate = dateList[j][0].split("-")
            
            if ((scheduleListSub[i][4]=="1" and ((partsSchedDate[0]==partsDate[0] and 9<=int(partsDate[1])<=12) or (partsSchedDate[1]==partsDate[0] and int(partsDate[1])==1)))
                or (scheduleListSub[i][4]=="2" and partsSchedDate[1]==partsDate[0] and 2<=int(partsDate[1])<=6)):
                if(scheduleListSub[i][1]==dateList[j][1]):
                    dateOfLesson = dateList[j][0]
                    scheduleSub = idLesson
                    row = ("|" + str(dateOfLesson) + "|" + str(scheduleSub))
                    LESSONS.append(row)
                    j+=7
        
        idLesson+=1

    t = ('\n'.join(LESSONS))
    file.write(t)


#Attendance
import random
def generate_random_bool(high_probability=True, probability=0.8):
    if high_probability:
        return random.random() < probability
    else:
        return random.random() >= probability

ATTENDANCE = []
with open("data22_23_bulk/attendance22_23.bulk", "w+", encoding="UTF-8") as file:
    lessonsList = [item.split("|") for item in LESSONS]

    myList2 = [item.split("|") for item in sqlData20_22.STUDENTS]
    newList2 = remove_column(myList2, 0)
    myList3 = [item.split("|") for item in STUDENTS]
    newList3 = remove_column(myList3, 0)
    listOfStudents.extend(newList2)
    listOfStudents.extend(newList3)
    
    studentIdFirst=sqlData20_22.studentIdFirst + (2*3*24) + 24
    studentIdLast=sqlData20_22.studentIdLast + (2*3*24) + 24

    id=0
    absenceBit = 0
    lessonCounter = sqlData20_22.lessonCounter
    idLesson = sqlData20_22.idLesson
    count = sqlData20_22.count + 70
    for i in range(LESSONS.__len__()):
        for j in range(studentIdFirst,studentIdLast):
            absence = generate_random_bool()
            if absence == True: absenceBit = 1
            else: absenceBit = 0
            row = ("|" + str(absenceBit) + "|" + str(lessonCounter) + "|" + str(listOfStudents[j]))
            ATTENDANCE.append(row)
        
        if i+1<LESSONS.__len__() and int(lessonsList[i+1][2]) == (idLesson+(3*70)) and id == 0: # we take odl idLesson (the last from lesson from 21/22) and 3 classes later we need to change considered class
            studentIdFirst -= (3*2*24)
            studentIdLast -= (3*2*24)
            id = 1
            count+=70
        elif i+1<LESSONS.__len__() and int(lessonsList[i+1][2]) == (idLesson+(2*3*70)) and id == 0:
            studentIdFirst = 0
            studentIdLast = 24
            id = 1
            count+=70
        elif i+1<LESSONS.__len__() and int(lessonsList[i+1][2]) == count: # each class has 7 lessons per day 5 day a week -> but also each class has different schedule for diff semester
            studentIdFirst += 24
            studentIdLast += 24
            count+=70
        
        if i+1<LESSONS.__len__() and int(lessonsList[i+1][2]) != (idLesson+(3*70)) and int(lessonsList[i+1][2]) != (idLesson+(2*3*70)):
            id = 0
        
        lessonCounter+=1
    t = ('\n'.join(ATTENDANCE))
    file.write(t)