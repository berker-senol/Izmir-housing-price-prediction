import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class RemovingPopUp(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.s = Service("C:\Program Files (x86)\chromedriver.exe")
        cls.driver = webdriver.Chrome(service=cls.s)
        cls.driver.get("https://www.sahibinden.com/en/for-sale-flat/izmir-karsiyaka-nergiz-dedebasi-mh.")
        cls.driver.find_element(by=By.XPATH, value="//*[@id='onetrust-accept-btn-handler']").click()
        time.sleep(1)
        cls.driver.find_element(by=By.XPATH, value="/html/body/div[13]/div[2]").click()

    def test_main_page_pop_ups_closer(self):
        """This method checks whether the pop-ups are closed in the main page"""

        check_list = WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located(
        (By.CLASS_NAME, "searchResultsItem")))
        self.assertIsNotNone(check_list)

    def test_page_end_controller(self):
        "This method checks whether the controller clicks second tab"
        buttons = self.driver.find_elements(by=By.CLASS_NAME, value="prevNextBut")
        self.assertEqual(buttons[0].text, "Next")

    def test_apartment_attributes(self):
        "This method checks the apartment attributes"

        check_list = WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located(
        (By.CLASS_NAME, "searchResultsItem")))
        check_list[0].click()

        apartment_name =self.driver.find_element(
        by=By.XPATH, value="//*[@id='classifiedDetail']/div/div[1]/h1")
        apartment_m_2_gross = self.driver.find_element(
        by=By.XPATH, value="//*[@id='classifiedDetail']/div/div[2]/div[2]/ul/li[5]/span")
        apartment_m_2_net = self.driver.find_element(
        by=By.XPATH, value="//*[@id='classifiedDetail']/div/div[2]/div[2]/ul/li[6]/span")
        apartment_age_of_building = self.driver.find_element(
        by=By.XPATH, value="//*[@id='classifiedDetail']/div/div[2]/div[2]/ul/li[8]/span")
        apartment_floor_number = self.driver.find_element(
        by=By.XPATH, value="//*[@id='classifiedDetail']/div/div[2]/div[2]/ul/li[9]/span")
        apartment_number_of_bathrooms = self.driver.find_element(
        by=By.XPATH, value="//*[@id='classifiedDetail']/div/div[2]/div[2]/ul/li[12]/span")
        apartment_number_of_rooms = self.driver.find_element(
        by=By.XPATH, value="//*[@id='classifiedDetail']/div/div[2]/div[2]/ul/li[7]/span")
        apartment_heating = self.driver.find_element(
        by=By.XPATH, value="//*[@id='classifiedDetail']/div/div[2]/div[2]/ul/li[11]/span")
        apartment_price = self.driver.find_element(
        by=By.XPATH, value="//*[@id='classifiedDetail']/div/div[2]/div[2]/h3")

        for element in ["user-info-store-name", "storeInfo", "username-info-area"]:   
            try:
                apartment_seller = self.driver.find_element(by=By.CLASS_NAME, value=element)
            except NoSuchElementException:
                pass
        
        self.assertEqual(apartment_name.text, "KARŞIYAKA NERGİSTE SATILIK DUBLEX DAİRE")
        self.assertEqual(apartment_m_2_gross.text, "125")
        self.assertEqual(apartment_m_2_net.text, "110")
        self.assertEqual(apartment_age_of_building.text, "0")
        self.assertEqual(apartment_floor_number.text, "4")
        self.assertEqual(apartment_number_of_bathrooms.text, "2")
        self.assertEqual(apartment_number_of_rooms.text, "3+1")
        self.assertEqual(apartment_heating.text, "Central Heating Boilers")
        self.assertEqual(apartment_price.text, "1,610,000 TL\nCredit Offers")
        self.assertEqual(apartment_seller.text, "ÖNDER GAYRİMENKUL")

        self.driver.execute_script('window.history.go(-1)')
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()


if __name__ == "__main__":
    unittest.main()