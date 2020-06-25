select count(pmt_det.pmt_det_id) "numWeeksPaid"
from client.self_emp_ueb_app app
left join client.self_emp_ueb_pmt_master pmt on pmt.app_id = app.app_id
left join client.self_emp_ueb_pmt_detail pmt_det on pmt_det.pmt_id = pmt.pmt_id
where app.app_id = :app_id