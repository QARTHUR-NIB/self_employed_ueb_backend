select pmt.pmt_amt,to_char(pmt.pmt_date,'DD'),to_char(pmt.pmt_date,'MM'),
       to_char(pmt.pmt_date,'YYYY'),app.eeni#,
       upper(app.first_name) || ' ' || upper(app.last_name)
from client.self_emp_ueb_app app
inner join client.self_emp_ueb_pmt_master pmt on pmt.app_id = app.app_id
      and pmt.status in ('Pending','Reissued')
left join client.self_emp_ueb_bank_info bank on bank.app_id = app.app_id
      and bank.status = 'Active'
where bank.app_id is null

union

select pmt.pmt_amt,to_char(pmt.pmt_date,'DD'),to_char(pmt.pmt_date,'MM'),
       to_char(pmt.pmt_date,'YYYY'),app.eeni#,
       upper(app.first_name) || ' ' || upper(app.last_name)
from client.self_emp_ueb_app app
inner join client.self_emp_ueb_pmt_master pmt on pmt.app_id = app.app_id
      and pmt.status in ('Pending','Reissued')
inner join client.self_emp_ueb_bank_info bank on bank.app_id = app.app_id
      and bank.status = 'Active' and bank.account_owner = 'No'

