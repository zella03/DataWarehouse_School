/*CREATE DATABASE school1;*/
DROP TABLE IF EXISTS Attendances;
DROP TABLE IF EXISTS ScheduleLessons;
DROP TABLE IF EXISTS Lessons;
DROP TABLE IF EXISTS Marks;
DROP TABLE IF EXISTS Teachings;
DROP TABLE IF EXISTS Subjects;
DROP TABLE IF EXISTS Teachers;
DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Classes;

USE school1

CREATE TABLE Classes (
    classID INT PRIMARY KEY IDENTITY(1,1),
    YearSchoolStarts INT NOT NULL,
	ClassLetter VARCHAR(1) CHECK (ClassLetter IN ('A', 'B', 'C')) NOT NULL
);

CREATE TABLE Students (
    studentID VARCHAR(6) PRIMARY KEY CHECK (studentID LIKE 's[0-9][0-9][0-9][0-9][0-9]'),
    Name NVARCHAR(20) CHECK(Name NOT LIKE '%[^A-Za-z]%' AND LEFT(Name, 1) = UPPER(LEFT(Name, 1))) NOT NULL,
    Surname NVARCHAR(20) CHECK (Surname NOT LIKE '%[^A-Za-z]%' AND LEFT(Surname, 1) = UPPER(LEFT(Surname, 1))) NOT NULL,
    PESEL VARCHAR(12) CHECK ( PESEL LIKE'[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]' ) NOT NULL,
    FK_Class INT NOT NULL,
    FOREIGN KEY (FK_Class) REFERENCES Classes(classID)
);

CREATE TABLE Teachers (
    employeeID VARCHAR(6) PRIMARY KEY CHECK (employeeID LIKE 'e[0-9][0-9][0-9][0-9][a-z]'),
    Name NVARCHAR(20) CHECK(Name NOT LIKE '%[^A-Za-z]%' AND LEFT(Name, 1) = UPPER(LEFT(Name, 1))) NOT NULL,
    Surname NVARCHAR(20) CHECK (Surname NOT LIKE '%[^A-Za-z]%' AND LEFT(Surname, 1) = UPPER(LEFT(Surname, 1))) NOT NULL,
    PESEL VARCHAR(11) CHECK ( PESEL LIKE'[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]' ) NOT NULL
);

CREATE TABLE Subjects (
    SubjectID INT PRIMARY KEY IDENTITY(1,1),
    Name VARCHAR(20) 
);

CREATE TABLE Teachings (
    teachingID INT PRIMARY KEY IDENTITY (1,1),
    FK_Class INT NOT NULL,
    FK_Employee VARCHAR(6) NOT NULL,
    FK_Subject INT NOT NULL,
    FOREIGN KEY (FK_Class) REFERENCES Classes(classID),
    FOREIGN KEY (FK_Employee) REFERENCES Teachers(employeeID),
    FOREIGN KEY (FK_Subject) REFERENCES Subjects(SubjectID)
);

CREATE TABLE Marks (
    markID INT PRIMARY KEY IDENTITY(1,1),
    Score INT  CHECK (Score BETWEEN 1 AND 6) NOT NULL,
    AssessmentDate DATE NOT NULL,
    TypeActivity VARCHAR(20) CHECK (TypeActivity IN ('Exam', 'Homework', 'Test')) NOT NULL,
    FK_Teaching INT NOT NULL,
    FK_Student VARCHAR(6) NOT NULL,
    FOREIGN KEY (FK_Teaching) REFERENCES Teachings(teachingID),
    FOREIGN KEY (FK_Student) REFERENCES Students(studentID)
);

CREATE TABLE ScheduleLessons (
    schLessonID INT PRIMARY KEY IDENTITY(1,1),
	DayOfWeek VARCHAR(10) NOT NULL,
    StartTime TIME NOT NULL,
    EndTime TIME NOT NULL,
    Semester INT CHECK (Semester IN(1,2)) NOT NULL,
    Year VARCHAR(9) NOT NULL,
    FK_Teaching INT NOT NULL,
    FOREIGN KEY (FK_Teaching) REFERENCES Teachings(teachingID)
);

CREATE TABLE Lessons (
    lessonID INT PRIMARY KEY IDENTITY(1,1),
    DateOfLesson DATE NOT NULL,
	FK_ScheduleLesson INT NOT NULL,
	FOREIGN KEY (FK_ScheduleLesson) REFERENCES ScheduleLessons(schLessonID)
);

CREATE TABLE Attendances (
    checkID INT PRIMARY KEY IDENTITY(1,1),
	Checker BIT NOT NULL,
    FK_Lesson INT NOT NULL,
    FK_Student VARCHAR(6) NOT NULL,
    FOREIGN KEY (FK_Student) REFERENCES Students(studentID),
    FOREIGN KEY (FK_Lesson) REFERENCES Lessons(lessonID)
);