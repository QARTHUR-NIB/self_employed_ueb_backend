select pmt.pmt_id,pmt.pmt_date,pmt.pmt_type,pmt.pmt_amt,pmt.beg_pay_period,
       pmt.end_pay_period,pmt.status,pmt.updated_by,pmt.updated_date
from client.self_emp_ueb_app app
inner join client.self_emp_ueb_pmt_master pmt on pmt.app_id = app.app_id
where app.app_id = :app_id
