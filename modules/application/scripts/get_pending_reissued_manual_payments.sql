select  pmt.pmt_amt,to_char(pmt.pmt_date,'DD'),to_char(pmt.pmt_date,'MM'),
        to_char(pmt.pmt_date,'YYYY'),app.eeni#,
       upper(app.first_name) || ' ' || upper(app.last_name),
       btch_pmts.batch_id,
       pmt.pmt_id
from client.self_emp_ueb_pmt_master pmt
inner join client.self_emp_ueb_app app on app.app_id = pmt.app_id
inner join client.self_emp_ueb_batch_payments btch_pmts on btch_pmts.pmt_id = pmt.pmt_id
 and btch_pmts.batch_id = (select max(batch_id) keep (dense_rank last order by inserted_date)from client.self_emp_ueb_check_run_batch)
where pmt.pmt_type = 'Check'
 and pmt.status in ('Pending','Reissued') 
