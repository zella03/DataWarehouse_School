USE SCHOOL_DW;
GO

IF OBJECT_ID('vETLDimClass') IS NOT NULL 
    DROP VIEW vETLDimClass;
GO

CREATE VIEW vETLDimClass
AS
SELECT DISTINCT
    [YearSchoolStarts] AS [YearSchoolStarts],
    [ClassLetter] AS [ClassLetter]
FROM [school1].[dbo].[Classes];
GO

MERGE INTO CLASS AS C
USING vETLDimClass AS DIM
    ON C.YearSchoolStarts = DIM.YearSchoolStarts
        AND C.ClassLetter = DIM.ClassLetter
WHEN NOT MATCHED THEN
    INSERT (YearSchoolStarts, ClassLetter)
    VALUES (DIM.YearSchoolStarts, DIM.ClassLetter)
WHEN NOT MATCHED BY SOURCE THEN
    DELETE;
GO

DROP VIEW vETLDimClass;