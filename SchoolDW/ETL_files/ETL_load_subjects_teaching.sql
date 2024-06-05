USE SCHOOL_DW;
GO

IF OBJECT_ID('vETLDimSubjectsData') IS NOT NULL 
    DROP VIEW vETLDimSubjectsData;
GO

CREATE VIEW vETLDimSubjectsData
AS
SELECT DISTINCT
    Subject_teaching_num = s.teachingID,
    s1.Name AS [Subject_name],
    'YES' AS [isCurrent],
    Teacher_ID AS [Teacher_ID]
FROM school1.dbo.Teachings AS s
JOIN school1.dbo.Subjects AS s1 ON s1.SubjectID = s.FK_Subject
LEFT JOIN dbo.TEACHER AS t1 ON t1.Teacher_num = s.FK_Employee;
GO

MERGE INTO SUBJECT_TEACHING as ST
USING vETLDimSubjectsData as DIM
        ON ST.Subject_teaching_num=DIM.Subject_teaching_num
            WHEN Not Matched
                THEN
                    INSERT Values (
                    DIM.Subject_teaching_num,
                    DIM.Subject_name,
                    DIM.Teacher_ID,
                    'YES'
                    )
            WHEN MATCHED AND (DIM.Subject_name <> ST.Subject_name)
            THEN
                UPDATE SET 
                    ST.isCurrent = 'NO' -- Assuming we're marking previous record as not current
        ;

-- Insert new records from ETL source to subject_teaching table
INSERT INTO subject_teaching (
    Subject_teaching_num, 
    Subject_name, 
    Teacher_ID, 
    isCurrent
)
SELECT 
    Subject_teaching_num, 
    Subject_name, 
    Teacher_ID, 
    'YES' -- Assuming isCurrent is set to 1 for new records
FROM 
    vETLDimSubjectsData
EXCEPT
SELECT 
    Subject_teaching_num, 
    Subject_name, 
    Teacher_ID, 
    'YES'
FROM 
    SUBJECT_TEACHING;

DROP VIEW vETLDimSubjectsData;