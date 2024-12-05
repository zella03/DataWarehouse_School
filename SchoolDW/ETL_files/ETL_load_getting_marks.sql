use SCHOOL_DW;
go

If (object_id('vETLFGettingMarks') is not null) Drop view vETLFGettingMarks;
go
CREATE VIEW vETLFGettingMarks
AS
SELECT DISTINCT
		Mark_num = ST1.markID,
		Score = ST1.Score,
		Student_ID = ST2.Student_ID,
		MarkDate_ID = SD.Date_ID,
		Subject_teaching_ID = ST3.Subject_teaching_num,
		Junk_ID = junk.Junk_ID
	FROM school1.dbo.Marks AS ST1
	JOIN dbo.STUDENT as ST2 ON ST1.FK_Student = ST2.Student_num
	JOIN dbo.DATE as SD ON CONVERT(VARCHAR(10), SD.Date, 111) = CONVERT(VARCHAR(10), ST1.AssessmentDate, 111)
	JOIN dbo.SUBJECT_TEACHING as ST3 ON ST3.Subject_teaching_num = ST1.FK_Teaching
	JOIN dbo.JUNK as junk ON junk.TypeOfActivity = ST1.TypeActivity

/*
SELECT DISTINCT AssessmentDate FROM school1.dbo.Marks
WHERE school1.dbo.Marks.markID NOT IN
(SELECT Mark_num FROM vETLFGettingMarks)
SELECT * FROM dbo.DATE*/

GO

MERGE INTO GETTING_MARKS as TT
	USING vETLFGettingMarks as ST
		ON 	
			TT.Mark_num = ST.Mark_num
		AND TT.Score = ST.Score
		AND	TT.Student_ID = ST.Student_ID
		AND TT.Subject_Teaching_ID = ST.Subject_teaching_ID
		AND TT.MarkDate_ID = ST.MarkDate_ID
		AND TT.Junk_ID = ST.Junk_ID
			WHEN Not Matched
				THEN
					INSERT
					Values (
						Mark_num
						, Score
						, ST.Student_ID
						, ST.Subject_Teaching_ID
						, ST.MarkDate_ID
						, ST.Junk_ID
					)
			;

Drop view vETLFGettingMarks;

-- select * from FBookSales;