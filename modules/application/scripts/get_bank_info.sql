select bank.*
from client.self_emp_ueb_app app
inner join client.self_emp_ueb_bank_info bank on bank.app_id = app.app_id
where app.app_id = :app_id
