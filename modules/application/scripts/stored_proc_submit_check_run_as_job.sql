create or replace procedure client.execute_se_ueb_check_run(
  success out varchar,
  message out varchar
)
as
  job_exists varchar(1);
begin
  success := 'N';
  job_exists := 'N';
  
  select case when count(*) <= 0 then 'N' else 'Y' end into job_exists
  from all_scheduler_jobs job
  where job.job_name = 'se_ueb_check_run';  
  
  if job_exists = 'N' then
      dbms_scheduler.create_job (  
                job_name      =>  'se_ueb_check_run',  
                job_type      =>  'PLSQL_BLOCK',  
                job_action    =>  'begin client.create_se_ueb_checks; end;',  
                start_date    =>  sysdate,  
                enabled       =>  TRUE,  
                auto_drop     =>  TRUE,  
                comments      =>  'one-time job'
                );
      success := 'Y';
      message := null;
  else
    success := 'N';
    message := 'Check Run is already in progress';      
  end if;
  
exception
  when others then
    success := 'N';
    message := 'SQL Code:'||SQLCODE||'-'||SQLERRM;
end;
