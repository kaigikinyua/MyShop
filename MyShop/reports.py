from views import UserView,TransactionView,PaymentView,SoldItemsView
class Reports:
    #daily reports
    def generateXReport(self,dateTimeStamp):
        pass

    def generateZReport(self,dateTimeStamp):
        pass

    def generateStockReport(self,startDate,endDate):
        pass

    def generateBusinessReport(self,startDate,endDate):
        pass

class CSV:
    @staticmethod
    def headers(headers,emptyStart):
        if(len(headers)>0):
            h=''
            if(emptyStart==True):
                h+=','
            for header in headers:
                h+=f'{str(header)},'
            return f'{h}\n'
        return False

    @staticmethod
    def rowData(two_D_array,numberedRow=False,emptyStart=True):
        if(len(two_D_array)>0):
            numRow=1
            d=''
            for row in two_D_array:
                if(emptyStart):
                    d=','
                if(numberedRow):
                    d=d+f'{str(numRow)},'
                for elm in row:
                    d=d+f'{elm},'
                d=d+'\n'
                numRow+=1
            return d
        
    @staticmethod
    def columData(header,data):
        dataString=f'{str(header)},'
        for d in data:
            dataString+=f'{str(data)},\n'
        return dataString

        
    @staticmethod
    def dataSheet(headers,data):
        headersString=CSV.headers(headers,True)
        dataString=CSV.rowData(data,True,False)
        dataSheet=headersString+dataString
        return dataSheet