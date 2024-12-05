use SCHOOL_DW

INSERT INTO [dbo].[JUNK] 
SELECT a 
FROM 
	  (
		VALUES 
			  ('exam')
			, ('homework')
			, ('test')
	  )AS AttendanceCheck(a);