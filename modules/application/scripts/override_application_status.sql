update client.self_emp_ueb_app app
set app.user_comment = trim(app.user_comment) || ' APPLICATION OVERRIDEN RESET FROM ' || upper(app.status) ||  ' BY ' || :user_name,
    app.status = :status,
    app.denial_date = null,
    app.denied_by = null,
    app.approved_by =  null,
    app.approval_date = null,
    app.routed_to = null,
    app.routed_date =  null,
    app.updated_by = :user_name
where app.app_id = :app_id
