update client.self_emp_ueb_pmt_master pmt
set pmt.applicant_notified = 'Y'
where pmt.pmt_id = :pmt_id
