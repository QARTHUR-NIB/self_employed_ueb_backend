from modules.application.background_jobs.mailer.Email import Mass_Email

class Check_Run_Aborted_Email(Mass_Email):
    def __init__(self,template):
        self.recipient = "CJohnson@nib-bahamas.com,Ronnie.Mortimer@nib-bahamas.com,ASands@nib-bahamas.com,LKnowles@nib-bahamas.com"
        self.sender = "checkrun@nib-bahamas.com"
        self.subject = "Self Employed Government Assistance: Check Run Aborted"
        self.template = template
        Mass_Email.__init__(self,self.sender,self.recipient,self.subject,self.template)
 