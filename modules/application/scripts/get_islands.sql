select distinct state.state_name
from dbo.state
where replace(translate( state_code, '0123456789', '0000000000' ),'0', '') is null
order by state.state_name
