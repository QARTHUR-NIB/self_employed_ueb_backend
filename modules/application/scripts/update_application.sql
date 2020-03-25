update client.self_emp_ueb_app app
set app.primary_contact = :primary_contact,
    app.secondary_contact = :secondary_contact,
    app.email = :email,
    app.updated_by = :user_name,
    app.updated_date = current_timestamp,
    app.user_comment = :user_comment
where app.app_id = :app_id
