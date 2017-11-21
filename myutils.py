from selenium.webdriver.common.by import By
from properties import Locators
import logging
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import csv
import requests
import json

class MyUtils(object):
    def __init__(self, driver, base_url="https://mpower.tvo.org/educators/#/signup/"):
        self.base_url = base_url
        self.driver = driver
        self.wait = WebDriverWait(self.driver,10)

# to write log file
    def log(self, log_string):
        logging.basicConfig(filename="logfile.log", level=logging.INFO)
        logging.info(log_string)

# check elements of home page
    def chk_home_page(self):
        if self.driver.find_element(*Locators.mpower_logo):
            if self.driver.find_element(*Locators.register_id_homepage):
                return True
        else:
            self.log("Login page not found")
            return False

# check elements of registration page
    def chk_registration_page(self):
        if self.driver.find_element(*Locators.mpower_logo):
            if self.verify_text_in_page('Create Your FREE Account'):
                return True
        else:
            self.log("registration page not found")
            return False

# validate the elements of the registration page
    def chk_registration_page_elements(self):
        # check elements of registration page
        if not self.driver.find_element(*Locators.mpower_logo):
            self.log("unable to locate registration page logo ")
            assert False
        if not self.driver.find_element(*Locators.firstName_id):
            self.log("unable to locate first name field")
            assert False
        if not self.driver.find_element(*Locators.lastName_id):
            self.log("unable to locate last name field")
            assert False
        if not self.driver.find_element(*Locators.educatorRole_id):
            self.log("unable to locate Role locator")
            assert False
        if not self.driver.find_element(*Locators.board_id):
            self.log("unable to locate board locator")
            assert False
        self.select_board_from_dropdown() #select a board name for school dropdown to be visible
        if not self.driver.find_element(*Locators.school_id):
            self.log("unable to locate school id locator")
            assert False
        if not self.driver.find_element(*Locators.email_id):
            self.log("unable to locate email id locator")
            assert False
        if not self.driver.find_element(*Locators.userEmailConfirm_id):
            self.log("unable to locate email confirmation ocator")
            assert False
        if not self.driver.find_element(*Locators.userPassword_id):
            self.log("unable to locate password locator")
            assert False
        if not self.driver.find_element(*Locators.userPasswordConfirm_id):
            self.log("unable to locate password confimration locator")
            assert False
        if not self.driver.find_element(*Locators.source_id):
            self.log("unable to locate source locator")
            assert False
        if not self.driver.find_element(*Locators.source_other_id):
            self.log("unable to locate source other locator")
            assert False
        if not self.driver.find_element(*Locators.agreement_id):
            self.log("unable to locate agreement checkbox locator")
            assert False
        if not self.driver.find_element(*Locators.emailPromos_id):
            self.log("unable to locate email promotion checkbox locator")
            assert False
        if not self.driver.find_element(*Locators.registerSubmit_id):
            self.log("unable to locate submit button")
            assert False
        if not self.driver.find_element(*Locators.registerCancel_css):
            self.log("unable to locate cancel button")
            assert False
        return True

# To veirfy is a element is present within the given timeout
    def is_id_present(self, value):
        timeout = 3
        try:
            WebDriverWait(self.driver,timeout).until(EC.presence_of_element_located((By.ID,value)))
        except NoSuchElementException as e:
            self.log("locator %s is not available", value)
            return False
        return True

# To verify is a elemenet is present within the given timeout
    def is_present_css(self, value):
        timeout = 3
        try:
            WebDriverWait(self.driver,timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR,value)))
        except NoSuchElementException as e:
            self.log("locator %s is not available", value)
            return False
        return True

# To verify is a elemenet is present within the given timeout
    def element_is_present_xpath(self, value):
        timeout = 3
        try:
            WebDriverWait(self.driver,timeout).until(EC.presence_of_element_located((By.XPATH,value)))
        except NoSuchElementException as e:
            self.log("locator %s is not available", value)
            return False
        return True

# To verify is a elemenet is present within the given timeout
    def element_is_present(self, method, value):
        timeout = 3
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((method, value)))
        except NoSuchElementException as e:
            self.log("locator %s is not available", value)
            return False
        return True

#To enter first name
    def add_firstname(self, name=Locators.test_firstName):
        self.is_id_present(Locators.firstName_locator)
        self.driver.find_element_by_id(Locators.firstName_locator).clear()
        self.driver.find_element_by_id(Locators.firstName_locator).send_keys(name)
        return True

# To enter last  name
    def add_lastname(self, name=Locators.test_LastName):
        self.is_id_present(Locators.lastName_locator)
        self.driver.find_element_by_id(Locators.lastName_locator).clear()
        self.driver.find_element_by_id(Locators.lastName_locator).send_keys(name)
        return True

# To select role form the drop down
    def select_educator_role_from_dropdown(self, role=Locators.test_educatorRole):
        self.is_id_present(Locators.educatorRole_locator)
        locator = "//select[@id='"+Locators.educatorRole_locator+"']/option[text()='"+role+"']"
        self.driver.find_element_by_xpath(locator).click()
        return True

# select a board from the dropdown
    def select_board_from_dropdown(self, board=Locators.test_board_name):
        self.is_id_present(Locators.board_id_locator)
        locator = "//select[@id='"+Locators.board_id_locator+"']/option[text()='"+board+"']"
        self.driver.find_element_by_xpath(locator).click()
        return True

# select a school from the dropdown
    def select_school_from_dropdown(self, school=Locators.test_school_name):
        time.sleep(3)
        self.is_id_present(Locators.school_locator)
        locator = "//select[@id='"+Locators.school_locator+"']/option[text()='"+school+"']"
        self.driver.find_element_by_xpath(locator).click()
        return True

# enter email
    def add_email(self, email=Locators.test_valid_email_name):
        self.is_id_present(Locators.email_locator)
        self.driver.find_element_by_id(Locators.email_locator).clear()
        self.driver.find_element_by_id(Locators.email_locator).send_keys(email)
        return True

# enter email in the confirmation field
    def add_email_confirm(self, email=Locators.test_valid_email_name):
        self.is_id_present(Locators.userEmailConfirm_locator)
        self.driver.find_element_by_id(Locators.userEmailConfirm_locator).clear()
        self.driver.find_element_by_id(Locators.userEmailConfirm_locator).send_keys(email)
        return True

# enter password
    def add_password(self, password=Locators.test_valid_password):
        self.is_id_present(Locators.userPassword_locator)
        self.driver.find_element_by_id(Locators.userPassword_locator).clear()
        self.driver.find_element_by_id(Locators.userPassword_locator).send_keys(password)
        return True

# enter password confirmation
    def add_password_confirm(self, password=Locators.test_valid_password):
        self.is_id_present(Locators.userPasswordConfirm_locator)
        self.driver.find_element_by_id(Locators.userPasswordConfirm_locator).clear()
        self.driver.find_element_by_id(Locators.userPasswordConfirm_locator).send_keys(password)
        return True

# select source from the dropdown
    def select_source_from_dropdown(self, name=Locators.test_source_name):
        self.is_id_present(Locators.source_locator)
        locator = "//select[@id='"+Locators.source_locator+"']/option[text()='"+name+"']"
        self.driver.find_element_by_xpath(locator).click()
        return True

# click the agreement checkbox
    def select_agreement_checkbox(self):
        self.is_id_present(Locators.agreement_locator)
        self.driver.find_element_by_id(Locators.agreement_locator).click()
        self.driver.find_element_by_id(Locators.agreement_locator).is_selected()
        return True

# click register in the registration form
    def click_register(self):
        self.is_id_present(Locators.registerSubmit_locator)
        self.driver.find_element_by_id(Locators.registerSubmit_locator).click()
        return True

# click cancel in the registration form
    def click_cancel(self):
        self.is_present_css(Locators.registerCancel_locator)
        self.driver.find_element(By.CSS_SELECTOR, Locators.registerCancel_locator).click()
        return True

# to check if the registration is success
    def check_registration_success(self):
        timeout = 10
        text = "//*[contains(text(),'Thank you for registering')]"
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, text)))
        except TimeoutException:
            self.log("Timeout Exceeded")
            return False
        return True

#For adding a new account
    def do_new_registration(self, email = Locators.test_valid_email_name):
        if not self.add_firstname():
            self.log("Unable to add first name")
            assert False
        if not self.add_lastname():
            self.log("Unable to add last name")
            assert False
        if not self.select_educator_role_from_dropdown():
            self.log("unable to select educator role")
            assert False
        if not self.select_board_from_dropdown():
            self.log("unable to select school board")
            assert False
        if not self.select_school_from_dropdown():
            self.log("unable to select school")
            assert False
        if not self.add_email(email):
            self.log("Unable to add email")
            assert False
        if not self.add_email_confirm(email):
            self.log("Unable to add email confirmation")
            assert False
        if not self.add_password():
            self.log("Unable to add password")
            assert False
        if not self.add_password_confirm():
            self.log("Unable to add password confirmation")
            assert False
        if not self.select_source_from_dropdown():
            self.log("Unable to select source details")
            assert False
        if not self.select_agreement_checkbox():
            self.log("Unable to check the agremment checkbox")
            assert False
        self.click_register()
        if not self.check_registration_success():
            self.log("Navigation to success page failed")
        return True

# add a new account and cancel the form, check if goes to home page
    def do_new_registration_cancel(self):
        if not self.add_firstname():
            self.log("Unable to add first name")
            assert False
        if not self.add_lastname():
            self.log("Unable to add last name")
            assert False
        if not self.select_educator_role_from_dropdown():
            self.log("unable to select educator role")
            assert False
        if not self.select_board_from_dropdown():
            self.log("unable to select school board")
            assert False
        if not self.select_school_from_dropdown():
            self.log("unable to select school")
            assert False
        if not self.add_email():
            self.log("Unable to add email")
            assert False
        if not self.add_email_confirm():
            self.log("Unable to add email confirmation")
            assert False
        if not self.add_password():
            self.log("Unable to add password")
            assert False
        if not self.add_password_confirm():
            self.log("Unable to add password confirmation")
            assert False
        if not self.select_source_from_dropdown():
            self.log("Unable to select source details")
            assert False
        if not self.select_agreement_checkbox():
            self.log("Unable to check the agremment checkbox")
            assert False
        self.click_cancel()
        if not self.chk_home_page():
            self.log("Navigation to success page failed")
        return True

#check for the mandatory feilds of the registration form
    def chk_mandate_field_reg_form(self):
        if not self.chk_mandate_field_ByLocator(Locators.firstName_locator,Locators.firstname_error_message): assert False
        self.add_firstname() #add first name
        if not self.chk_mandate_field_ByLocator(Locators.lastName_locator,Locators.lastname_error_message): assert False
        self.add_lastname() #add last name
        if not self.chk_mandate_field_ByLocator(Locators.educatorRole_locator,Locators.role_error_message): assert False
        self.select_educator_role_from_dropdown() #select role
        if not self.chk_mandate_field_ByLocator(Locators.board_id_locator,Locators.board_error_message): assert False
        self.select_board_from_dropdown() #select board
        if not self.chk_mandate_field_ByLocator(Locators.board_id_locator,Locators.school_error_message): assert False
        self.select_school_from_dropdown() #select school
        if not self.chk_mandate_field_ByLocator(Locators.email_locator,Locators.email_error_message): assert False
        self.add_email() #add first name
        if not self.chk_mandate_field_ByLocator(Locators.emailPromos_locator,Locators.password_error_message): assert False
        self.add_password() #add first name
        if not self.chk_mandate_field_ByLocator(Locators.source_locator,Locators.source_error_message): assert False
        self.select_source_from_dropdown() #select source details
        if not self.chk_mandate_field_ByLocator(Locators.agreement_locator,Locators.agreement_error_message): assert False
        self.select_agreement_checkbox() #check agremment checkbox
        if not self.chk_mandate_field_ByLocator(Locators.userEmailConfirm_locator,Locators.email_mismatch_error): assert False
        self.add_email_confirm() #add email confirmation
        if not self.chk_mandate_field_ByLocator(Locators.userPasswordConfirm_locator,Locators.password_mismatch_error): assert False
        self.add_password_confirm() #add first nam
        self.click_register()
        if not self.check_registration_success():
            self.log("Navigation to success page failed")
        return True

#click register button and verify the error message
    def chk_mandate_field_ByLocator(self, locator, text):
        self.is_id_present(locator)
        self.click_register()
        if self.verify_text_in_page(text):
            return True

#To verify if a test is present in the web page
    def verify_text_in_page(self, text):
        _text = "//*[contains(text(),text)]"
        if not self.driver.find_element_by_xpath(_text):
            self.log("Given text %s not found", text)
            return False
        return True

#to try registration with invalid email
    def registration_invalid_emailid(self):
        if not self.add_firstname(): assert False
        if not self.add_lastname(): assert False
        if not self.select_educator_role_from_dropdown(): assert False
        if not self.select_board_from_dropdown(): assert False
        if not self.select_school_from_dropdown(): assert False
        if not self.add_email(Locators.test_invalid_email_name): assert False
        if not self.add_email_confirm(Locators.test_invalid_email_name): assert False
        if not self.add_password(): assert False
        if not self.add_password_confirm(): assert False
        if not self.select_source_from_dropdown(): assert False
        if not self.select_agreement_checkbox(): assert False
        self.click_register()
        if not self.verify_text_in_page(Locators.invalid_email_error_message): # verify the error message
            self.log("Invalid email error messsage is not found")
            assert False
        self.click_cancel()
        return True

    def add_new_school(self):
    #Method to add a new school
        self.element_is_present_xpath(Locators.add_new_school_locator)
        self.driver.find_element(By.LINK_TEXT, 'click here').click()
        self.is_id_present(Locators.new_school_text_locator)
        self.driver.find_element_by_id(Locators.new_school_text_locator).send_keys(Locators.test_new_school_name)
        return True

#register a new account by adding a new school
    def registration_new_school(self):
        if not self.add_firstname(): assert False
        if not self.add_lastname(): assert False
        if not self.select_educator_role_from_dropdown(): assert False
        if not self.select_board_from_dropdown(): assert False
        if not self.add_new_school():
            self.log('unable to add new school')
            assert False
        if not self.add_email(Locators.test_invalid_email_name): assert False
        if not self.add_email_confirm(Locators.test_invalid_email_name): assert False
        if not self.add_password(): assert False
        if not self.add_password_confirm(): assert False
        if not self.select_source_from_dropdown(): assert False
        if not self.select_agreement_checkbox(): assert False
        self.click_register()
        if not self.verify_text_in_page(Locators.invalid_email_error_message):
            self.log("Invalid email error messsage is not found")
            assert False
        self.click_cancel()
        return True

    def check_field_validation(self):
    # Field validation for the name field with invalid names
        if not self.chk_field_validation_ByLocator(Locators.firstName_locator,Locators.test_invalid_name, Locators.invalid_first_name_error_message):
            assert False
        if not self.chk_field_validation_ByLocator(Locators.lastName_locator,Locators.test_invalid_name, Locators.invalid_last_name_error_message):
            assert False
        self.click_cancel()
        return True

# for TC 7 - input data is taken by reading the csv file
    def check_field_validation_from_csv(self):
    # Feild validation for the name field with invalid names
        first_name_handle = csv.reader(open("input_data_file_lastname.csv"))
        last_name_handle = csv.reader(open("input_data_file_firstname.csv"))
        for row in first_name_handle:
            if not self.chk_field_validation_ByLocator(Locators.firstName_locator,row[0], row[1]):
                assert False
        for row in last_name_handle:
            if not self.chk_field_validation_ByLocator(Locators.lastName_locator,row[0],row[1]):
                assert False
        self.click_cancel()
        return True

# for enter the given value on the required text field and validate the error message
    def chk_field_validation_ByLocator(self, locator, name, error_text):
        self.is_id_present(locator)
        self.driver.find_element_by_id(locator).clear()
        self.driver.find_element_by_id(locator).send_keys(name)
        if not self.verify_text_in_page(error_text):
            return False
        self.driver.find_element_by_id(locator).clear()
        return True

# For Tc 8 - Try registration with the given values and check if the required error message is displayed
    def registration_limit_exceeded(self):
        if not self.add_firstname(): assert False
        if not self.add_lastname(): assert False
        if not self.select_educator_role_from_dropdown('Administrator'): assert False
        if not self.select_board_from_dropdown('Algoma DSB'): assert False
        if not self.select_school_from_dropdown('Anna McCrea Public School'): assert False
        if not self.add_email(Locators.test_invalid_email_name): assert False
        if not self.add_email_confirm(Locators.test_invalid_email_name): assert False
        if not self.add_password(): assert False
        if not self.add_password_confirm(): assert False
        if not self.select_source_from_dropdown(): assert False
        if not self.select_agreement_checkbox(): assert False
        self.click_register()
        if not self.verify_text_in_page('There are already 3 administrators in your school. Please choose another role.'):
            self.log("Invalid email error messsage is not found")
            assert False
        self.click_cancel()
        return True

# To register a account from the backend using the APIs
    def create_user_backend(self, email_id):
        url = 'https://mpower.tvo.org/api/educatorAPI.php/register'
        headers = {"Accept" : "*/*", "content-type" : "application/x-www-form-urlencoded; charset=UTF-8"}
        data = {"board" : "","schoolId" : "2239","source" : "Another_Educator",
                "educatorRoleId" : "4","boardId" : "72","lastName" : "test" , "password" : "test1@tdsb.on.ca",
                "firstName":"test","email": email_id,"sourceOther":"","agreement" : "true", "t":""}
        response = requests.post(url, data, headers) # post method
        if response.status_code == 200:
            output = json.loads(response.text)
            email = output['data']['email']
            if email == Locators.test_email_id:
                return True
        print "account creation failed"
        return False

#For TC 9 - creates two account to confimr duplication
    def check_duplicate_account_creation(self):
        #lets register a account first
        if not self.create_user_backend(Locators.test_email_id): return False
        # lets register a account from the UI
        if not self.do_new_registration(Locators.test_email_id): return False
        return True

#TC 10 - to test all the legal links available in the reg form
    def check_all_legal_links(self):
    #To check all the legal links are working properly
    # click and verify the Terms of use link
        if not self.click_link_veriy_text(By.LINK_TEXT,Locators.user_terms_link,Locators.user_terms_message):
            self.log("Verification of Terms of Use link failed")
            return False
    # click and verify the Privacy Policy link
        if not self.click_link_veriy_text(By.XPATH,Locators.privacy_policy_locator, Locators.privacy_policy_message):
            self.log("Verification of Privacy Policy link failed")
            return False
    # click and verify the copyright link
        if not self.click_link_veriy_text(By.LINK_TEXT,Locators.copyright_link, Locators.copyright_message):
            self.log("Verification of copyright link failed")
            return False
        return True

#clicks the given link and check for the given message
    def click_link_veriy_text(self, method, locator, text):
        time.sleep(1)
        self.driver.find_element(method, locator).click()
        if not self.verify_text_in_page(text):
            return False
        return True




