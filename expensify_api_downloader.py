import requests
import json
import urllib

class ExpensifyAPI:
    def __init__(self,partnerUserID,partnerUserSecret):
        self.headers = {"Content-Type":"application/x-www-form-urlencoded",
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding":"gzip, deflate",
                "Accept-Language":"en-US,en;q=0.8,hr;q=0.6,es;q=0.4,zh;q=0.2,ja;q=0.2",
                "Cache-Control":"no-cache",
                "Connection":"keep-alive",
                "Content-Type":"application/x-www-form-urlencoded",
                "Host":"integrations.expensify.com",
                "Origin":"https://integrations.expensify.com",
                "Pragma":"no-cache",
                "Referer":"https://integrations.expensify.com/Integration-Server/index.html",
                "Upgrade-Insecure-Requests":"1",
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2560.0 Safari/537.36"
                }
        self.download_file ={
                "type":"download",
                "credentials":{
                    "partnerUserID":"",
                    "partnerUserSecret":""
                },
                "fileName":""
            }
        self.download_file['credentials']['partnerUserSecret'] = partnerUserSecret
        self.download_file['credentials']['partnerUserID'] = partnerUserID

        self.requestJobDescription ={
                "test":"true",
                "type":"file",
                "credentials":{
                    "partnerUserID":"",
                    "partnerUserSecret":""
                },
                "onReceive":{
                    "immediateResponse":["returnRandomFileName"]
                },
                "inputSettings":{
                    "type":"combinedReportData",
                    "reportState":"OPEN,SUBMITTED,APPROVED,REIMBURSED,ARCHIVED",
                    "filters":{
                        "startDate":"2015-1-1",
                        "markedAsExported":"Partner name"
                    }
                },
                "outputSettings":{
                    "fileExtension":"csv"
                },
                "onFinish":[
                    {"actionName":"markAsExported","label":"Partner name"}
                ]
        }
        self.requestJobDescription['credentials']['partnerUserID'] = partnerUserID
        self.requestJobDescription['credentials']['partnerUserSecret'] = partnerUserSecret

        self.template ="""<#-- Header -->Report ID,Merchant,Amount,Category,Expense Date
            <#list reports as report>
                <#list report.transactionList as expense>
                    ${report.reportID},<#t>
                    ${expense.merchant},<#t>
                    ${(expense.amount/100)?string("0.00")},<#t>
                    ${expense.category},<#t>
                    ${expense.created}<#lt>
                </#list>
            </#list>
        """
        self.api_endpoint = 'https://integrations.expensify.com/Integration-Server/ExpensifyIntegrations'


    def get_report_file_name(self,filetype,start_date):

        self.requestJobDescription['inputSettings']['filters']['startDate'] = start_date
        self.requestJobDescription['outputSettings']['fileExtension'] = filetype
        post_data = "requestJobDescription={}&template={}".format(urllib.quote_plus(json.dumps(self.requestJobDescription)),
                urllib.quote_plus(self.template))

        res = requests.post(self.api_endpoint,data = post_data,headers=self.headers)
        if res.status_code == 200:
            return res.text
        else:
            raise Exception("Request POST error")

    def download(self,filetype,start_date):
        filename = self.get_report_file_name(filetype,start_date)
        self.download_file['fileName'] = filename
        post_data = "requestJobDescription={}".format(urllib.quote_plus(json.dumps(self.download_file)),headers=self.headers)
        res = requests.post(self.api_endpoint,data = post_data,headers=self.headers)
        if res.status_code == 200:
            with open(filename,"w") as f:
                f.write(res.text)
        else:
            raise Exception("Request POST error")


if __name__=="__main__":
    api = ExpensifyAPI("aa_tmslav_gmail_com","d70360324fb29688cf34757b7fea8802f0397235")
    api.download("csv","2015-1-1")

