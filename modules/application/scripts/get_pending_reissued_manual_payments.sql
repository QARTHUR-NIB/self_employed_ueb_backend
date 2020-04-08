select  pmt.pmt_amt,to_char(pmt.pmt_date,'DD'),to_char(pmt.pmt_date,'MM'),
        to_char(pmt.pmt_date,'YYYY'),app.eeni#,
       upper(app.first_name) || ' ' || upper(app.last_name)
from client.self_emp_ueb_pmt_master pmt
inner join client.self_emp_ueb_app app on app.app_id = pmt.app_id
where pmt.pmt_type = 'Check'
 and pmt.status in ('Pending','Reissued')
