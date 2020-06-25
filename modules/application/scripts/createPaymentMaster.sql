insert into client.self_emp_ueb_pmt_master
(pmt_id,app_id,pmt_date,pmt_type,status,pmt_amt,beg_pay_period,end_pay_period,last_paid_date,
 next_pay_date)
values(:paymentID,:applicationID,current_date,:paymentType,:paymentStatus,:paymentAmount,:beginingPaymentPeriod,
       :endingPaymentPeriod,:lastPaymentDate,:nextPaymentDate)