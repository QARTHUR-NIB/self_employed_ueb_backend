select '6',case bank.account_type when 'Savings' then '32' when 'Checking' then '22' end,
       bank.branch_number,'0',cast(bank.bank_account_number as varchar(17)),(pmt.pmt_amt*100),client.self_emp_ueb_chk_run_id.nextval,
       cast(upper(app.first_name)|| ' '||upper(app.last_name) as varchar(16)),'  0056250030',
       row_number() over(order by pmt.pmt_id)
from client.self_emp_ueb_app app
inner join client.self_emp_ueb_bank_info bank on bank.app_id = app.app_id
      and bank.status = 'Active' and bank.account_owner = 'Yes'
inner join client.self_emp_ueb_pmt_master pmt on pmt.app_id = app.app_id
      and pmt.status in ('Pending','Reissued')