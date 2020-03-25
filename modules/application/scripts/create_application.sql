/*
Author: Quincy Arthur
Date: March 19th, 2020
Description: Create Self Employed UEB Application
*/

create or replace procedure client.create_self_emp_ueb_app(
       p_first_name in client.self_emp_ueb_app.first_name%type,
       p_last_name in client.self_emp_ueb_app.last_name%type,
       p_dob in varchar,
       p_eeni# in client.self_emp_ueb_app.eeni#%type,
       p_erni# in client.self_emp_ueb_app.erni#%type,
       p_email in client.self_emp_ueb_app.email%type,
       p_primary_contact in client.self_emp_ueb_app.primary_contact%type,
       p_secondary_contact in client.self_emp_ueb_app.secondary_contact%type,
       p_place_of_operation in client.self_emp_ueb_app.place_of_operation%type,
       p_island_of_operation in client.self_emp_ueb_app.island_of_operation%type,
       p_estimated_weekly_earnings in client.self_emp_ueb_app.estimated_weekly_earnings%type,
       p_user in client.self_emp_ueb_app.inserted_by%type,
       p_branch_number in client.self_emp_ueb_bank_info.branch_number%type,
       p_bank_code in client.self_emp_ueb_bank_info.bank_code%type,
       p_account_type in client.self_emp_ueb_bank_info.account_type%type,
       p_bank_account_number in client.self_emp_ueb_bank_info.bank_account_number%type,
       p_bank_info_status in client.self_emp_ueb_bank_info.status%type,
       p_app_id out client.self_emp_ueb_bank_info.app_id%type
) as
begin
  insert into client.self_emp_ueb_app
  (first_name,last_name,dob,eeni#,erni#,email,primary_contact,secondary_contact,place_of_operation,
   island_of_operation,estimated_weekly_earnings,status,inserted_by)
  values(p_first_name,p_last_name,to_date(p_dob,'YYYYMMDD'),p_eeni#,p_erni#,p_email,p_primary_contact,
         p_secondary_contact,p_place_of_operation,p_island_of_operation,p_estimated_weekly_earnings,
         'Pending',p_user);
         
  select client.self_emp_ueb_app_seq.currval into p_app_id from dual;
         
  insert into client.self_emp_ueb_bank_info
  (app_id,branch_number,bank_code,account_type,bank_account_number,
   status,inserted_by)
  values(p_app_id,p_branch_number,p_bank_code,
         p_account_type,p_bank_account_number,p_bank_info_status,p_user);
commit;
end;

