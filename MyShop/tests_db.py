import sys,unittest
from unittest import TestCase
sys.path.insert(0,'../')


from utils import FormatTime
from views import UserView,TransactionView,PaymentView

class Tests_UserView(unittest.TestCase):
    def test_login(self):
        u1={'name':'admin','pass':'admin12345'}
        u2={'name':'admin','pass':'adm12345'}
        u=UserView()
        login1,token1,userLevel1=u.login(u1['name'],u1['pass'])
        login2,token2,userLevel2=u.login(u2['name'],u2['pass'])
        TestCase.assertEqual(self,login1,True)    
        TestCase.assertEqual(self,login2,False)
        if(login1==True,login2==False):
            print("Test:[Success] test_login()")
    
    def test_logout(self):
        u1={'name':'admin','pass':'admin12345'}
        u=UserView()
        if(len(u.get_UserActiveSessions(u1['name']))>0):
            user=u.getUser(u1['name'])
            u.logout(user.id)
        else:
            u.login(u1['name'],u1['pass'])
            user=u.getUser(u1['name'])
            u.logout(user.id)
        activeSessions=u.get_UserActiveSessions(u1['name'])
        TestCase.assertEqual(self,len(activeSessions),0)
        if(len(activeSessions)==0):
            print("Test:[Success] test_logout()")
    
    #test_authenticated can be skipped for now
    def test_isAuthenticated(self):
        pass

    def test_addUser(self):
        pass
    def test_deleteUser(self):
        pass
    def test_updateUser(self):
        pass
    def test_updatePassword(self):
        pass

class Tests_TransactionView(unittest.TestCase):
    def test_createTransaction(self):
        t1={'succ':True,'custId':'1','sellerId':'3','tillId':'WareHouse','saleAmount':20000,'paidAmount':18000}
        t2={'succ':False,'custId':'','sellerId':'0','tillId':'WareHouse','saleAmount':30000,'paidAmount':30000}
        t3={'succ':True,'custId':'1','sellerId':'3','tillId':'WareHouse','saleAmount':15000,'paidAmount':15000}
        all_transactions=[t1,t2,t3]
        transactions=[]
        counter=1
        for t in all_transactions:
            tr=TransactionView()
            if(tr.fetchTransactionById(counter)==None):
                transactions+=[t]
            counter+=1

        for t in transactions:
            transaction=TransactionView()
            rslt=transaction.createTransaction(t['custId'],t['sellerId'],t['tillId'],t['saleAmount'],t['paidAmount'])
            TestCase.assertEqual(self,t['succ'],rslt)

    def test_fetchTransactionById(self):
        t=TransactionView()
        transaction=t.fetchTransactionById(1)
        print(transaction)

    def fetchAllTransactions(self):
        pass

class Tests_PaymentView(unittest.TestCase):
    def test_addPayment(self):
        p1={'pMethod':'mpesa','pAmount':1000,'tId':'1'}
        p2={'pMethod':'cash','pAmount':5000,'tId':'1'}
        p3={'pMethod':'bank','pAmount':10000,'tId':'1'}
        payments=[p1,p2,p3]
        p=PaymentView()
        for payMent in payments:
            rslt,message=p.addPayment(payMent['pMethod'],payMent['pAmount'],payMent['tId'])
            if(rslt==False):
                print(f'Payment failed {payMent} -> {message}')
        payments=p.fetchTransactionPayments('0')
        TestCase.assertGreaterEqual(self,len(payments),0)
    
    def test_fetchAllPayments(self):
        p1={'startTime':FormatTime.toTimeStamp(2024,10,3,0,0,0),'endtime':FormatTime.now()}
        #p2={'startTime':[2024,10,3,0,0,0],'endtime':FormatTime.now()}
        p=PaymentView()
        allTransactions=p.fetchAllPayments(None,None)
        rangeTransactions=p.fetchAllPayments(p1['startTime'],p1['endtime'])
        TestCase.assertEqual(self,len(allTransactions),len(rangeTransactions))        
if __name__=='__main__':
    unittest.main()