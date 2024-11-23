import sys,unittest
from unittest import TestCase
sys.path.insert(0,'../')


from views import UserView,TransactionView

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
        t1={'custId':'1','sellerId':'3','tillId':'WareHouse','saleAmount':20000,'paidAmount':18000}
        t2={'custId':'','sellerId':'0','tillId':'WareHouse','saleAmount':30000,'paidAmount':30000}
        
        transaction=TransactionView()
        t1_rslt=transaction.createTransaction(t1['custId'],t1['sellerId'],t1['tillId'],t1['saleAmount'],t1['paidAmount'])
        t2_rslt=transaction.createTransaction(t2['custId'],t2['sellerId'],t2['tillId'],t2['saleAmount'],t2['paidAmount'])
        TestCase.assertEqual(self,True,t1_rslt)
        TestCase.assertNotEqual(self,True,t2_rslt)
    def test_fetchTransactionById(self):
        pass
    def fetchAllTransactions(self):
        pass

if __name__=='__main__':
    unittest.main()