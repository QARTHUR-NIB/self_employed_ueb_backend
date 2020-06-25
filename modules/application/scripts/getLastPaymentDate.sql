select max(pmt.last_paid_date) keep (dense_rank last order by pmt.inserted_date) "lastPaymentDate"
from client.self_emp_ueb_app app
left join client.self_emp_ueb_bank_info bank on bank.app_id = app.app_id and bank.status = 'Active'
left join client.self_emp_ueb_pmt_master pmt on pmt.app_id = app.app_id
left join client.self_emp_ueb_pmt_detail pmt_det on pmt_det.pmt_id = pmt.pmt_id
where app.app_id = :app_id