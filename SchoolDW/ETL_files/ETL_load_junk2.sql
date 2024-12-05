use SCHOOL_DW;

INSERT INTO [dbo].[JUNK2] 
SELECT c
FROM 
	  (
		VALUES 
			  ('absent')
			, ('present')
	  ) 
	AS AttendanceCheck(c)
	;