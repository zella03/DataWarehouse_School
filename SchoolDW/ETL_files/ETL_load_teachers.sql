USE SCHOOL_DW
GO

If (object_id('dbo.EmployeesTemp') is not null) DROP TABLE dbo.EmployeesTemp;
CREATE TABLE dbo.EmployeesTemp (PESEL varchar(11),employee_num varchar(6), name varchar(20),surname varchar(20),gender varchar(6),
		position varchar(16), street_house varchar(100), city varchar(20), zipcode varchar(6), phone varchar(9), email varchar(30), date_emp date, date_dissm date);
go

BULK INSERT dbo.EmployeesTemp
    FROM 'C:\Users\Monika\Desktop\STUDIA\IV_semester\Data_Warehouses\SchoolDW\SchoolDataWarehouse\schoolDatabase\excel\teacher_changed.txt'
    WITH
    (
    FIELDTERMINATOR = '|',
    ROWTERMINATOR = '\n'
    )

--SELECT * FROM dbo.EmployeesTemp;
BULK INSERT dbo.EmployeesTemp
    FROM 'C:\Users\Monika\Desktop\STUDIA\IV_semester\Data_Warehouses\SchoolDW\SchoolDataWarehouse\schoolDatabase\excel\Excel1_22_23.txt'
    WITH
    (
    FIELDTERMINATOR = '|',
    ROWTERMINATOR = '\n'
    )

If (object_id('vETLDimTeacher') is not null) Drop View vETLDimTeacher;
go
CREATE VIEW vETLDimTeacher
AS
SELECT 
	--[Teacher_ID],
	[employee_num] as [Teacher_num],
	[PESEL],
	[NameAndSurname] = Cast([name] + ' ' + [surname] as varchar(50)),
	[Address] = Cast([street_house] + ' ' + [zipcode]+ ' ' + [city] as varchar(80)),
	[gender] as [Gender],
	[Contact] = Cast([phone] + ', ' + [email] as varchar(30)),
	CASE
		WHEN DATEDIFF(year, [date_emp], isNull([date_dissm], CURRENT_TIMESTAMP)) <=2 THEN 'up to two years'
		WHEN DATEDIFF(year, [date_emp], isNull([date_dissm], CURRENT_TIMESTAMP)) >2 THEN 'more than two years'
	END AS [WorkExperience],
	 CASE 
        WHEN date_dissm IS NULL THEN 'YES'
        ELSE 'NO'
    END AS [IsCurrentlyEmployed]
FROM dbo.EmployeesTemp
WHERE [position]='teacher';
go


MERGE INTO TEACHER as TT
	USING vETLDimTeacher as ST
		ON TT.PESEL = ST.PESEL
			WHEN Not Matched
				THEN
					INSERT (Teacher_num, PESEL, NameAndSurname, Address, Gender, Contact, WorkExperience, IsCurrentlyEmployed) 
					Values (
					ST.Teacher_num,
					ST.PESEL,
					ST.NameAndSurname,
					ST.Address,
					ST.Gender,
					ST.Contact,
					ST.WorkExperience,
					ST.IsCurrentlyEmployed
					)
			WHEN Not Matched By Source
				Then
					DELETE
			;
			

-- SELect * from TEACHER;

DROP VIEW vETLDimTeacher;
DROP TABLE dbo.EmployeesTemp;
