/*
Author: Quincy Arthur
Date: April 7th, 2019
Description: Drop DB for Installment Agreement Manager Application *DEVELOPMENT ONLY*
*/

alter table client.self_emp_ueb_bank_info
drop constraint app_fk;
/
alter table client.self_emp_ueb_pmt_master
drop constraint pmt_mas_fk;
/
alter table client.self_emp_ueb_pmt_detail
drop constraint pmt_det_fk;
/
alter table client.self_emp_ueb_app
drop constraint app_pk;
/
alter table client.self_emp_ueb_bank_info
drop constraint bank_info_pk;
/
alter table client.self_emp_ueb_pmt_master
drop constraint pmt_mas_pk;
/
alter table client.self_emp_ueb_pmt_detail
drop constraint pmt_det_pk;
/
drop sequence client.self_emp_ueb_app_seq;
/
drop sequence client.self_emp_ueb_bank_info_seq;
/
drop sequence client.self_emp_ueb_pmt_master_seq;
/
drop sequence client.self_emp_ueb_pmt_detail_seq;
/
drop table client.self_emp_ueb_bank_info;
/
drop table client.self_emp_ueb_app;
/
drop table client.self_emp_ueb_pmt_master;
/
drop table client.self_emp_ueb_pmt_detail;


