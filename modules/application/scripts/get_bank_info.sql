select bank.*,branch.branch_name
from client.self_emp_ueb_app app
inner join client.self_emp_ueb_bank_info bank on bank.app_id = app.app_id
inner join client.bank_branches branch on branch.branch_number = bank.branch_number
where app.app_id = :app_id
