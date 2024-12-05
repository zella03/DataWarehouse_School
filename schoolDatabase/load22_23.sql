use school1;
UPDATE Subjects SET "Name" = 'Advanced Mathematic' WHERE "SubjectID" = '1';
UPDATE Subjects SET "Name" = 'HIT' WHERE "SubjectID" = '6';
UPDATE Subjects SET "Name" = 'Theatre' WHERE "SubjectID" = '11';

BULK INSERT Classes
FROM 'C:\Users\Monika\Desktop\STUDIA\IV_semester\Data_Warehouses\SchoolDW\SchoolDataWarehouse\schoolDatabase\data22_23_bulk\classes22_23.bulk'
WITH (FIELDTERMINATOR = '|');

BULK INSERT Marks
FROM 'C:\Users\Monika\Desktop\STUDIA\IV_semester\Data_Warehouses\SchoolDW\SchoolDataWarehouse\schoolDatabase\data22_23_bulk\marks22_23.bulk'
WITH (FIELDTERMINATOR = '|');

BULK INSERT Students
FROM 'C:\Users\Monika\Desktop\STUDIA\IV_semester\Data_Warehouses\SchoolDW\SchoolDataWarehouse\schoolDatabase\data22_23_bulk\students22_23.bulk'
WITH ( FIELDTERMINATOR = '|');

BULK INSERT Teachings
FROM 'C:\Users\Monika\Desktop\STUDIA\IV_semester\Data_Warehouses\SchoolDW\SchoolDataWarehouse\schoolDatabase\data22_23_bulk\teaching22_23.bulk'
WITH ( FIELDTERMINATOR = '|');

BULK INSERT Teachers
FROM 'C:\Users\Monika\Desktop\STUDIA\IV_semester\Data_Warehouses\SchoolDW\SchoolDataWarehouse\schoolDatabase\data22_23_bulk\teachers22_23.bulk'
WITH ( FIELDTERMINATOR = '|');

BULK INSERT ScheduleLessons
FROM 'C:\Users\Monika\Desktop\STUDIA\IV_semester\Data_Warehouses\SchoolDW\SchoolDataWarehouse\schoolDatabase\data22_23_bulk\schedule_lessons22_23.bulk'
WITH ( FIELDTERMINATOR = '|');

BULK INSERT Lessons
FROM 'C:\Users\Monika\Desktop\STUDIA\IV_semester\Data_Warehouses\SchoolDW\SchoolDataWarehouse\schoolDatabase\data22_23_bulk\lessons22_23.bulk'
WITH ( FIELDTERMINATOR = '|');

BULK INSERT Attendances
FROM 'C:\Users\Monika\Desktop\STUDIA\IV_semester\Data_Warehouses\SchoolDW\SchoolDataWarehouse\schoolDatabase\data22_23_bulk\attendance22_23.bulk'
WITH ( FIELDTERMINATOR = '|');