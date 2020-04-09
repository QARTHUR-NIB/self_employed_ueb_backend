select upper(app.first_name) || ' ' || upper(app.last_name),app.primary_contact,
       pmt.pmt_amt,app.email,'NIB', app.eeni#
from client.self_emp_ueb_pmt_master pmt
inner join client.self_emp_ueb_app app on app.app_id = pmt.app_id
inner join client.self_emp_ueb_batch_payments btch_pmts on btch_pmts.pmt_id = pmt.pmt_id
 and btch_pmts.batch_id = (select max(batch_id) keep (dense_rank last order by inserted_date)from client.self_emp_ueb_check_run_batch)
where pmt.pmt_type = 'SUN'
 and pmt.status in ('Pending','Reissued')
