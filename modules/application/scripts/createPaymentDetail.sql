insert into client.self_emp_ueb_pmt_detail pmt_det
(pmt_id,assistance_amount,benefit_penalty_amount,pmt_amt,beg_pay_period,end_pay_period)
values(:paymentID,:weeklyAssistanceAmount,:weeklyBenefitPenaltyAmount,:weeklyPaymentAmount,
       :beginingPaymentAmount,:endingPaymentAmount)