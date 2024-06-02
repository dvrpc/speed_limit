-- to identify mismatches in default speed across divided roads
with tblA as(
	select "ST_RT_NO","SEQ_NO" , default_speed, count(*) as cnt
	from typologies_joined tj 
	where "DIV_RDWY" = 1
	group by "ST_RT_NO", "SEQ_NO", default_speed
	having count(*) = 1
	)
select a.*, tj.geom 
from typologies_joined tj
inner join tblA a
on tj."ST_RT_NO" = a."ST_RT_NO"
and tj."SEQ_NO" = a."SEQ_NO"
and tj.default_speed = a.default_speed

-- need to look at context to see what to adjust the SL to
-- not sure there is a programatic way to do this - might have to be manual
-- or look into what is adjacent?

-- for other inconsistencies; possible to dissolve by default speed (and other fields) and then calcualte distance?

-- need to get rid of ST_RT_NO that start with G (what are these??)
-- next steps - 1. re run script 3 with new overwrites
-- 2. see if/how many mismatches and inconsistencies are still a problem  (some, but not as many)

-- 3. dissolve and calculate distances of each segment; if shorter than mile, manually adjust?
-- 4. manually adjust those with differences on either sides of divided road (see query above)
 -- in python, grab mismatches results from query
 -- itterate over each pair with same seqno. grab seqno +1 and -1 to check default speed
 -- change default speed of the one in the mismatched pair that doesn't match the surrounding segments
 -- udpate based objectid (query)
 -- same method could possibly be used for short segments that don't match surrounding speeds (although I'd prefer to leave this part alone)