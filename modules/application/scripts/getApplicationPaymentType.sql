select case
         when max(bank.bank_info_id) keep (dense_rank last order by bank.inserted_date) is null and max(app.island_of_operation) in ('GRAND BAHAMA','NEW PROVIDENCE') then
          case when max(app.sun_cash_opt_in) = 'No' then
               'Check'
          else
               'SUN'
          end
         when max(bank.account_owner) keep (dense_rank last order by bank.inserted_date) = 'No' and max(app.island_of_operation) in ('GRAND BAHAMA','NEW PROVIDENCE') then
          case when max(app.sun_cash_opt_in) = 'No' then
               'Check'
          else
               'SUN'
          end
         when max(bank.bank_info_id) keep (dense_rank last order by bank.inserted_date) is null then
           'Check'
         when max(bank.account_owner) keep (dense_rank last order by bank.inserted_date) = 'No' then --director requested that in situations where the applicant is not the owner of the bank account automatically generate a manaul check
           'Check'
         else
           'EFT'
       end "appPaymentType"
from client.self_emp_ueb_app app
left join client.self_emp_ueb_bank_info bank on bank.app_id = app.app_id and bank.status = 'Active'
left join client.self_emp_ueb_pmt_master pmt on pmt.app_id = app.app_id
left join client.self_emp_ueb_pmt_detail pmt_det on pmt_det.pmt_id = pmt.pmt_id
where app.app_id = :app_id