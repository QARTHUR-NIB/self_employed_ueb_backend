update client.self_emp_ueb_app app
set app.status = :status,
    app.denial_date = trunc(current_date),
    app.denied_by = :user_name,
    app.user_comment = :user_comment
where app.app_id = :app_id
    and app.status = 'Pending'
