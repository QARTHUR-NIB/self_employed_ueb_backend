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

cursor approved_app_payments is
  select app.app_id,nvl(max(pmt.last_paid_date) keep (dense_rank last order by pmt.inserted_date),app.approval_date) last_payment_date,
         nvl(max(pmt.next_pay_date) keep (dense_rank last order by pmt.inserted_date),app.approval_date) next_payment_date,
         count(pmt_det.pmt_det_id) num_weeks_paid,
         case 
           when max(bank.bank_info_id) keep (dense_rank last order by bank.inserted_date) is null then
             'Check'
           else
             'EFT'
         end payment_type
  from client.self_emp_ueb_app app
  left join client.self_emp_ueb_bank_info bank on bank.app_id = app.app_id and bank.status = 'Active'
  left join client.self_emp_ueb_pmt_master pmt on pmt.app_id = app.app_id
  left join client.self_emp_ueb_pmt_detail pmt_det on pmt_det.pmt_id = pmt.pmt_id
  where app.status = 'Approved'
  group by app.app_id,app.approval_date;
  
payment_record approved_app_payments%rowtype;

begin
  for payment_record in approved_app_payments loop
    if payment_record.next_payment_date > current_date then
      continue; --move onto next record becasuse appliaction is not yet in payment
    else
      
      select client.self_emp_ueb_pmt_master_seq.nextval into nxt_pmt_id from dual; --get value of next_pmt_id
      --create shell for payment header
      insert into client.self_emp_ueb_pmt_master
      (pmt_id,app_id,pmt_date,pmt_type,status)
      values(nxt_pmt_id,payment_record.app_id,current_date,payment_record.payment_type,'Pending');
      commit;
      
      while payment_record.next_payment_date < current_date loop
        if payment_record.num_weeks_paid = total_benefit_weeks then
          exit;
        end if;    
        current_pay_period := payment_record.last_payment_date;   
        while current_pay_period < payment_record.next_payment_date loop
          insert into client.self_emp_ueb_pmt_detail pmt_det
          (pmt_id,assistance_amount,benefit_penalty_amount,pmt_amt,beg_pay_period,end_pay_period)
          values(nxt_pmt_id,max_weekly_benefit,benefit_pmt_amt,(max_weekly_benefit - benefit_pmt_amt),
                 current_pay_period,current_pay_period + 7);
          commit;
          current_pay_period := current_pay_period + (7); --increments date by 7 days (1 week)
          payment_record.num_weeks_paid := payment_record.num_weeks_paid + 1;                                                       
        end loop;
        payment_record.last_payment_date := payment_record.next_payment_date;
        payment_record.next_payment_date := payment_record.last_payment_date + (pay_cycle_weeks * 7);
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
        nxt_pay_date := max_pay_period + (pay_cycle_weeks * 7);
      end if;
                    
      --update header with the summary totals from the payment details
      update client.self_emp_ueb_pmt_master pmt
      set pmt.pmt_amt = sum_det_pmt,
          pmt.beg_pay_period = min_pay_period,
          pmt.end_pay_period = max_pay_period,
          pmt.last_paid_date = max_pay_period,
          pmt.next_pay_date = nxt_pay_date
      where pmt.pmt_id = nxt_pmt_id;
      commit;
      
    end if;  
  end loop;
exception
  when others then
     DBMS_OUTPUT.put_line('SQL Code:'||SQLCODE||'-'||SQLERRM);
end;
