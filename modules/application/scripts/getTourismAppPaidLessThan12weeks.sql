select app.app_id "applicationID",app.first_name "firstName", app.last_name "lastName",
       app.dob "dob",app.eeni# "eeni", app.erni# "erni", app.email "email", app.primary_contact "primaryContact",
       app.secondary_contact "secondaryContact",app.place_of_operation "placeOfOperation", 
       app.island_of_operation "islandOfOperation", app.estimated_weekly_earnings "estimatedWeeklyEarnings",
       app.status "status", app.approval_date "approvalDate", app.inserted_date "insertedDate", app.inserted_by "insertedBy", app.denied_by "deniedBy",
       app.user_comment "userComment", app.denial_date "denialDate",app.nature_of_employment "natureOfEmployment",
       app.routed_to "routedTo",app.routed_date "routedDate", app.sun_cash_opt_in "sunCashOptIn",
       app.tourism_industry "tourismIndustryFlag", app.updated_by "updatedBy", app.updated_date "updatedDate", app.approved_by "approvedBy"
from client.self_emp_ueb_app app
left join client.self_emp_ueb_pmt_master pmt on pmt.app_id = app.app_id
left join client.self_emp_ueb_pmt_detail pmt_det on pmt_det.pmt_id = pmt.pmt_id
where app.status not in ('Denied','Pending')
 and app.tourism_industry = 'Yes'
group by app.app_id, app.first_name, app.last_name,
       app.dob, app.eeni#, app.erni#, app.email, app.primary_contact,
       app.secondary_contact,app.place_of_operation, 
       app.island_of_operation, app.estimated_weekly_earnings,
       app.status, app.approval_date, app.inserted_date,app.inserted_by, app.denied_by,
       app.user_comment, app.denial_date,app.nature_of_employment,
       app.routed_to,app.routed_date, app.sun_cash_opt_in,
       app.tourism_industry, app.updated_by,app.updated_date,app.approved_by
having count(pmt_det.pmt_det_id) < 12