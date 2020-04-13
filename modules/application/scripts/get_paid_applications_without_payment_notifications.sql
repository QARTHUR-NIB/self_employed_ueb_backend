select app.first_name,to_char(pmt.beg_pay_period,'YYYY-MON-DD'),
       to_char(pmt.end_pay_period,'YYYY-MON-DD'),
       (select count(det.pmt_det_id)
        from client.self_emp_ueb_pmt_master pmt
        inner join client.self_emp_ueb_pmt_detail det on det.pmt_id = pmt.pmt_id
        where pmt.app_id = app.app_id
         and pmt.status = 'Paid'
        ) num_weeks_paid,8 max_weeks,pmt.pmt_type,
        branch.branch_name,bank.bank_account_number,pmt.pmt_id,app.email,
        app.tourism_industry
from client.self_emp_ueb_app app
inner join client.self_emp_ueb_pmt_master pmt on pmt.app_id = app.app_id
 and pmt.status = 'Paid' and pmt.applicant_notified = 'N'
left join client.self_emp_ueb_bank_info bank on bank.app_id = app.app_id
 and bank.status = 'Active'
left join client.bank_branches branch on branch.branch_number = bank.branch_number
