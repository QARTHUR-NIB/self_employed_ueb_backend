select alt_identifier,valid_first_name,valid_last_name,valid_dob,
       case
         when sum(weekly_payment_amt) < 200 then
           'N'
         else
           'Y'
       end weekly_pmt_amt_gte_200
from(
select alt_identifier,valid_first_name,valid_last_name,valid_dob,
       nvl(case w_m_ind
           when 'W' then
             gross_amount
           when 'M' then
             (gross_amount * 12) / 52
           end ,0) weekly_payment_amt
from(
select p.alt_identifier,
       case when trim(lower(p.first_name)) <> trim(lower(:first_name)) then 'N' else 'Y' end valid_first_name,
       case when trim(lower(p.last_name)) <> trim(lower(:last_name)) then 'N' else 'Y' end valid_last_name,
       case when p.birth_date <> to_date(:dob,'YYYYMMDD') then 'N' else 'Y' end valid_dob,
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
       ds.gross_amount
from dbo.person p
inner join dbo.business_entity_key bek on bek.alt_key_code = p.alt_identifier
left join dbo.v_pension_application_q pa on pa.owner_business_entity_key_id = bek.business_entity_key_id
 and pa.pension_plan_code not in ('B67_CLAIM','INVALIDITY','INVALASSIST','FUNERAL','RET_ESTIMATE','REFUND')
left join dbo.disburse_schedule ds on ds.source_key = pa.application_id and ds.source_entity = 350
     and ds.sched_status = 'A' and lower(ds.schedule_name) not like '%retro%' 
     and lower(ds.schedule_name) not like '%dependent%'
     and nvl(ds.stop_date,current_date + 1) > current_date --if stop date is empty assume claimant is still being paid
where p.alt_identifier = :eeni
)
)
group by alt_identifier,valid_first_name,valid_last_name,valid_dob

