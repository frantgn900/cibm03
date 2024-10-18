from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from django.contrib.auth.models import User
import time

class MySeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)

        
        User.objects.create_superuser("isard", "isard@isardvdi.com", "pirineus")

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_create_user_and_check_permissions(self):
        
        self.selenium.get(f'{self.live_server_url}/admin/login/')
        username_input = self.selenium.find_element(By.NAME, "username")
        password_input = self.selenium.find_element(By.NAME, "password")
        username_input.send_keys("isard")
        password_input.send_keys("pirineus")
        self.selenium.find_element(By.XPATH, "//input[@value='Log in']").click()

        self.selenium.get(f'{self.live_server_url}/admin/auth/user/add/')
        username_input = self.selenium.find_element(By.NAME, "username")
        password_input = self.selenium.find_element(By.NAME, "password1")
        password_confirm_input = self.selenium.find_element(By.NAME, "password2")
        username_input.send_keys("new_staff")
        password_input.send_keys("Password123456!")
        password_confirm_input.send_keys("Password123456!")
        
        self.selenium.find_element(By.XPATH, "//input[@value='Save and continue editing']").click()

        
        staff_checkbox = self.selenium.find_element(By.ID, "id_is_staff")
        if not staff_checkbox.is_selected():
            staff_checkbox.click()

        select_element = Select(self.selenium.find_element(By.ID, "id_user_permissions_from"))
        select_element.select_by_visible_text("Polls | question | Can add question")
        self.selenium.find_element(By.ID, "id_user_permissions_add_link").click()

        select_element = Select(self.selenium.find_element(By.ID, "id_user_permissions_from"))
        select_element.select_by_visible_text("Polls | question | Can view question")
        self.selenium.find_element(By.ID, "id_user_permissions_add_link").click()

        self.selenium.find_element(By.NAME, "_save").click()

        self.selenium.get(f'{self.live_server_url}/admin/')
        self.selenium.find_element(By.XPATH, "//button[text()='Log out']").click()

        time.sleep(1)

        self.selenium.get(f'{self.live_server_url}/admin/login/')
        username_input = self.selenium.find_element(By.NAME, "username")
        password_input = self.selenium.find_element(By.NAME, "password")
        username_input.send_keys("new_staff")
        password_input.send_keys("Password123456!")
        self.selenium.find_element(By.XPATH, "//input[@value='Log in']").click()

        try:
            self.selenium.find_element(By.XPATH, "//a[text()='Users']")
            assert False, "Error: l'usuari pot veure Users"
        except NoSuchElementException:
            print("Ok l'usuari no pot veure Users")

        try:
            self.selenium.find_element(By.XPATH, "//a[text()='Questions']")
            print("Ok l'usuari pot veure Questions")
        except NoSuchElementException:
            print("Error: l'usuari no pot veure Questions")
