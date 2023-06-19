from LoginWindow import *
import unittest

class unit_test(unittest.TestCase):

    def test_if_user_exists(self):
        self.assertTrue(MainWindow.if_user_exists("ayşe demir", "Kişi"))

    def test_get_sub_type(self):
        self.assertEqual(MainWindow.get_sub_type("can kaya", "Kişi"), "Aylık")

    def test_get_new_count_for_user(self):
        self.assertEqual(MainWindow.get_new_count_for_user("ece yıldız"), 5)

    
    def test_if_user_activated(self):
        self.assertTrue(MainWindow.if_user_activated("medilife innovations", "Şirket"))

    def test_did_user_bought_a_survey(self):
        self.assertTrue(MainWindow.did_user_bought_a_survey("barış şahin"))

    def test_does_media_exist(self):
        self.assertTrue(MainWindow.does_media_exist("Youtube"))


unittest.main()