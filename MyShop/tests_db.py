import unittest
from unittest import TestCase

from views import UserView

class Tests_DB_User(unittest.TestCase):
    def test_login(self):
        u1={'name':'admin','pass':'admin12345'}
        u2={'name':'admin','pass':'adm12345'}
        u=UserView()
        login1=u.login(u1['name'],u1['pass'])
        login2=u.login(u2['name'],u2['pass'])
        TestCase.assertEqual(self,login1,True)    
        TestCase.assertEqual(self,login2,False)
        if(login1==True,login2==False):
            print("Test:[Success] test_login()")
    
    def test_logout(self):
        pass
    
    def test_isAuthenticated(self):
        pass

if __name__=='__main__':
    unittest.main()