update client.self_emp_ueb_bank_info bank
set bank.status = 'Inactive'
where bank.app_id = :app_id
 and bank.status = 'Active'
