select '6',case bank.account_type when 'Savings' then '32' when 'Checking' then '22' end,
       bank.branch_number,'0',bank.bank_account_number,(pmt.pmt_amt*100),client.self_emp_ueb_chk_run_id.nextval,
       upper(app.first_name)|| ' '||upper(app.last_name),'0056250030',
       row_number() over(order by pmt.pmt_id)
from client.self_emp_ueb_app app
inner join client.self_emp_ueb_bank_info bank on bank.app_id = app.app_id
      and bank.status = 'Active'
inner join client.self_emp_ueb_pmt_master pmt on pmt.app_id = app.app_id
      and pmt.status in ('Pending','Reissued')
