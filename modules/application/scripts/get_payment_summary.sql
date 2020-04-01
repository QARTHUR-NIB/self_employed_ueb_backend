select app.app_id,sum(pmt.pmt_amt),
       (select count(det.pmt_det_id)
        from client.self_emp_ueb_pmt_master pmt
        inner join client.self_emp_ueb_pmt_detail det on det.pmt_id = pmt.pmt_id
        where pmt.app_id = app.app_id
         and pmt.status = 'Paid'
        ) num_weeks_paid
from client.self_emp_ueb_app app
inner join client.self_emp_ueb_pmt_master pmt on pmt.app_id = app.app_id
 and pmt.status = 'Paid'
where app.app_id = :app_id
group by app.app_id
