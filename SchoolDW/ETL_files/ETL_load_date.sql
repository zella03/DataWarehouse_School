use SCHOOL_DW
go

-- Step a: Declare variables use in processing
DECLARE @StartDate DATE; 
DECLARE @EndDate DATE;

-- Step b: Fill the variable with values for the range of years needed
SELECT @StartDate = '2020-09-01', @EndDate = '2023-06-30';

-- Step c: Use a while loop to add dates to the table
DECLARE @DateInProcess DATETIME = @StartDate;


WHILE @DateInProcess <= @EndDate
BEGIN
    -- Check if the current date is a weekend (Saturday or Sunday) or a holiday
    /*IF DATEPART(dw, @DateInProcess) NOT IN (1, 7) -- Exclude Sundays (1) and Saturdays (7)
        AND MONTH(@DateInProcess) NOT IN (7, 8)*/ -- Exclude July (7) and August (8)
	IF MONTH(@DateInProcess) NOT IN (7, 8)
    BEGIN
        -- Check if the current date is a holiday and skip it
        IF NOT EXISTS (SELECT 1 FROM auxiliary.dbo.vacations WHERE @DateInProcess BETWEEN start AND koniec)
        BEGIN
            -- Add a row into the date dimension table for this date
            INSERT INTO [dbo].[DATE] 
            (
                [Date],
                [Day],
                [Month],
                [MonthNo],
                [Year],
                [Semester],
                [DayOfWeek]
            )
            VALUES 
            ( 
                @DateInProcess, -- [Date]
                DATEPART(dw, @DateInProcess), -- [Day]
                CAST(DATENAME(month, @DateInProcess) AS VARCHAR(10)), -- [Month]
                MONTH(@DateInProcess), -- [MonthNo]
                CAST(YEAR(@DateInProcess) AS VARCHAR(4)), -- [Year]
                -- Assuming your semester logic here, adjust accordingly
                CASE 
                    WHEN MONTH(@DateInProcess) BETWEEN 9 AND 12 OR MONTH(@DateInProcess) = 1 THEN 'Winter semester'
                    ELSE 'Summer semester'
                END,
                CAST(DATENAME(dw, @DateInProcess) AS VARCHAR(15)) -- [DayOfWeek]
            );  
        END
    END
    -- Add a day and loop again
    SET @DateInProcess = DATEADD(d, 1, @DateInProcess);
END


-- insert into holidays and vacations
-------------------------------------------------------------

-- auxiliary tables should be created first!


IF OBJECT_ID('vETLDimDatesData') IS NOT NULL DROP VIEW vETLDimDatesData;
GO

CREATE VIEW vETLDimDatesData
AS
SELECT 
    dd.[Date] AS DateKey,
    dd.[Date],
    CAST(YEAR(dd.[Date]) AS VARCHAR(4)) AS [Year],
    DATENAME(MONTH, dd.[Date]) AS [Month],
    MONTH(dd.[Date]) AS [MonthNo],
    DATENAME(DW, dd.[Date]) AS [DayOfWeek],
    DATEPART(DW, dd.[Date]) AS [DayOfWeekNo],
    CASE
        WHEN v.start IS NOT NULL THEN 'holiday'
        ELSE 'non-holiday'
    END AS [Holiday],
    CASE 
        WHEN MONTH(dd.[Date]) BETWEEN 9 AND 12 OR MONTH(dd.[Date]) = 1 THEN 'Winter semester'
        ELSE 'Summer semester'
    END AS [Semester]
FROM [dbo].[DATE] AS dd
LEFT JOIN auxiliary.dbo.vacations AS v ON dd.[Date] BETWEEN v.start AND v.koniec
WHERE DATEPART(DW, dd.[Date]) NOT IN (1, 7);  -- Exclude Sundays (1) and Saturdays (7)
GO

-- Merge view with updated information about holidays and before holiday days with already existing DimDate rows

-- SELECT * from DimDate;

Drop View vETLDimDatesData;