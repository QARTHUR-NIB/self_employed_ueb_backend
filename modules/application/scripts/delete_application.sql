/*
Author: Quincy Arthur
Date: March 27th, 2020
Description: Delete Self Employed UEB Application
*/

create or replace procedure client.delete_self_emp_ueb_app(
       p_app_id in client.self_emp_ueb_app.app_id%type,
       success out varchar,
       message out varchar
) as
is_pending varchar(1);
begin
  
  select case when app.status = 'Pending' then 'Y' else 'N' end into is_pending
  from client.self_emp_ueb_app app
  where app.app_id = p_app_id;
  
  if is_pending = 'Y' then
    delete 
    from client.self_emp_ueb_bank_info bank
    where bank.app_id = p_app_id;
    commit;
    
    delete 
    from client.self_emp_ueb_app app
    where app.app_id = p_app_id;
    commit;
    
     success := 'Y';
     message := null;
   else   
     success := 'N';
     message := 'Only applications with a pending status can be deleted'; 
  end if;
 
exception
  when others then
    success := 'N';
    message := 'SQL Code:'||SQLCODE||'-'||SQLERRM;
end;

