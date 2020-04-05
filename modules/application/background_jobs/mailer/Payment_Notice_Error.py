from modules.application.background_jobs.mailer.Email import Mass_Email

class Payment_Notice_Error(Mass_Email):
    def __init__(self,template):
        self.recipient = "CJohnson@nib-bahamas.com,Ronnie.Mortimer@nib-bahamas.com,ASands@nib-bahamas.com,LKnowles@nib-bahamas.com,QArthur@nib-bahamas.com,DBethel@nib-bahamas.com"
        self.sender = "payment_notice@nib-bahamas.com"
        self.subject = "Self Employed Government Assistance: Payment Notification Process Aborted"
        self.template = template
        Mass_Email.__init__(self,self.sender,self.recipient,self.subject,self.template)
 