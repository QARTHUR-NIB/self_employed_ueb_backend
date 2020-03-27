  select max(t.user_data.event_type) keep (dense_rank last order by t.user_data.event_timestamp)
  from sys.AQ$SCHEDULER$_EVENT_QTAB t
  where t.user_data.object_name = 'SE_UEB_CHECK_RUN'