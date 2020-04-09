update client.self_emp_ueb_batch_payments btch
set btch.check_num = :check_num,
    btch.check_generated = 'Yes'
where btch.batch_id = :batch_id
 and btch.pmt_id = :pmt_id
 and btch.pmt_type = 'Check'
 and btch.check_generated = 'No'