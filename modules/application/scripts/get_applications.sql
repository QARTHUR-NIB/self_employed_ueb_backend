select *
from(
select app.*,row_number() over (order by app.app_id) rn,
       count(*) over ()
from client.self_emp_ueb_app app
) applications
where rn between ((:page_size * :page_number) - (:page_size - 1)) and (:page_size * :page_number)
