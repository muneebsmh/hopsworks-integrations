use nba;

alter table adv_as 
add PT_Poss double;

set sql_safe_updates=0;
with cte as
(
select a.adv_idx_uuid,a.Box_Type,((b.T2_PTS+b.T1_PTS)/avg(a.T1_Poss_Cnt+a.T2_Poss_Cnt)) as PT_Poss
from adv_as a 
inner join adv_bs b
on a.adv_idx_uuid=b.adv_idx_uuid
and a.Box_Type=b.Box_Type
group by a.adv_idx_uuid,a.box_type
) 
update adv_as a 
inner join cte b
on a.adv_idx_uuid=b.adv_idx_uuid
and a.Box_Type=b.Box_Type
set a.PT_Poss=b.PT_Poss
;

select * from adv_as
where adv_idx_uuid;