create or replace procedure client.create_se_ueb_checks as
total_benefit_weeks number(1) := 8;
max_weekly_benefit decimal(16,2) := 200;
pay_cycle_weeks number(1) := 2;
current_pay_period date;
nxt_pmt_id number(20);
benefit_pmt_amt decimal(16,2) := 0;
sum_det_pmt decimal(16,2) := 0;
min_pay_period date;
max_pay_period date;
nxt_pay_date date;
pay_up_to_date date;

cursor approved_app_payments is
  select app.app_id,max(pmt.last_paid_date) keep (dense_rank last order by pmt.inserted_date) last_payment_date,
         nvl(max(pmt.next_pay_date) keep (dense_rank last order by pmt.inserted_date),app.approval_date) next_payment_date,
         count(pmt_det.pmt_det_id) num_weeks_paid,
         case 
           when max(bank.bank_info_id) keep (dense_rank last order by bank.inserted_date) is null then
             'Check'
           else
             'EFT'
         end payment_type,
         app.eeni#
  from client.self_emp_ueb_app app
  left join client.self_emp_ueb_bank_info bank on bank.app_id = app.app_id and bank.status = 'Active'
  left join client.self_emp_ueb_pmt_master pmt on pmt.app_id = app.app_id
  left join client.self_emp_ueb_pmt_detail pmt_det on pmt_det.pmt_id = pmt.pmt_id
  where app.status = 'Approved'
  group by app.app_id,app.approval_date,app.eeni#;
  
payment_record approved_app_payments%rowtype;

-- Gets Weekly Benefit Payment Information

begin
  for payment_record in approved_app_payments loop
    if payment_record.next_payment_date > current_date then
      continue; --move onto next record becasuse appliaction is not yet in payment
    else
      pay_up_to_date := payment_record.next_payment_date + (pay_cycle_weeks * 7);
      
      select client.self_emp_ueb_pmt_master_seq.nextval into nxt_pmt_id from dual; --get value of next_pmt_id
      --create shell for payment header
      insert into client.self_emp_ueb_pmt_master
      (pmt_id,app_id,pmt_date,pmt_type,status)
      values(nxt_pmt_id,payment_record.app_id,current_date,payment_record.payment_type,'Pending');
      commit;
      
      loop
        while payment_record.next_payment_date < pay_up_to_date loop
          if payment_record.num_weeks_paid = total_benefit_weeks then
            exit;
          end if;
          
          --get weekly benefit payment info
          select weekly_payment_amt into benefit_pmt_amt
          from(
          select
                sum(nvl(case w_m_ind
                         when 'W' then
                           gross_amount
                         when 'M' then
                           (gross_amount * 12) / 52
                         end 
                        ,0)
                    ) weekly_payment_amt
          from(
          select p.alt_identifier,
                 case pa.pension_plan_code
                   when 'SB' then
                     'W'
                   when 'INDUSTRIAL_SURVIVOR' then
                     'M'
                   when 'SICKASSIST' then
                     'W'
                   when 'RETIREMENT' then
                     'M'
                   when 'DISABLE_BENEFIT' then
                     'M'
                   when 'INJURY' then
                     'W'
                   when 'SURV' then
                     'M'
                   when 'OLD' then
                     'M'   
                   when 'UNEMP' then
                     'W'
                   when 'METBEN' then
                     'W'  
                  end w_m_ind,                    
                 ds.gross_amount,
                 ds.start_date,
                 case ds.pay_until
                   when 'A' then
                     add_months(p.birth_date,(ds.pay_until_age * 12))
                   when 'UD' then
                     trunc(add_months(current_date,12))
                   when 'D' then
                     ds.stop_date
                  end
                  end_date
          from dbo.person p
          inner join dbo.business_entity_key bek on bek.alt_key_code = p.alt_identifier
          left join dbo.v_pension_application_q pa on pa.owner_business_entity_key_id = bek.business_entity_key_id
           and pa.pension_plan_code not in ('B67_CLAIM','INVALIDITY','INVALASSIST','FUNERAL','RET_ESTIMATE','REFUND')
          left join dbo.disburse_schedule ds on ds.source_key = pa.application_id and ds.source_entity = 350
               and ds.sched_status = 'A' and lower(ds.schedule_name) not like '%retro%' 
               and lower(ds.schedule_name) not like '%dependent%'
               and nvl(ds.stop_date,current_date + 1) > current_date --if stop date is empty assume claimant is still being paid
          where p.alt_identifier = payment_record.eeni#
          )
          where payment_record.next_payment_date between start_date and end_date
          );
                   
          insert into client.self_emp_ueb_pmt_detail pmt_det
          (pmt_id,assistance_amount,benefit_penalty_amount,pmt_amt,beg_pay_period,end_pay_period)
          values(nxt_pmt_id,max_weekly_benefit,benefit_pmt_amt,(max_weekly_benefit - benefit_pmt_amt),
                 payment_record.next_payment_date,payment_record.next_payment_date + 7);
          commit;
          payment_record.next_payment_date := payment_record.next_payment_date + (7); --increments date by 7 days (1 week)
          payment_record.num_weeks_paid := payment_record.num_weeks_paid + 1;                                                       
        end loop;
       
        if pay_up_to_date < current_date then
          payment_record.next_payment_date := pay_up_to_date;
          pay_up_to_date := pay_up_to_date + (pay_cycle_weeks * 7);
        else
          exit;
        end if;
      end loop;
      
      select sum(pmt_det.pmt_amt),min(pmt_det.beg_pay_period),max(pmt_det.end_pay_period)
             into sum_det_pmt,min_pay_period,max_pay_period
      from client.self_emp_ueb_pmt_detail pmt_det
      where pmt_det.pmt_id = nxt_pmt_id
      group by pmt_det.pmt_id;
      
      if payment_record.num_weeks_paid = total_benefit_weeks then
          update client.self_emp_ueb_app app
          set app.status = 'Completed'
          where app.app_id = payment_record.app_id;
          commit;
          nxt_pay_date := null;
      else
        nxt_pay_date := max_pay_period;
      end if;
                    
      --update header with the summary totals from the payment details
      update client.self_emp_ueb_pmt_master pmt
      set pmt.pmt_amt = sum_det_pmt,
          pmt.beg_pay_period = min_pay_period,
          pmt.end_pay_period = max_pay_period,
          pmt.last_paid_date = min_pay_period,
          pmt.next_pay_date = nxt_pay_date
      where pmt.pmt_id = nxt_pmt_id;
      commit;
      
    end if;  
  end loop;
exception
  when others then
     DBMS_OUTPUT.put_line('Error in '|| $$plsql_unit || ' at ' || $$plsql_line);
     DBMS_OUTPUT.put_line('SQL Code:'||SQLCODE||'-'||SQLERRM);
end;
