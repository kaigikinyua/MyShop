import unittest,sys
from unittest import TestCase

from utils import FormatTime
from views import UserView,ShiftView,CustomerView,TransactionView,PaymentView,ProductsView

class TestData:
    userTestData={
        'testLogin':[
            {'succ':True,'name':'admin','pass':'admin12345'},
            {'succ':False,'name':'admin','pass':'admin4551'},
        ],
        'testCreate':[
            {'succ':True,'name':'jimmy1','pass':'testJim12345','id':None,'level':1},
            {'succ':False,'name':None,'pass':None,'id':None,'level':1},
            {'succ':False,'name':'','pass':'','id':None,'level':1},
            {'succ':False,'name':'jim','pass':'','id':None,'level':1},
            {'succ':False,'name':'jimmy2','pass':'tes','id':None,'level':1},
            {'succ':False,'name':'jimmy3','pass':'','id':None,'level':1},
            {'succ':True,'name':'jimmy4','pass':'testJim12345','id':None,'level':1},
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
            #everything ok should work
            'succ':True,
            "id":None,
            'custId':customerData['id'],
            'sellerId':'3',
            'tillId':'WareHouse',
            'saleAmount':20000,
            'paidAmount':18000,
            'paymentList':[
                {'succ':True,'pMethod':'mpesa','pAmount':1000,'tId':None,'tNum':'LKFJASLKDF;07265461'},
                {'succ':True,'pMethod':'cash','pAmount':5000,'tId':None,'tNum':''},
                {'succ':True,'pMethod':'bank','pAmount':10000,'tId':None,'tNum':'34523452345;KCB'},
                {'succ':True,'pMethod':'credit','pAmount':4000,'tId':None,'tNum':'11/11/2030;1'}
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
            'saleAmount':-30000,
            'paidAmount':30000,
            'paymentList':[
                #should fail because of buggy payment list
                {'pMethod':'mpesa','pAmount':None,'tId':None,'tNum':'LKFJASLKDF;07265461'},
                {'pMethod':'','pAmount':5000,'tId':None,'tNum':''},
                {'pMethod':'bank','pAmount':-10000,'tId':None,'tNum':'34523452345;KCB'},
                {'pMethod':'credit','pAmount':4000000000,'tId':None,'tNum':'11/11/2030;1'}
            ],
            'busketList':[
                #should fail because of buggy busket list
                {'barCode':products[0]['barCode'],'quantity':None,'price':products[0]['bPrice']},
                {'barCode':products[1]['barCode'],'quantity':'','price':products[1]['bPrice']},
                {'barCode':products[2]['barCode'],'quantity':-12,'price':products[2]['bPrice']},
                {'barCode':products[3]['barCode'],'quantity':5,'price':-1*products[3]['bPrice']},
                {'barCode':products[4]['barCode'],'quantity':0,'price':products[4]['bPrice']},
                {'barCode':-1*products[0]['barCode'],'quantity':1,'price':products[0]['bPrice']},
            ]
        },
        {
            'succ':False,
            "id":None,
            'custId':'1',
            'sellerId':'3',
            'tillId':'WareHouse',
            'saleAmount':15000,
            'paidAmount':15000,
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
        }
    ]

class Tests_UserView(unittest.TestCase):
    def test_login(self):
        testUsers=TestData.userTestData['testLogin']
        u=UserView()
        for user in testUsers:
            login,token,userLevel=u.login(user['name'],user['pass'])
            if(user['succ']):
                TestCase.assertEqual(self,login,True)
                TestCase.assertNotEqual(self,token,None)
                TestCase.assertNotEqual(self,userLevel,None)
            else:
                TestCase.assertEqual(self,login,False)
                TestCase.assertEqual(self,token,None)
                TestCase.assertEqual(self,type(userLevel),type('String'))

    def test_logout(self):
        testUsers=TestData.userTestData['testLogin']
        u=UserView()
        for user in testUsers:
            logoutState=None
            activeSessions=u.get_UserActiveSessions(user['name'])
            if(len(activeSessions)>0):
                userObject=u.getUser(user['name'])
                u.logout(userObject.id)
                activeSessions=u.get_UserActiveSessions(user['name'])
            if(user['succ']==True):
                TestCase.assertEqual(self,len(activeSessions),0)
            else:
                TestCase.assertEqual(self,logoutState,None)

    #test_authenticated can be skipped for now
    def test_isAuthenticated(self):
        testUsers=TestData.userTestData['testLogin']
        u=UserView()
        for user in testUsers:
            login,token,userLevel=u.login(user['name'],user['pass'])
            if(login and user['succ']):
                userDetails=u.getUser(user['name'])
                result=u.is_authenticated(userDetails.id)
                TestCase.assertEqual(self,True,result)
                u.logout(userDetails.id)
                result=u.is_authenticated(userDetails.id)
                TestCase.assertEqual(self,False,result)
            elif(login==False and user['succ']==True):
                print(f'User could not be logged in Error {userLevel}')
            elif(login==False and user['succ']==False):
                pass
            TestCase.assertEqual(self,user['succ'],login)

    def test_addUser(self):
        testUsers=TestData.userTestData['testCreate']
        u=UserView()
        for user in testUsers:
            added,message=u.addUser(user['name'],user['pass'],user['level'])
            if(added!=user['succ']):
                print(f'\ntest_addUser() Test data state is {user['succ']} but on adding user the state is {added} with message {message}\nUser data=>{user}')
            TestCase.assertEqual(self,added,user['succ'])

    def test_updateUser(self):
        testUsers=TestData.userTestData['testCreate']
        u=UserView()
        for user in testUsers:
            userDetails=u.getUser(user['name'])
            if(userDetails):
                reslutPass,message=u.updatePassword(userDetails.id,user['pass'])
                resultUpdateUserLevel,message=u.updateUserLevel(userDetails.id,user['level'])
                TestCase.assertEqual(self,reslutPass,user['succ'])
                TestCase.assertEqual(self,resultUpdateUserLevel,['succ'])
            
    def test_deleteUser(self):
        testUsers=TestData.userTestData['testCreate']
        u=UserView()
        for user in testUsers:
            userDetails=u.getUser(user['name'])
            deleted=False
            if(userDetails!=None):
                deleted,message=u.deleteUser(userDetails.id)
            if(user['succ']!=deleted):
                print(f'\ntest_deleteUser() Test data state is {user['succ']} but on deleting user the state is {deleted} with message {message}\nUser data=>{user}')
            TestCase.assertEqual(self,deleted,user['succ'])

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
            shift2State,closedShiftId=ShiftView.createShift(shift2_Id,self.validUser.id,True)
            #TestCase.assertEqual(self,shift1State,True)
            #TestCase.assertEqual(self,shift1State,True)
            if(shift1State==True and shift2State==True):
                self.openShiftId=openShiftId
                self.closedShiftId=closedShiftId
        else:
            print(f"Could not create user=> Error {message}")
        #TestCase.assertNotEqual(self,createdUser,False)
        #TestCase.assertNotEqual(self,createdUser,None)

    def test_createShiftId(self):
        shiftId=ShiftView.createShiftId()
        TestCase.assertGreater(self,len(shiftId),0)

    def test_openShift(self):
        if(self.validUser!=None):
            oShift=ShiftView.shiftIsOpen(self.openShiftId)
            cShift=ShiftView.shiftIsOpen(self.closedShiftId)
            TestCase.assertEqual(self,oShift,False)
            TestCase.assertEqual(self,cShift,False)

            openShift=ShiftView.openShift(self.validUser.id)
            TestCase.assertEqual(self,False,openShift)
            closingShift,message=ShiftView.closeShift(self.openShiftId)
            newOpenShift=ShiftView.openShift(self.validUser.id)
            
            TestCase.assertEqual(self,False,newOpenShift)
            TestCase.assertNotEqual(self,None,newOpenShift)
            TestCase.assertEqual(self,openShift,newOpenShift)
            TestCase.assertEqual(self,closingShift,True)
            self.openShiftId=newOpenShift

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

class Test_CustomerView(unittest.TestCase):
    
    def test_CRUD_Ops_Customer(self):
        customer=TestData.customerData
        c=CustomerView()
        createdCustomer=c.addCustomer(customer['name'],customer['phone'])
        TestCase.assertTrue(self,createdCustomer,True)
        cust=c.getCustomerByPhoneNumber(customer['phone'])
        TestCase.assertNotEqual(self,cust,None)
        TestCase.assertNotEqual(self,cust,False)
        cust=c.getCustomer(cust.id)
        TestCase.assertNotEqual(self,cust,None)
        TestCase.assertNotEqual(self,cust,False)
        allCustomers=c.getAllCustomers()
        TestCase.assertNotEqual(self,allCustomers,[])
        customerExists=c.customerAlreadyExists(customer['phone'])
        TestCase.assertEqual(self,customerExists,True)
        deletedCustomer=c.deleteCustomer(cust.id)
        TestCase.assertEqual(self,deletedCustomer,True)
        customerExists=c.customerAlreadyExists(customer['phone'])
        TestCase.assertEqual(self,customerExists,False)

class Tests_TransactionView(unittest.TestCase):
    t1=TestData.transactionData[0]
    t2=TestData.transactionData[1]
    t3=TestData.transactionData[2]
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
    p1=TestData.transactionData[0]['paymentList']
    p2=TestData.transactionData[1]['paymentList']
    p3=TestData.transactionData[2]['paymentList']
    all_payments=[p1,p2,p3]
    def test_addPayment(self):
        t=Tests_TransactionView.t1
        tView=TransactionView()
        tState,tId=tView.createTransaction(t['custId'],t['sellerId'],t['tillId'],t['saleAmount'])

        paymentTime=FormatTime.now()
        p=PaymentView()

        for payMentList in self.all_payments:
            for payMent in payMentList:
                rslt,message=p.addPayment(payMent['pMethod'],payMent['pAmount'],tId,payMent['tNum'],paymentTime)
                if(rslt==False):
                    print(f'Payment failed {payMent} -> {message}')
        payments=p.fetchTransactionPayments('0')
        TestCase.assertGreaterEqual(self,len(payments),0)
    
    def test_fetchAllPaymentsWithinPeriod(self):
        p1={'startTime':FormatTime.toTimeStamp(2024,10,3,0,0,0),'endtime':FormatTime.now()}
        #p2={'startTime':[2024,10,3,0,0,0],'endtime':FormatTime.now()}
        p=PaymentView()
        allTransactions=p.fetchAllPaymentsWithinPeriod(None,None)
        rangeTransactions=p.fetchAllPaymentsWithinPeriod(p1['startTime'],p1['endtime'])
        TestCase.assertEqual(self,len(allTransactions),len(rangeTransactions))        

    def test_deletePayments(self):
        pass

class Tests_CustomerCreditView(unittest.TestCase):

    def test_payCredit(self):
        pass

    def test_addCredit(self):
        pass

    def test_creditBalance(self):
        pass

    def test_calcTotalCustomerCredit(self):
        pass

    def test_isCustomerCreditWorthy(self):
        pass

    def test_fetchCreditById(self):
        pass

    def test_fetchCreditByCustomer(self):
        pass
    
class Tests_StockView(unittest.TestCase):
    pass

class StockHistoryView(unittest.TestCase):
    pass

class EmptiesView(unittest.TestCase):
    pass

class BranchesView(unittest.TestCase):
    pass

if __name__=='__main__':
    unittest.main()