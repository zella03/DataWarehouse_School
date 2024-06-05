import random
from faker import Faker
import ExcelFiles20_22
from datetime import datetime
fake = Faker('pl_PL')
from dateFiles import date20_22 

#Teachers
#data taken from the excel -> sheet1
myList = []
TEACHER = []
with open("data20_22_bulk/teachers20_22.bulk", "w+", encoding="UTF-8") as file:
    myList = [item.split("|") for item in ExcelFiles20_22.Excel]

    id=0
    for i in myList:
        if myList[id][5]=="teacher":
            dataEntity = (str(myList[id][1]) + "|" + myList[id][2] + "|" + myList[id][3] + "|" + myList[id][0])
            TEACHER.append(dataEntity)
        id+=1
    
    t = ('\n'.join(TEACHER))
    file.write(t)


#Students
#data taken from the excel -> sheet2
myList = []
STUDENTS = []
with open("data20_22_bulk/students20_22.bulk", "w+", encoding="UTF-8") as file:
    myList = [item.split("|") for item in ExcelFiles20_22.Excel2]

    classIDstud=1
    id=0
    for i in myList:
        dataEntity = (str(myList[id][1]) + "|" + myList[id][2] + "|" + myList[id][3] + "|" + myList[id][0] + "|" + str(classIDstud))
        STUDENTS.append(dataEntity)
        
        if (id+1)%24==0 : classIDstud+=1
        id+=1
    
    t = ('\n'.join(STUDENTS))
    file.write(t)


#Subjects
SUBJECT = []
with open("data20_22_bulk/subjects.bulk", "w+", encoding="UTF-8") as file:
    subjects = ["Mathematics", "Polish", "English", "Science", "German", "WOS", "History", "PE", "IT"
               , "Music", "Art", "Religion"]
    
    for i in subjects:
        row = ("|" + str(i))
        SUBJECT.append(row)

    t = ('\n'.join(SUBJECT))
    file.write(t)

#Classes
#we generate classes for the time period 2020-2022
#in the school year 20/21 we have 15 classes: levels from 4 to 8 and on each level 3 classes A,B,C
#in the school year 21/22 only one level was added as our school welcomed new fourth graders -> 3 new classes 4A, 4B, 4C
#i.e. our file contains 4-8 class years, 3 classes on each level, and at the end we have added 3 new classes which were added in 21/22
CLASSES = []
with open("data20_22_bulk/classes20_22.bulk", "w+", encoding="UTF-8") as file:
    yearOfStart = 0
    letter = ["A","B","C"]
    yearOftheYoungestClassStart = 2020
    yearOftheOldestClass = 2016

    #first 8 classes -> year 20/21
    yearOfStart = yearOftheYoungestClassStart
    while yearOfStart>=yearOftheOldestClass:
        #3 classes on the same level A,B,C
        letterID = 0
        for i in range(3):
            row = ("|" + str(yearOfStart) + "|" + str(letter[letterID]))
            CLASSES.append(row)
            letterID+=1

        yearOfStart-=1

    #additional classes -> in this case 3 new classes of fourth graders
    yearOfStart = yearOftheYoungestClassStart + 1
    numOfNewClasses = 1
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
#in this file we combine teachers, subjects and classes that are thaught this subject by particular teacher
#subjects are assigned for the whole period of study at a given school -> in Poland, subjects usually remain the same during these levels of study
def remove_column(nums, n):
   result = [i.pop(n) for i in nums]
   return result 

TEACHING = []
with open("data20_22_bulk/teaching20_22.bulk", "w+", encoding="UTF-8") as file:
    teacherList2 = [item.split("|") for item in TEACHER]
    teacherList = remove_column(teacherList2, 0)
    index = 0
    classID = 1
    id_teacher_subject = [0,1,2,3,4] #which teacher in order is taken into account - we have 5 teachers for the same subject, each teachers stays with the class for those 5 years of studying
    class_level_count = 0 #we got 3 classes on the same level - they have same teachers

    for i in range(15): #15 classes as the first year school considered -> 20/21
        change_subject = 0 #we change teacher of a subject - they are separated by 5 rows
        for j in range(SUBJECT.__len__()):
            if j < 9:
                teacher = teacherList[id_teacher_subject[index]+change_subject]
                subject_id = j
                row = ("|" + str(classID) + "|" + str(teacher) + "|" + str(subject_id + 1))
                TEACHING.append(row)

                change_subject+=5
                if j==8: change_subject=9*5 #in this row we will find next subject -> following subjects have only one teacher per subject
            else:
                teacher = teacherList[change_subject]
                subject_id = j
                row = ("|" + str(classID) + "|" + str(teacher) + "|" + str(subject_id + 1))
                TEACHING.append(row)

                change_subject+=1
        
        classID+=1
        class_level_count += 1
        if class_level_count%3 == 0:
            index += 1
            class_level_count = 0
        

    id_teacher_subject.insert(0, id_teacher_subject.pop())
    index = 0
    numOfAdditionalClasses = 3 # in 21/22 3 additional 4th grade -> which is one level
    numOfNewYears = 1
    for i in range(numOfNewYears):
        for i in range(numOfAdditionalClasses):
            change_subject = 0 #we change teacher of a subject - they are separated by 5 rows
            for j in range(SUBJECT.__len__()):
                if j < 9:
                    teacher = teacherList[id_teacher_subject[index]+change_subject]
                    subject_id = j
                    row = ("|" + str(classID) + "|" + str(teacher) + "|" + str(subject_id + 1))
                    TEACHING.append(row)

                    change_subject+=5
                    if j==8: change_subject=9*5
                else:
                    teacher = teacherList[change_subject]
                    subject_id = j
                    row = ("|" + str(classID) + "|" + str(teacher) + "|" + str(subject_id + 1))
                    TEACHING.append(row)

                    change_subject+=1
            classID+=1
        id_teacher_subject.insert(0, id_teacher_subject.pop())
    
    t = ('\n'.join(TEACHING))
    file.write(t)


#Marks
#in this file we saved the marks for each student recived during particular teaching (Mathematics, Polish, History, etc.)
#each class recive the same amout of grades per activity, and the number of grades per semester is not fixed
#at this point we have 3 types of assesments
MARKS = []
with open("data20_22_bulk/marks20_22.bulk", "w+", encoding="UTF-8") as file:
    list = []
    activity = ["exam", "test", "homework"]
    myList2 = [item.split("|") for item in STUDENTS]
    newList = remove_column(myList2, 0)

    startYear=2020
    endYear=2021
    studentIdFirst=0
    studentIdLast=24
    teachingFirst=0
    teachingLast=12
    timeSlots = 2
    newClasses=0

    for n in range(timeSlots): #two year taken into account -> year 20/21 and 21/22
        for m in range(5*3): #during each school year we have 15 classes -> levels 4-8 and per each 3 classes A,B,C
            #when we get to the end of the file of students/classes (at the end we have fourth graders) we need to 
            #jump to the begging of the list with students/classes because 4th classes from 20/21 in 21/22 are 5th classes
            if(n>=1 and m==newClasses):
                teachingFirst = 0; teachingLast=12
                studentIdFirst = 0; studentIdLast=24
            for i in range(teachingFirst,teachingLast): #number of teachings -> for each class teachings have differend id thats why we take range of those ids
                numOfGrades = random.randint(15,20)

                firstSem=int(numOfGrades/2)
                secondSem=numOfGrades-firstSem

                semesterGrades = firstSem
                startMonth = 9; endMonth = 1
                startDay=1; endDay=31
                for k in range(2): #we take into account two semestres 

                    for j in range(semesterGrades): #during each semester children received similar ammount of grades but its not always the same
                        start_date = datetime(startYear, startMonth, startDay)
                        end_date = datetime(endYear, endMonth, endDay)
                        valid_date = False
                        while not valid_date:
                            date_of_assesment =fake.date_between_dates(date_start=start_date, date_end=end_date)

                            if date_of_assesment <= datetime.now().date():
                                valid_date=True
                        
                        type_of_act = random.choice(activity)

                        for l in range(studentIdFirst,studentIdLast): #we give each student different grade but each student has to receive the grade
                            score = random.randint(1,6)
                            row = ("|" + str(score) + "|" + str(date_of_assesment) + "|" + str(type_of_act) + "|" + str(i+1) +
                                "|"+ str(newList[l]))
                            
                            MARKS.append(row)

                    if k == 0: #we move to another time period -> to next semester
                        startYear=endYear
                        startMonth = 2; endMonth = 6
                        startDay=1; endDay=30
                        semesterGrades=secondSem
                
                startYear-=1
            
            teachingFirst+=12
            teachingLast+=12

            studentIdFirst+=24
            studentIdLast+=24
                
        endYear+=1
        startYear+=1
        newClasses+=3

    t = ('\n'.join(MARKS))
    file.write(t)


#Schedule Lessons
SCHEDULE_LESSONS = []
#in schedule lesson we contain schedule for each class for first and second semester different 
#each plan covers 5 days per week with 7 lessons per day
#schedule changes also for another shool year
with open("data20_22_bulk/schedule_lessons20_22.bulk", "w+", encoding="UTF-8") as file:
    dayList = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
    hourStart = ["8:00","9:00","10:00","11:00","12:00","13:00","14:00"]
    endHour = ["8:45","9:45","10:45","11:45","12:45","13:45","14:45"]
    startYearSchedule=2020
    endYearSchedule=2021
    teachingFirstSchedule=1
    teachingLastSchedule=12
    timeSlots = 2
    newClassesSchedule=0
    semester = ""

    for n in range(timeSlots): # two school years 20/21 and 21/22
        for m in range(5*3): #CLASSES.__len__()
            if(n>=1 and m==newClassesSchedule): 
                teachingFirstSchedule = 1; teachingLastSchedule=12
            
            for sem in range(2): #2 semesters
                for i in range(5): #5 days of lessons
                    for j in range(7): #7 lessons per day
                        teaching = random.randint(teachingFirstSchedule,teachingLastSchedule)
                        if sem == 0: semester = "1"
                        else : semester = "2"
                        row = ("|" + str(dayList[i]) + "|" + str(hourStart[j]) + "|" + str(endHour[j]) + "|" + str(semester) + "|" + 
                               str(startYearSchedule)+"/"+str(endYearSchedule) + "|" + str(teaching))

                        SCHEDULE_LESSONS.append(row)
            
            teachingFirstSchedule+=12
            teachingLastSchedule+=12
        endYearSchedule+=1
        startYearSchedule+=1
        newClassesSchedule+=3

    t = ('\n'.join(SCHEDULE_LESSONS))
    file.write(t)


#Lessons
#lesson files contains all lesson taking place within the scope of a given teaching
#for each teaching included in the schedule lessons (according to the day on which it takes place) the lessons are 
#listed with the specific date on which they take place
LESSONS = []
with open("data20_22_bulk/lessons20_22.bulk", "w+", encoding="UTF-8") as file:
    dateList = [item.split(",") for item in date20_22.output_string.split("\n")]
    scheduleListSub = [item.split("|") for item in SCHEDULE_LESSONS]

    idLesson=1
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
#attendance is allocated to pupils during each lesson
#at the beginning of the file there are lessons for the first 4A class of 20/21 and so on
import random
def generate_random_bool(high_probability=True, probability=0.8):
    if high_probability:
        return random.random() < probability
    else:
        return random.random() >= probability

ATTENDANCE = []
with open("data20_22_bulk/attendance20_22.bulk", "w+", encoding="UTF-8") as file:
    lessonsList = [item.split("|") for item in LESSONS]
    myList2 = [item.split("|") for item in STUDENTS]
    newList = remove_column(myList2, 0)
    studentIdFirst=0
    studentIdLast=24

    id=0
    count = 71 #after 70 lessons aloccated in schedule lessons (5days*7classes*2semesters) we change considered class
    lessonCounter = 0
    absenceBit = 0
    for i in range(LESSONS.__len__()): #for each lesson included in file
        for j in range(studentIdFirst,studentIdLast): #for the range of the students ids that are in particular class
            absence = generate_random_bool()
            if absence == True: absenceBit = 1
            else: absenceBit = 0
            row = ("|" + str(absenceBit) + "|" + str(i+1) + "|" + str(newList[j]))
            ATTENDANCE.append(row)
        
        if i+1<LESSONS.__len__() and int(lessonsList[i+1][2]) == ((7*10*18)+1) and id == 0: # after considering 18 classes -> because we want to start the file of students from the start od 4th class in 21/22 5th class
            studentIdFirst = 0 
            studentIdLast = 24
            id = 1
            count+=70
        elif i+1<LESSONS.__len__() and int(lessonsList[i+1][2]) == count : # each class has 7 lessons per day 5 day a week -> but also each class has different schedule for diff semester
            studentIdFirst += 24
            studentIdLast += 24
            count+=70
        
        if i+1<LESSONS.__len__() and int(lessonsList[i+1][2]) != ((7*10*18)+1):
            id = 0
        
        lessonCounter+=1
    t = ('\n'.join(ATTENDANCE))
    file.write(t)


import ExcelFiles22_23
from dateFiles import date22_23 

#_____________________________________________________________________
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
STUDENTS_23 = []
with open("data22_23_bulk/students22_23.bulk", "w+", encoding="UTF-8") as file:
    myList = [item.split("|") for item in ExcelFiles22_23.Excel2]

    id=0
    classID=classIDstud
    for i in myList:
        dataEntity = (str(myList[id][1]) + "|" + myList[id][2] + "|" + myList[id][3] + "|" + myList[id][0] + "|" + str(classID))
        STUDENTS_23.append(dataEntity)
        
        if (id+1)%24==0 : classID+=1
        id+=1
    
    t = ('\n'.join(STUDENTS_23))
    file.write(t)


#Classes
CLASSES = []
with open("data22_23_bulk/classes22_23.bulk", "w+", encoding="UTF-8") as file:
    letter = ["A","B","C"]
    
    yearOfStart2 = yearOfStart
    numOfNewClasses = 1 # in 22/23 3 additional 4th grade -> which is one level
    for i in range(numOfNewClasses):
        letterID = 0
        for j in range(3):
            row = ("|" + str(yearOfStart2) + "|" + str(letter[letterID]))
            CLASSES.append(row)
            letterID+=1
        yearOfStart2 += 1

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
            for j in range(SUBJECT.__len__()):
                if j < 9:
                    teacher = teacherList[id_teacher_subject[index]+change_subject]
                    subject_id = j
                    row = ("|" + str(classID) + "|" + str(teacher) + "|" + str(subject_id + 1))
                    TEACHING.append(row)

                    change_subject+=5
                    if j==8: change_subject=9*5
                else:
                    teacher = teacherList[change_subject]
                    subject_id = j
                    row = ("|" + str(classID) + "|" + str(teacher) + "|" + str(subject_id + 1))
                    TEACHING.append(row)

                    change_subject+=1
            classID+=1
        id_teacher_subject.insert(0, id_teacher_subject.pop())
    
    
    t = ('\n'.join(TEACHING))
    file.write(t)


#Marks
MARKS = []
with open("data22_23_bulk/marks22_23.bulk", "w+", encoding="UTF-8") as file:
    listOfTeachings = []
    listOfStudents = []
    list = []
    activity = ["exam", "test", "homework"]

    myList2 = [item.split("|") for item in STUDENTS]
    newList2 = remove_column(myList2, 0)
    myList3 = [item.split("|") for item in STUDENTS_23]
    newList3 = remove_column(myList3, 0)
    listOfStudents.extend(newList2)
    listOfStudents.extend(newList3)


    startYear2=startYear
    endYear2=endYear
    #while generating previous file we ended on 7th (from 20/21) but in 21/22 they happened to be 8th graded (so to get to the 
    #right id we need to skip old 8th (from 20/21) and old 4th (from 21/22 -> which now in 22/23 will be 5th)) -> thats why 2levels* 3classesOnLvl* 24pupils
    studentIdFirst2=studentIdFirst + (2*3*24) 
    studentIdLast2=studentIdLast + (2*3*24)
    teachingFirst2=teachingFirst + (2*3*12)
    teachingLast2=teachingLast + (2*3*12)
    timeSlots = 1

    
    for m in range(5*3):
        if(m==newClasses): 
            teachingFirst2 = 0; teachingLast2=12
            studentIdFirst2 = 0; studentIdLast2=24
        elif(m==3):
            teachingFirst2 -= (3*2*12); teachingLast2 -= (3*2*12)
            studentIdFirst2 -= (3*2*24); studentIdLast2 -= (3*2*24)
        for i in range(teachingFirst2,teachingLast2): #number of teachings
            numOfGrades = random.randint(15,20)

            firstSem=int(numOfGrades/2)
            secondSem=numOfGrades-firstSem

            semester = firstSem
            startMonth = 9; endMonth = 1
            startDay=1; endDay=31
            for k in range(2):

                for j in range(semester):
                    start_date = datetime(startYear2, startMonth, startDay)
                    end_date = datetime(endYear2, endMonth, endDay)
                    valid_date = False
                    while not valid_date:
                        date_of_assesment =fake.date_between_dates(date_start=start_date, date_end=end_date)

                        if date_of_assesment <= datetime.now().date():
                            valid_date=True
                        
                    type_of_act = random.choice(activity)

                    for l in range(studentIdFirst2,studentIdLast2):
                        score = random.randint(1,6)
                        row = ("|" + str(score) + "|" + str(date_of_assesment) + "|" + str(type_of_act) + "|" + str(i+1) +
                            "|"+ str(listOfStudents[l]))
                            
                        MARKS.append(row)

                if k == 0:
                    startYear2=endYear2
                    startMonth = 2; endMonth = 6
                    startDay=1; endDay=30
                    semester=secondSem
                
            startYear2-=1
            
        teachingFirst2+=12
        teachingLast2+=12

        studentIdFirst2+=24
        studentIdLast2+=24
                
    t = ('\n'.join(MARKS))
    file.write(t)


#Schedule Lessons
SCHEDULE_LESSONS = []
with open("data22_23_bulk/schedule_lessons22_23.bulk", "w+", encoding="UTF-8") as file:
    startYear=startYearSchedule
    endYear=endYearSchedule
    teachingFirst=teachingFirstSchedule + (2*3*12)
    teachingLast=teachingLastSchedule + (2*3*12)
    semester = ""
    
    for m in range(5*3):
        if(m==newClasses): 
            teachingFirst = 1; teachingLast=12
        elif(m==3):
            teachingFirst -= (3*2*12); teachingLast -= (3*2*12)
            
        for sem in range(2): #2 semesters
            for i in range(5): #5 days of lessons
                for j in range(7): #7 lessons per day
                    teaching = random.randint(teachingFirst,teachingLast)
                    if sem == 0: semester = "1"
                    else : semester = "2"
                    row = ("|" + str(dayList[i]) + "|" + str(hourStart[j]) + "|" + str(endHour[j]) + 
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

    idLesson2 = idLesson
    for i in range(scheduleListSub.__len__()):
        partsSchedDate = scheduleListSub[i][5].split("/")
        for j in range(len(dateList)):
            partsDate = dateList[j][0].split("-")
            
            if ((scheduleListSub[i][4]=="1" and ((partsSchedDate[0]==partsDate[0] and 9<=int(partsDate[1])<=12) or (partsSchedDate[1]==partsDate[0] and int(partsDate[1])==1)))
                or (scheduleListSub[i][4]=="2" and partsSchedDate[1]==partsDate[0] and 2<=int(partsDate[1])<=6)):
                if(scheduleListSub[i][1]==dateList[j][1]):
                    dateOfLesson = dateList[j][0]
                    scheduleSub = idLesson2
                    row = ("|" + str(dateOfLesson) + "|" + str(scheduleSub))
                    LESSONS.append(row)
                    j+=7
        
        idLesson2+=1

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

    myList2 = [item.split("|") for item in STUDENTS]
    newList2 = remove_column(myList2, 0)
    myList3 = [item.split("|") for item in STUDENTS]
    newList3 = remove_column(myList3, 0)
    listOfStudents.extend(newList2)
    listOfStudents.extend(newList3)
    
    studentIdFirst2=studentIdFirst + (2*3*24) + 24
    studentIdLast2=studentIdLast + (2*3*24) + 24

    id=0
    absenceBit = 0
    lessonCounter2 = lessonCounter
    idLesson2 = idLesson
    count2 = count + 70
    for i in range(LESSONS.__len__()):
        for j in range(studentIdFirst2,studentIdLast2):
            absence = generate_random_bool()
            if absence == True: absenceBit = 1
            else: absenceBit = 0
            row = ("|" + str(absenceBit) + "|" + str(lessonCounter2) + "|" + str(listOfStudents[j]))
            ATTENDANCE.append(row)
        
        if i+1<LESSONS.__len__() and int(lessonsList[i+1][2]) == (idLesson2+(3*70)) and id == 0: # we take odl idLesson (the last from lesson from 21/22) and 3 classes later we need to change considered class
            studentIdFirst2 -= (3*2*24)
            studentIdLast2 -= (3*2*24)
            id = 1
            count2+=70
        elif i+1<LESSONS.__len__() and int(lessonsList[i+1][2]) == (idLesson2+(2*3*70)) and id == 0:
            studentIdFirst2 = 0
            studentIdLast2 = 24
            id = 1
            count2+=70
        elif i+1<LESSONS.__len__() and int(lessonsList[i+1][2]) == count2: # each class has 7 lessons per day 5 day a week -> but also each class has different schedule for diff semester
            studentIdFirst2 += 24
            studentIdLast2 += 24
            count2+=70
        
        if i+1<LESSONS.__len__() and int(lessonsList[i+1][2]) != (idLesson2+(3*70)) and int(lessonsList[i+1][2]) != (idLesson2+(2*3*70)):
            id = 0
        
        lessonCounter2+=1
    t = ('\n'.join(ATTENDANCE))
    file.write(t)