create or replace procedure client.create_se_ueb_app_bank_info(
       p_app_id in client.self_emp_ueb_bank_info.app_id%type,
       p_account_owner in client.self_emp_ueb_bank_info.account_owner%type,
       p_branch_number in client.self_emp_ueb_bank_info.branch_number%type,
       p_account_type in client.self_emp_ueb_bank_info.account_type%type,
       p_bank_account_number in client.self_emp_ueb_bank_info.bank_account_number%type,
       p_bank_info_status in client.self_emp_ueb_bank_info.status%type,
       p_user in client.self_emp_ueb_bank_info.inserted_by%type,
       p_success out varchar,
       p_message out varchar       
) as
begin
  --Set all existing bank accounts to Inactive
  update client.self_emp_ueb_bank_info b_info
  set b_info.status = 'Inactive'
  where b_info.status = 'Active'
   and b_info.app_id = p_app_id;
         
  insert into client.self_emp_ueb_bank_info
  (app_id,branch_number,account_type,bank_account_number,account_owner,
   status,inserted_by)
  values(p_app_id,p_branch_number,p_account_type,p_bank_account_number,p_account_owner,p_bank_info_status,p_user);
         
  p_success := 'Y';
  p_message := '';
  
commit;
exception
  when others then
    p_success := 'N';
    p_message := 'SQL Code:'||SQLCODE||'-'||SQLERRM;
end;
