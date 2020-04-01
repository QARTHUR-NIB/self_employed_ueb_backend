select su.user_name,min(sr.display_name) keep (dense_rank first order by sru.priority)
from dbo.security_users su
inner join dbo.security_role_user sru on sru.security_users_id = su.security_users_id
inner join dbo.security_role sr on sr.role_id = sru.role_id
inner join dbo.security_department_role sdr on sdr.role_id = sr.role_id
inner join dbo.security_department sd on sd.department_id = sdr.department_id
where lower(su.user_name) = lower(:user_name)
group by su.user_name
