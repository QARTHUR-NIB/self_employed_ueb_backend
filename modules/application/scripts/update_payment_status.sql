update client.self_emp_ueb_pmt_master pmt
set pmt.status = :status,
    pmt.updated_by = :user_name,
    pmt.updated_date = trunc(current_date)
where pmt.pmt_id = :pmt_id
 and pmt.app_id = :app_id
