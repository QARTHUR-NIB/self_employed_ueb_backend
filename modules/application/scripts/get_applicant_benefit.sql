select app.app_id,pa.pension_plan_code || '-' || pa.pension_type_description
from client.self_emp_ueb_app app
inner join dbo.business_entity_key bek on bek.alt_key_code = app.eeni#
inner join dbo.v_pension_application_q pa on pa.owner_business_entity_key_id = bek.business_entity_key_id
 and pa.pension_plan_code not in ('B67_CLAIM','INVALIDITY','INVALASSIST','FUNERAL','RET_ESTIMATE','REFUND')
inner join dbo.disburse_schedule ds on ds.source_key = pa.application_id and ds.source_entity = 350
     and ds.sched_status = 'A' and lower(ds.schedule_name) not like '%retro%' 
     and lower(ds.schedule_name) not like '%dependent%'
where app.app_id = :app_id
group by app.app_id,pa.pension_plan_code,pa.pension_type_description

