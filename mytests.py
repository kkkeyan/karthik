import unittest
from selenium import webdriver
from myutils import MyUtils


class mytests(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.base_url = "https://mpower.tvo.org/educators/#/signup/"
        self.driver.get(self.base_url)
        self.myutils = MyUtils(self.driver)

#TC 1 : To verify the registration page elements , input parameters are passed for properties.py
    def test_registration_page_validation(self):
        self.myutils.log('Test 1 : Registration page validation')
        if self.myutils.chk_registration_page():
            if self.myutils.chk_registration_page_elements():
                self.myutils.log('Test 1 : Registration page validation - Test Passed')
                return True
        self.myutils.log('Test 1 : Registration page validation - Test Failed')
        return False

#TC 2 : To verify the registration page with valid inputs , input parameters are passed for properties.py
    def test_account_registration(self):
        self.myutils.log('Test 2 : Test new account registration')
        if self.myutils.do_new_registration():
            self.myutils.log('Test 2 : Test new account registration - Test Passed')
            return True
        self.myutils.log('Test 2 : Test new account registration - Test Failed')
        return False

#TC 3 : To verify the registration cancel and check navigation to home page upon cancel
    def test_account_registration_cancel(self):
        self.myutils.log('Test 3 : Test new account registration cancellation')
        if self.myutils.do_new_registration_cancel():
            self.myutils.log('Test 3 : Test new account registration cancellation - Test Passed')
            return True
        self.myutils.log('Test 3 : Test new account registration cancellation - Test Failed')
        return False

#TC 4 : To verify the mandatory fileds in the registration page
    def test_mandatoryfield_validation(self):
        self.myutils.log('Test 4 : Test new account registration')
        if self.myutils.chk_mandate_field_reg_form():
            self.myutils.log('Test 4 : Test new account registration - Test Passed')
            return True
        self.myutils.log('Test 4 : Test new account registration - Test Failed')
        return False

#TC 5 : To verify the registration by adding new school
    def test_add_new_school(self):
        self.myutils.log('Test 5  : Test registration with new school name')
        if self.myutils.registration_new_school():
            self.myutils.log('Test 5 : Test registration with new school name - Test Passed')
            return True
        self.myutils.log('Test 5 : Test registration with new school name - Test Failed')
        return False

#TC 6 :  To verify the registration page with invalid email id
    def test_registeration_invalid_emailid(self):
        self.myutils.log('Test 6 : Test registration with invalid emailid')
        if self.myutils.registration_invalid_emailid():
            self.myutils.log('Test 6 : Test registration with invalid emailid - Test Passed')
            return True
        self.myutils.log('Test 6 : Test registration with invalid emailid - Test Failed')
        return False

#TC 7 : To validate the name filed. test data and messages are read from an csv file
    def test_field_validation(self):
        self.myutils.log('Test 7  : Name Filed validation')
        if self.myutils.check_field_validation_from_csv():
            self.myutils.log('Test 7 : Name Filed validation - Test Passed')
            return True
        self.myutils.log('Test 7 : Name Filed validation - Test Failed')
        return False

#TC 8 : Test to check the error message when the role limit exceeds. pre-req is to have atleast three administrator
       # roles for a board/school
    def test_role_limit_exceeds(self):
        self.myutils.log('Test 8  : Test to check the error message when the role limit exceeds')
        if self.myutils.registration_limit_exceeded():
            self.myutils.log('Test 8 : Test to check the error message when the role limit exceeds - Test Passed')
            return True
        self.myutils.log('Test 8 : Test to check the error message when the role limit exceeds - Test Failed')
        return False

#TC 9 : Test to check the duplicate account reisteration.I assume that untill we validate the email
        #post registeration we will be able register a account with same details
        #used APIs for creating a account in the backend
    def test_duplicate_account_creation(self):
        self.myutils.log('Test 9  : Test to check the duplicate account creation')
        if self.myutils.check_duplicate_account_creation():
            self.myutils.log('Test 9  : Test to check the duplicate account creation - Test Passed')
            return True
        self.myutils.log('Test 9  : Test to check the duplicate account creation - Test Failed')
        return False

#TC 10 : click and check if all the legal links like terms of use, copyright.. are working properly
    def test_legal_links(self):
        self.myutils.log('Test 10  : Test for legal links')
        if self.myutils.check_all_legal_links():
            self.myutils.log('Test 10  : Test for legal links - Test Passed')
            return True
        self.myutils.log('Test 10  : Test for legal links - Test Failed')
        return False

    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest((mytests('test_registration_page_validation')))
    suite.addTest((mytests('test_account_registration')))
    suite.addTest((mytests('test_account_registration_cancel')))
    suite.addTest((mytests('test_mandatoryfield_validation')))
    suite.addTest((mytests('test_add_new_school')))
    suite.addTest((mytests('test_registeration_invalid_emailid')))
    suite.addTest((mytests('test_field_validation')))
    suite.addTest((mytests('test_role_limit_exceeds')))
    suite.addTest((mytests('test_duplicate_account_creation')))
    suite.addTest((mytests('test_legal_links')))
    unittest.TextTestRunner().run(suite)