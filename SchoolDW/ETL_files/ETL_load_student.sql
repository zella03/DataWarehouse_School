USE SCHOOL_DW
GO

If (object_id('dbo.StudentsTemp') is not null) DROP TABLE dbo.StudentsTemp;
CREATE TABLE dbo.StudentsTemp (PESEL varchar(11),student_num varchar(6), name varchar(20),surname varchar(20), birth_date date, birth_city varchar(35), gender varchar(6),
		street_house varchar(100), city varchar(20), postal_code varchar(6), placeOfLiving varchar(20), phone varchar(9), email varchar(45));
go

BULK INSERT dbo.StudentsTemp
    FROM 'C:\Users\Monika\Desktop\STUDIA\IV_semester\Data_Warehouses\SchoolDW\SchoolDataWarehouse\schoolDatabase\excel\Excel2_20_22.txt'
    WITH
    (
    FIELDTERMINATOR = '|',
    ROWTERMINATOR = '\n'
    )

--SELECT * FROM dbo.EmployeesTemp;
BULK INSERT dbo.StudentsTemp
    FROM 'C:\Users\Monika\Desktop\STUDIA\IV_semester\Data_Warehouses\SchoolDW\SchoolDataWarehouse\schoolDatabase\excel\Excel2_22_23.txt'
    WITH
    (
    FIELDTERMINATOR = '|',
    ROWTERMINATOR = '\n'
    )

IF (object_id('vETLDimStudent') IS NOT NULL) DROP VIEW vETLDimStudent;
go
CREATE VIEW vETLDimStudent
AS
SELECT 
    s.[student_num] AS StudentNumber,
    s.[PESEL],
    [NameAndSurname] = CAST(s.[name] + ' ' + s.[surname] AS VARCHAR(50)),
    [Address] = CAST(s.[street_house] + ' ' + s.[postal_code] + ' ' + s.[city] AS VARCHAR(80)),
    s.[birth_city],
	CASE
		WHEN TRY_CAST(c.YearSchoolStarts AS INT) - YEAR(s.[birth_date]) <= 11 THEN 'from 9 to 11'
        ELSE 'from 12 to 14'
	END AS [AgeCategory],
    s.[gender] AS [Gender],
    s.[placeOfLiving],
    [Contact] = CAST(s.[phone] + ', ' + s.[email] AS VARCHAR(60)),
    c.[Class_ID]
FROM dbo.StudentsTemp AS s
JOIN school1.dbo.Students AS s1 ON s1.studentID = s.student_num
JOIN dbo.CLASS AS c ON s1.FK_Class = c.Class_ID;
GO

-----------------------------------------
-- for testing purposes only!!
/*Declare @EntryDate date; 
SELECT @EntryDate = '2020-09-01';*/
--SELECT @EntryDate = '2016-06-30 00:00:00';
-----------------------------------------

MERGE INTO STUDENT as TT
	USING vETLDimStudent as ST
		ON TT.PESEL = ST.PESEL
			WHEN Not Matched
				THEN
					INSERT Values (
					ST.StudentNumber,
					ST.PESEL,
					ST.NameAndSurname,
					ST.Address,
					ST.[AgeCategory],
					ST.[birth_city],
					ST.Gender,
					ST.[placeOfLiving],
					ST.Contact,
					ST.Class_ID
					)
			WHEN Not Matched By Source
				Then
					DELETE
			;

DROP VIEW vETLDimStudent;
DROP TABLE dbo.StudentsTemp;
