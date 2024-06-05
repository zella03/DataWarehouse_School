use SCHOOL_DW;
go

If (object_id('vETLCheckingAttendance') is not null) Drop view vETLCheckingAttendance;
go
CREATE VIEW vETLCheckingAttendance
AS
SELECT DISTINCT
    Subject_teaching_ID = st.Subject_teaching_num,
    Student_ID = dbo.STUDENT.Student_ID,
    AssessmentDate_ID = ST3.Date_ID,
    Time_ID=ST5.Time_ID,
    Junk2_ID=junk2.Junk2_ID
FROM school1.dbo.Attendances as ST1
JOIN dbo.STUDENT on dbo.STUDENT.Student_num = ST1.FK_Student
JOIN school1.dbo.Lessons ST2 on ST2.lessonID = ST1.FK_Lesson
JOIN dbo.DATE ST3 on CONVERT(VARCHAR(10), ST3.Date, 111) = CONVERT(VARCHAR(10), ST2.DateOfLesson, 111)
JOIN school1.dbo.ScheduleLessons ST4 on ST4.schLessonID=ST2.FK_ScheduleLesson
JOIN dbo.TIME ST5 ON ST5.Hour = DATEPART(HOUR, ST4.StartTime)
JOIN dbo.JUNK2 as junk2 ON junk2.AttendanceCheck =
    CASE 
        WHEN ST1.Checker = 1 THEN 'absent'
        WHEN ST1.Checker = 0 THEN 'present'
    END
JOIN school1.dbo.Teachings as t ON t.teachingID = ST4.FK_Teaching
JOIN dbo.SUBJECT_TEACHING as st ON st.Subject_teaching_num = t.teachingID
;
go

MERGE INTO CHECKING_ATTENDANCE as TT
    USING vETLCheckingAttendance as ST
        ON TT.Subject_teaching_ID = ST.Subject_teaching_ID
        AND TT.Student_ID = ST.Student_ID
        AND TT.AssessmentDate_ID = ST.AssessmentDate_ID
        AND TT.Time_ID = ST.Time_ID
        AND TT.Junk2_ID = ST.Junk2_ID
            WHEN Not Matched
                THEN
                    INSERT
                    Values (
                    ST.Subject_teaching_ID,
                    ST.Student_ID,
                    ST.AssessmentDate_ID,
                    ST.Time_ID,
                    ST.Junk2_ID
                    )
            ;

Drop view vETLCheckingAttendance;
