update client.self_emp_ueb_pmt_master pmt
set pmt.status = 'Paid'
where pmt.pmt_id in (
    select pmt.pmt_id
    from client.self_emp_ueb_app app
    inner join client.self_emp_ueb_pmt_master pmt on pmt.app_id = app.app_id
          and pmt.status in ('Pending','Reissued')
)
