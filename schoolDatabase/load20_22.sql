USE school1;
BULK INSERT Subjects
FROM 'C:\Users\Monika\Desktop\STUDIA\IV_semester\Data_Warehouses\SchoolDW\SchoolDataWarehouse\schoolDatabase\data20_22_bulk\subjects.bulk'
WITH (FIELDTERMINATOR = '|');

BULK INSERT Classes
FROM 'C:\Users\Monika\Desktop\STUDIA\IV_semester\Data_Warehouses\SchoolDW\SchoolDataWarehouse\schoolDatabase\data20_22_bulk\classes20_22.bulk'
WITH (FIELDTERMINATOR = '|');

BULK INSERT Marks
FROM 'C:\Users\Monika\Desktop\STUDIA\IV_semester\Data_Warehouses\SchoolDW\SchoolDataWarehouse\schoolDatabase\data20_22_bulk\marks20_22.bulk'
WITH (FIELDTERMINATOR = '|');

BULK INSERT Students
FROM 'C:\Users\Monika\Desktop\STUDIA\IV_semester\Data_Warehouses\SchoolDW\SchoolDataWarehouse\schoolDatabase\data20_22_bulk\students20_22.bulk'
WITH ( FIELDTERMINATOR = '|');

BULK INSERT Teachings
FROM 'C:\Users\Monika\Desktop\STUDIA\IV_semester\Data_Warehouses\SchoolDW\SchoolDataWarehouse\schoolDatabase\data20_22_bulk\teaching20_22.bulk'
WITH ( FIELDTERMINATOR = '|');

BULK INSERT Teachers
FROM 'C:\Users\Monika\Desktop\STUDIA\IV_semester\Data_Warehouses\SchoolDW\SchoolDataWarehouse\schoolDatabase\data20_22_bulk\teachers20_22.bulk'
WITH ( FIELDTERMINATOR = '|');

BULK INSERT ScheduleLessons
FROM 'C:\Users\Monika\Desktop\STUDIA\IV_semester\Data_Warehouses\SchoolDW\SchoolDataWarehouse\schoolDatabase\data20_22_bulk\schedule_lessons20_22.bulk'
WITH ( FIELDTERMINATOR = '|');

BULK INSERT Lessons
FROM 'C:\Users\Monika\Desktop\STUDIA\IV_semester\Data_Warehouses\SchoolDW\SchoolDataWarehouse\schoolDatabase\data20_22_bulk\lessons20_22.bulk'
WITH ( FIELDTERMINATOR = '|');

BULK INSERT Attendances
FROM 'C:\Users\Monika\Desktop\STUDIA\IV_semester\Data_Warehouses\SchoolDW\SchoolDataWarehouse\schoolDatabase\data20_22_bulk\attendance20_22.bulk'
WITH ( FIELDTERMINATOR = '|');