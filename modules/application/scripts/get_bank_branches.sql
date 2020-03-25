select oi.oi_name,oi.routing_number
from dbo.oi_organization oi
where oip_type_id = 15 
 and routing_number is not null
 and oi_org_status = 'A'
order by oi.oi_name
