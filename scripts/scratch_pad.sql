-- to identify mismatches in default speed across divided roads
--at first glance in Q, these results look reasonable, but digging deeper, there are sometimes matched pairs with duplicates on top with differnt assigned speeds
--need to figure out where these duplicates are coming from
with tblA AS(
	select *
	from typologies_joined tj 
	where "SEQ_NO" in(
		select "SEQ_NO"
		from (
		select "ST_RT_NO","SEQ_NO" , count(*) as cnt
		from typologies_joined tj 
		where "DIV_RDWY" = 1
		group by "ST_RT_NO", "SEQ_NO"
		having count(*) > 1) foo)
	and "DIV_RDWY"= 1
),
tblB as(
select "ST_RT_NO" , "SEQ_NO", default_speed, count(*)
from tblA
group by "ST_RT_NO" , "SEQ_NO", default_speed 
having count(*) = 1
)
select b.*, a.geom
from tblB b
inner join tbla a
on a."ST_RT_NO" = b."ST_RT_NO"
and a."SEQ_NO" = b. "SEQ_NO"