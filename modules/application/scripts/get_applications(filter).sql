select *
from(
select app.*,row_number() over (order by app.app_id) rn,
       count(app.app_id) over (order by app.app_id)
from client.self_emp_ueb_app app
:where_clause
) applications
where rn between ((:page_size * :page_number) - (:page_size - 1)) and (:page_size * :page_number)
