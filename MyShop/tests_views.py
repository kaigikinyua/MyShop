import unittest,sys
from unittest import TestCase
sys.path.insert(0,'../')

from utils import FormatTime
from views import UserView,ShiftView,TransactionView,PaymentView,ProductsView

class TestData:
    userTestData={
        'testLogin':[
            {'succ':True,'name':'admin','pass':'admin12345'},
            {'succ':False,'name':'admin','pass':'admin4551'},
        ],
        'testCreate':[
            {'succ':True,'name':'jim','pass':'testJim12345','id':None,'level':1},
            {'succ':False,'name':'jim','pass':'testJim12345','id':None,'level':1},
            {'succ':False,'name':'jim2','pass':'','id':None,'userLevel':1},
            {'succ':True,'name':'jim2','pass':'testJim12345','id':None,'level':1},
            {'succ':False,'name':'','pass':'','id':None,'level':1},
            {'succ':False,'name':None,'pass':None,'id':None,'level':1}
        ],

    }
    products=[
            {'name':'Test Product 001','barCode':'500000001','tags':'tusker','desc':'500ml','bPrice':300,'sPrice':500,'returnContainers':False},
            {'name':'Test Product 002','barCode':'500000002','tags':'tusker','desc':'500ml','bPrice':300,'sPrice':500,'returnContainers':True},
            {'name':'Test Product 003','barCode':'500000003','tags':'tusker','desc':'500ml','bPrice':300,'sPrice':500,'returnContainers':False},
            {'name':'Test Product 004','barCode':'500000004','tags':'tusker','desc':'500ml','bPrice':300,'sPrice':500,'returnContainers':True},
            {'name':'Test Product 005','barCode':'500000005','tags':'tusker','desc':'500ml','bPrice':300,'sPrice':500,'returnContainers':False},
        ]
    customerData={'name':'TestCustomer','phone':'07564115X','id':None,'credit':0}
    transactionData=[
        {
            'succ':True,
            "id":None,
            'custId':customerData['id'],
            'sellerId':'3',
            'tillId':'WareHouse',
            'saleAmount':20000,
            'paidAmount':18000,
            'paymentList':[
                {'pMethod':'mpesa','pAmount':1000,'tId':None,'tNum':'LKFJASLKDF;07265461'},
                {'pMethod':'cash','pAmount':5000,'tId':None,'tNum':''},
                {'pMethod':'bank','pAmount':10000,'tId':None,'tNum':'34523452345;KCB'},
                {'pMethod':'credit','pAmount':4000,'tId':None,'tNum':'11/11/2030;1'}
            ],
            'busketList':[
                {'barCode':products[0]['barCode'],'quantity':10,'price':products[0]['bPrice']},
                {'barCode':products[1]['barCode'],'quantity':15,'price':products[1]['bPrice']},
                {'barCode':products[2]['barCode'],'quantity':12,'price':products[2]['bPrice']},
                {'barCode':products[3]['barCode'],'quantity':5,'price':products[3]['bPrice']},
                {'barCode':products[4]['barCode'],'quantity':1,'price':products[4]['bPrice']},
                {'barCode':products[0]['barCode'],'quantity':1,'price':products[0]['bPrice']},
            ]
        },
        {
            'succ':False,
            "id":None,'custId':'',
            'sellerId':'3',
            'tillId':'WareHouse',
            'saleAmount':30000,
            'paidAmount':30000,
            'paymentList':[
                {'pMethod':'mpesa','pAmount':1000,'tId':None,'tNum':'LKFJASLKDF;07265461'},
                {'pMethod':'cash','pAmount':5000,'tId':None,'tNum':''},
                {'pMethod':'bank','pAmount':10000,'tId':None,'tNum':'34523452345;KCB'},
                {'pMethod':'credit','pAmount':4000,'tId':None,'tNum':'11/11/2030;1'}
            ],
            'busketList':[
                {'barCode':products[0]['barCode'],'quantity':10,'price':products[0]['bPrice']},
                {'barCode':products[1]['barCode'],'quantity':15,'price':products[1]['bPrice']},
                {'barCode':products[2]['barCode'],'quantity':12,'price':products[2]['bPrice']},
                {'barCode':products[3]['barCode'],'quantity':5,'price':products[3]['bPrice']},
                {'barCode':products[4]['barCode'],'quantity':1,'price':products[4]['bPrice']},
                {'barCode':products[0]['barCode'],'quantity':1,'price':products[0]['bPrice']},
            ]
        },
        {'succ':True,"id":None,'custId':'1','sellerId':'3','tillId':'WareHouse','saleAmount':15000,'paidAmount':15000}
    ]

class Tests_UserView(unittest.TestCase):
    def test_login(self):
        testUsers=TestData.userTestData['testLogin']
        u=UserView()
        for user in testUsers:
            login,token,userLevel,shiftId=u.login(user['name'],user['pass'])
            if(user['succ']):
                TestCase.assertEqual(self,login,True)
                TestCase.assertNotEqual(self,token,None)
                TestCase.assertNotEqual(self,userLevel,None)
                TestCase.assertNotEqual(self,shiftId,None)
            else:
                TestCase.assertEqual(self,login,False)
                TestCase.assertEqual(self,token,None)
                TestCase.assertEqual(self,userLevel,None)

    def test_logout(self):
        testUsers=TestData.userTestData['testLogin']
        u=UserView()
        for user in testUsers:
            logoutState=None
            activeSessions=u.get_UserActiveSessions(user['name'])
            if(len(activeSessions)>0):
                user=u.getUser(user['name'])
                u.logout(user.id)
            activeSessions=u.get_UserActiveSessions(user['name'])
            if(user['succ']==True):
                TestCase.assertEqual(self,len(activeSessions),0)
            else:
                TestCase.assertEqual(self,logoutState,False)

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
            print(f'User could not be logged in Error {shiftId}')
        TestCase.assertEqual(self,True,login)
        
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

class Test_ShiftView(unittest.TestCase):
    validUser=None
    openShiftId=None
    closedShiftId=None

    @classmethod
    def setUpClass(self):
        user=TestData.userTestData['testCreate'][0]
        u=UserView()
        createdUser,message=u.addUser(user['name'],user['pass'],user['level'])
        shift1_Id=ShiftView.createShiftId()
        shift2_Id=ShiftView.createShiftId()
        if(createdUser!=False):
            self.validUser=u.getUser(user['name'])
            shift1State,openShiftId=ShiftView.createShift(shift1_Id,self.validUser.id,False)
            shift2State,closedShiftId=ShiftView.createShift(shift2_Id,self.validUser.id,False)
            TestCase.assertEqual(shift1State,True)
            TestCase.assertEqual(shift1State,True)
            if(shift1State==True and shift2State==True):
                self.openShiftId=openShiftId
                self.closedShiftId=closedShiftId
        else:
            print(f"Could not create user=> Error {message}")
        TestCase.assertNotEqual(self,createdUser,False)
        TestCase.assertNotEqual(self,createdUser,None)

    def test_createShiftId(self):
        shiftId=ShiftView.createShiftId()
        TestCase.assertGreater(self,len(shiftId),0)

    def test_openShift(self):
        if(self.validUser!=None):
            openShift=ShiftView.openShift(self.validUser.id)
            TestCase.assertEqual(self,1,len(openShift))
            closingShift=ShiftView.closeShift(openShift[0].shiftId)
            newOpenShift=ShiftView.openShift(self.validUser.id)
            TestCase.assertNotEqual(self,False,newOpenShift)
            TestCase.assertNotEqual(self,None,newOpenShift)
            TestCase.assertNotEqual(self,openShift,newOpenShift)
            TestCase.assertEqual(self,closingShift,True)
            self.openShiftId=newOpenShift

    def test_shiftIsOpen(self):
        if(self.openShiftId!=None and self.closedShiftId!=None):
            openS=ShiftView.shiftIsOpen(self.openShiftId)
            closedS=ShiftView.shiftIsOpen(self.closedShiftId)
            TestCase.assertEqual(self,True,openS)
            TestCase.assertEqual(self,False,closedS)

    #should run as the last function to clean up the database entries by Test_ShiftView
    def test_deleteShift(self):
        if(self.openShiftId!=None and self.closedShiftId!=None):
            delShift1,messageShift1=ShiftView.deleteShift(self.openShiftId)
            delShift2,messageShift2=ShiftView.deleteShift(self.closedShiftId)
            TestCase.assertEqual(self,delShift1,True)
            TestCase.assertEqual(self,delShift2,True)
            print(f'Cleaning up Shifts Tests: Deleted messages \n{messageShift1}\n{messageShift2}')
            u=UserView()
            u.deleteUser(self.validUser.id)
class Test_ProductsView(unittest.TestCase):

    idStart=10000000
    def test_addProduct(self):
        i=self.idStart
        productStates=[]
        x=ProductsView()
        for p in TestData.products:
            pState=x.addProduct(i,p['name'],p['barCode'],p['tags'],p['desc'],p['bPrice'],p['sPrice'],p['returnContainers'])
            i=i+1
            productStates.append(pState)

    def test_getProductsById(self):
        i=self.idStart
        products=[]
        x=ProductsView()    
        for p in TestData.products:
            pState=x.getProductById(i)
            i=i+1
            self.assertNotEqual(self,pState,False)
            products.append(pState)

    def test_getProductsByBarCode(self):
        i=self.idStart
        products=[]
        x=ProductsView()    
        for p in TestData.products:
            pState=x.getProductByBarCode(p['barCode'])
            i=i+1
            self.assertNotEqual(self,pState,False)
            products.append(pState)

    def test_deleteProduct(self):
        i=self.idStart
        deletedProductStates=[]
        x=ProductsView()    
        for p in TestData.products:
            pState=x.deleteProduct(i)
            i=i+1
            deletedProductStates.append(pState)

class Tests_TransactionView(unittest.TestCase):
    t1={'succ':True,"id":None,'custId':'1','sellerId':'3','tillId':'WareHouse','saleAmount':20000,'paidAmount':18000}
    t2={'succ':False,"id":None,'custId':'','sellerId':'0','tillId':'WareHouse','saleAmount':30000,'paidAmount':30000}
    t3={'succ':True,"id":None,'custId':'1','sellerId':'3','tillId':'WareHouse','saleAmount':15000,'paidAmount':15000}
    all_transactions=[t1,t2,t3]
    def test_createTransaction(self):    
        all_transactions=self.all_transactions
        transactions=[]
        tView=TransactionView()
        counter=0
        for t in all_transactions:
            rslt,tId=tView.createTransaction(t['custId'],t['sellerId'],t['tillId'],t['saleAmount'])
            TestCase.assertEqual(self,t['succ'],rslt)
            t["id"]=tId
            all_transactions[counter]=t
            counter=counter+1

    def test_fetchTransactionById(self):
        t=TransactionView()
        transaction=t.fetchTransactionById(1)
        print(transaction)

    def test_deleteTransaction(self):
        tView=TransactionView()
        all_transactions=[self.t1,self.t2,self.t3]
        for t in all_transactions:
            state,error=tView.deleteTransaction(t["id"])
            TestCase.assertEqual(self,state,t['succ'])
        
class Tests_PaymentView(unittest.TestCase):
    p1={'pMethod':'mpesa','pAmount':1000,'tId':None,'tNum':'LKFJASLKDF;07265461'}
    p2={'pMethod':'cash','pAmount':5000,'tId':None,'tNum':''}
    p3={'pMethod':'bank','pAmount':10000,'tId':None,'tNum':'34523452345;KCB'}
    p4={'pMethod':'credit','pAmount':4000,'tId':None,'tNum':'11/11/2030;1'}
    all_payments=[p1,p2,p3]
    def test_addPayment(self):
        t=Tests_TransactionView.t1
        tView=TransactionView()
        tState,tId=tView.createTransaction(t['custId'],t['sellerId'],t['tillId'],t['saleAmount'])

        paymentTime=FormatTime.now()
        p=PaymentView()

        for payMent in self.all_payments:
            rslt,message=p.addPayment(payMent['pMethod'],payMent['pAmount'],tId,payMent['tNum'],paymentTime)
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

    def test_deletePayments(self):
        pass

class Tests_CustomerCreditView(unittest.TestCase):

    def test_addCredit(self):
        pass

if __name__=='__main__':
    unittest.main()