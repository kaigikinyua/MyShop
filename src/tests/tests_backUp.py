'''
Unit/Module tests for the following
modules.backUp.py
    BackUp, Server
'''
import unittest
from unittest import TestCase
from modules.backUp import BackUp,Server

class TestBackUp(unittest.TestCase):
    def test_runDataBaseBackUp(self):
        pass

    def test_runLogsBackUp(self):
        pass

    def test_backUpDirectory(self):
        pass

    def test_backUpFile(self):
        pass


class TestPostServer(unittest.TestCase):
 
    def test_postData(self):
        data,state=Server.postData('api/items','new item')
        self.assertEqual(state,True)
        self.assertNotEqual(data,{'key':'value'})


class TestGetServer(unittest.TestCase):
    def test_getData(self):
        data,state=Server.getData('api/items')
        self.assertEqual(state,True)
        self.assertNotEqual(data,[])

    def test_postFiles(self):
        pass



if __name__=='__main__':
    unittest.main()