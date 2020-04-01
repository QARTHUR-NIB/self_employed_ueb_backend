select sr.display_name
from dbo.security_role sr
inner join dbo.security_department_role sdr on sdr.role_id = sr.role_id
inner join dbo.security_department sd on sd.department_id = sdr.department_id
where sd.department_name in ('LONG TERM BENEFIT or CENTRAL BENEFIT','IT','EXECUTIVE','System Administrator')
 and sr.display_name not in ('EXECUTIVE - ACCOUNTS  E','EXECUTIVE - AUDIT  E','EXECUTIVE - IT  E','EXECUTIVE - LEGAL  E','SECURITY MANAGER IT')
