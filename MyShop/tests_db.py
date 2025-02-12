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
        login1,token1,userLevel1,shiftId=u.login(u1['name'],u1['pass'])
        login2,token2,userLevel2,shiftId=u.login(u2['name'],u2['pass'])
        TestCase.assertEqual(self,login1,True)    
        TestCase.assertEqual(self,login2,False)
        if(login1==True,login2==False):
            print("Test:[Success] test_login()")
    
    def test_logout(self):
        u1={'name':'admin','pass':'admin12345'}
        u=UserView()
        activeSessions=u.get_UserActiveSessions(u1['name'])
        if(len(activeSessions)>0):
            user=u.getUser(u1['name'])
            u.logout(user.id)
        else:
            u.login(u1['name'],u1['pass'])
            user=u.getUser(u1['name'])
            u.logout(user.id)
        activeSessions=u.get_UserActiveSessions(u1['name'])
        TestCase.assertEqual(self,len(activeSessions),0)

    #test_authenticated can be skipped for now
    def test_isAuthenticated(self):
        user={'name':'admin','pass':'admin12345'}
        u=UserView()
        login,token,userLevel,shiftId=u.login(user['name'],user['pass'])
        if(login):
            userDetails=u.getUser(user['name'])
            result=u.is_authenticated(userDetails.id)
            TestCase.assertEqual(self,True,result)
            u.logout(userDetails.id)
            result=u.is_authenticated(userDetails.id)
            TestCase.assertEqual(self,False,result)
        else:
            print("Error: test_isAuthenticated() -> Could not login user")
            TestCase.assertEqual(self,True,False)

    def test_addUser(self):
        user={'name':'James','pass':'testpass12345','level':1}
        u=UserView()
        added,message=u.addUser(user['name'],user['pass'],user['level'])
        TestCase.assertEqual(self,added,True)
        added2,message=u.addUser(user['name'],user['pass'],user['level'])
        TestCase.assertEqual(self,added2,False)
        added3,message=u.addUser('TestUser','pa','admin')
        TestCase.assertEqual(self,added3,False)

    def test_updateUser(self):
        user={'name':'James','pass':'newPass','level':'cashier'}
        u=UserView()
        userDetails=u.getUser(user['name'])
        if(userDetails):
            reslutPass,message=u.updatePassword(userDetails.id,user['pass'])
            resultUpdateUserLevel,message=u.updateUserLevel(userDetails.id,user['level'])
            TestCase.assertEqual(self,reslutPass,True)
            TestCase.assertEqual(self,resultUpdateUserLevel,True)
        else:
            self.test_addUser()
            userDetails=u.getUser(user['name'])
            reslutPass,message=u.updatePassword(userDetails.id,user['pass'])
            TestCase.assertEqual(self,reslutPass,True)
            #resultUpdateUserLevel,message=u.updateUserLevel(userDetails.id,user['level'])
            #TestCase.assertEqual(self,resultUpdateUserLevel,True)
            self.test_deleteUser()
            
    def test_deleteUser(self):
        user={'name':'James','pass':'testpass12345','level':'admin'}
        u=UserView()
        userDetails=u.getUser(user['name'])
        deleted,message=u.deleteUser(userDetails.id)
        TestCase.assertEqual(self,deleted,True)
        deleted2,message=u.deleteUser(userDetails.id)
        TestCase.assertEqual(self,deleted2,False)
        deleted3,message=u.deleteUser(None)
        TestCase.assertEqual(self,deleted3,False)
    
class Test_ProductsView(unittest.TestCase):
    def test_addProduct(self):
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
        p1={'pMethod':'mpesa','pAmount':1000,'tId':'1','tNum':'fasdgasdg'}
        p2={'pMethod':'cash','pAmount':5000,'tId':'1','tNum':''}
        p3={'pMethod':'bank','pAmount':10000,'tId':'1','tNum':'34523452345'}
        payments=[p1,p2,p3]
        p=PaymentView()
        for payMent in payments:
            rslt,message=p.addPayment(payMent['pMethod'],payMent['pAmount'],payMent['tId'],payMent['tNum'])
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