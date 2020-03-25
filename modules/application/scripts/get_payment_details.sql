select pmt_det.pmt_det_id,pmt_det.pmt_id,pmt_det.beg_pay_period,
       pmt_det.end_pay_period,pmt_det.assistance_amount,
       pmt_det.benefit_penalty_amount,pmt_det.pmt_amt
from client.self_emp_ueb_app app
inner join client.self_emp_ueb_pmt_master pmt on pmt.app_id = app.app_id
inner join client.self_emp_ueb_pmt_detail pmt_det on pmt_det.pmt_id = pmt.pmt_id
where app.app_id = :app_id
and pmt_det.pmt_id = :pmt_id
