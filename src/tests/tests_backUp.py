'''
Unit/Module tests for the following
modules.backUp.py
    BackUp, Server
'''
import unittest
from unittest import TestCase
from unittest.mock import patch
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
 
    def test_getData(self):
        data,state=Server.getData('api/items')
        self.assertEqual(state,True)
        self.assertNotEqual(data,[])
        print(data)

    @patch('modules.backUp.requests.post')
    def test_postData(self,mock_post):
        mock_post.return_value={"data":"data from server"},True

        data,state=Server.postData('api/items','new item')
        self.assertEqual(state,True)
        self.assertEqual(data,{"data":"data from server"})

    @patch('modules.backUp.requests.get')
    def test_getData2(self,mock_get):
        mock_get.return_value={'data':'data from server'},True

        data,state=Server.getData('api/items')
        self.assertEqual(state,True)
        self.assertNotEqual(data,[])

    def test_postFiles(self):
        pass



if __name__=='__main__':
    unittest.main()