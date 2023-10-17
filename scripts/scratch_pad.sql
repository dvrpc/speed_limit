-- obs_greaterthan_posted_overnight
-- any hour netween 7pm and 12am
select objectid, "ST_RT_NO" , "SPD_LIMIT" , "TYPOLOGY" , "HIN" , geom , spdwkd1920, spdwkd2021, spdwkd2122, spdwkd2223, spdwkd2300
from rejoined.inrix i 
where spdwkd1920 > "SPD_LIMIT"
or spdwkd2021 > "SPD_LIMIT"
or spdwkd2122 > "SPD_LIMIT"
or spdwkd2223 > "SPD_LIMIT"
or spdwkd2300 > "SPD_LIMIT"



with tblA as(
	select *
	from rejoined.inrix i
	where spdwkd1920 > "SPD_LIMIT"
	),
tblB as(
	select *
	from rejoined.inrix i2
	where spdwkd2021 > "SPD_LIMIT"
	),
tblC as(
	select *
	from rejoined.inrix i3
	where spdwkd2122 > "SPD_LIMIT"
	),
tblD as(
	select *
	from rejoined.inrix i4
	where spdwkd2223 > "SPD_LIMIT"
	),
tblE as(
	select *
	from rejoined.inrix i5
	where spdwkd2300 > "SPD_LIMIT"
	),
tblF as(
	select *
	from tblA
	union all
	select *
	from tblB
	union all
	select *
	from tblC
	union all
	select*
	from tblD
	union all
	select *
	from tblE
	),
tblCOUNT as(
	select objectid, count(*), round(count(*)/5::numeric, 2) as percentage
	from tblF
	group by (objectid)
	)
select i6.*, tc.count, tc.percentage
from rejoined.inrix i6 
left join tblCOUNT tc
on i6.objectid = tc.objectid


-- "ST_RT_NO" , "SPD_LIMIT" , "TYPOLOGY" , "HIN" , geom ,
--spdwkd1920, spdwkd2021, spdwkd2122, spdwkd2223, spdwkd2300