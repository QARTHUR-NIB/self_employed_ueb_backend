/*
Author: Quincy Arthur
Date: March 19th, 2020
Description: Create DB for Self Employed UEB Application
*/

create table client.self_emp_ueb_app (
       app_id number(20) not null,
       first_name varchar(50) not null,
       last_name varchar(50) not null,
       dob date not null,
       eeni# varchar(8),
       erni# varchar(9),
       email varchar(250) not null,
       primary_contact varchar(250) not null,
       secondary_contact varchar(250),
       place_of_operation varchar(250),
       island_of_operation varchar(250),
       estimated_weekly_earnings decimal(16,2) default 0,
       document_location varchar(250),
       status varchar(10) not null check(status in ('Pending','Approved','Denied','Completed')),
       approval_date date,
       inserted_by varchar(10) not null,
       inserted_date timestamp default current_timestamp,
       updated_by varchar(10),
       updated_date timestamp,
       approved_by varchar(25),
       denied_by varchar(25),
       user_comment varchar(250),
       denial_date date     
)
/
create table client.self_emp_ueb_bank_info (
       bank_info_id number(20) not null,
       app_id number(20) not null,
       branch_number varchar(20) not null,
       account_type varchar(10) not null check(account_type in ('Savings','Checking')), 
       bank_account_number varchar(25) not null,
       account_owner varchar(3) not null check(account_owner in ('Yes','No')),
       status varchar(10) not null check(status in ('Active','Inactive')),
       inserted_by varchar(10) not null,
       inserted_date timestamp default current_timestamp
)
/
create sequence client.self_emp_ueb_app_seq start with 1 increment by 1 order;
/
create sequence client.self_emp_ueb_bank_info_seq start with 1 increment by 1 order;
/
alter table client.self_emp_ueb_app add(
      constraint app_pk primary key (app_id)
)
/
alter table client.self_emp_ueb_bank_info add(
      constraint bank_info_pk primary key (bank_info_id)
)
/
alter table client.self_emp_ueb_bank_info add(
      constraint app_fk foreign key (app_id) references client.self_emp_ueb_app (app_id)
)
/
create or replace trigger client.app_gen_id 
before insert on client.self_emp_ueb_app
for each row
begin
  select client.self_emp_ueb_app_seq.NEXTVAL
  into   :new.app_id
  from   dual;
end;
/
create or replace trigger client.bank_info_gen_id 
before insert on client.self_emp_ueb_bank_info
for each row
begin
  select client.self_emp_ueb_bank_info_seq.NEXTVAL
  into   :new.bank_info_id
  from   dual;
end;
/
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
       p_account_owner in client.self_emp_ueb_bank_info.account_owner%type,
       p_branch_number in client.self_emp_ueb_bank_info.branch_number%type,
       p_account_type in client.self_emp_ueb_bank_info.account_type%type,
       p_bank_account_number in client.self_emp_ueb_bank_info.bank_account_number%type,
       p_bank_info_status in client.self_emp_ueb_bank_info.status%type,
       p_bank_info_exist boolean,
       p_app_id out client.self_emp_ueb_bank_info.app_id%type,
       p_success out varchar,
       p_message out varchar
       
) as
begin
  insert into client.self_emp_ueb_app
  (first_name,last_name,dob,eeni#,erni#,email,primary_contact,secondary_contact,place_of_operation,
   island_of_operation,estimated_weekly_earnings,status,inserted_by)
  values(p_first_name,p_last_name,to_date(p_dob,'YYYYMMDD'),p_eeni#,p_erni#,p_email,p_primary_contact,
         p_secondary_contact,p_place_of_operation,p_island_of_operation,p_estimated_weekly_earnings,
         'Pending',p_user);
         
  select client.self_emp_ueb_app_seq.currval into p_app_id from dual;
  
  if p_bank_info_exist then
    insert into client.self_emp_ueb_bank_info
    (app_id,branch_number,account_type,bank_account_number,account_owner,
     status,inserted_by)
    values(p_app_id,p_branch_number,p_account_type,p_bank_account_number,p_account_owner,p_bank_info_status,p_user);
  end if;
         
  p_success := 'Y';
  p_message := '';
  
commit;
exception
  when others then
    p_success := 'N';
    p_message := 'SQL Code:'||SQLCODE||'-'||SQLERRM;
end;
/
create or replace procedure client.create_se_ueb_app_bank_info(
       p_app_id in client.self_emp_ueb_bank_info.app_id%type,
       p_branch_number in client.self_emp_ueb_bank_info.branch_number%type,
       p_account_type in client.self_emp_ueb_bank_info.account_type%type,
       p_bank_account_number in client.self_emp_ueb_bank_info.bank_account_number%type,
       p_bank_info_status in client.self_emp_ueb_bank_info.status%type,
       p_account_owner in client.self_emp_ueb_bank_info.account_owner%type,
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
/
create table client.self_emp_ueb_pmt_master(
       pmt_id number(20) not null,--pk
       app_id number(20) not null, --fk
       pmt_date date not null,
       pmt_type varchar(5) not null check(pmt_type in ('Check','EFT')),
       pmt_amt decimal(16,2) default 0,
       beg_pay_period date,
       end_pay_period date,
       last_paid_date date,
       next_pay_date date,
       status varchar(10) not null check(status in ('Pending','Paid','Voided','Reissued')),
       inserted_by varchar(10) default 'SYSTEM',
       inserted_date timestamp default current_timestamp,
       updated_by varchar(10),
       updated_date timestamp default current_timestamp
)
/
create table client.self_emp_ueb_pmt_detail (
        pmt_det_id number(20) not null,--pk
        pmt_id number(20) not null,--fk
        assistance_amount decimal(16,2) not null,
        benefit_penalty_amount decimal(16,2) default 0,
        pmt_amt decimal(16,2) not null check(pmt_amt > 0),
        beg_pay_period date not null,
        end_pay_period date not null
)
/
alter table client.self_emp_ueb_pmt_master add(
      constraint pmt_mas_pk primary key (pmt_id),
      constraint pmt_mas_fk foreign key (app_id) references client.self_emp_ueb_app (app_id)
)
/
alter table client.self_emp_ueb_pmt_detail add(
      constraint pmt_det_pk primary key (pmt_det_id),
      constraint pmt_det_fk foreign key (pmt_id) references client.self_emp_ueb_pmt_master (pmt_id)
)
/
create sequence client.self_emp_ueb_pmt_master_seq start with 1 increment by 1 order;
/
create sequence client.self_emp_ueb_pmt_detail_seq start with 1 increment by 1 order;
/
create or replace trigger client.ueb_pmt_detail_gen_id 
before insert on client.self_emp_ueb_pmt_detail
for each row
begin
  select client.self_emp_ueb_pmt_detail_seq.NEXTVAL
  into   :new.pmt_det_id
  from   dual;
end;
