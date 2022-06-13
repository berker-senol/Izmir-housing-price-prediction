import time
from random import randint
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


# Time randomizer has been created
def random_time(short_time, long_time):
    rand_sleep_time = randint(short_time, long_time)
    return time.sleep(rand_sleep_time) 


# Gets the house list and checks if the ads pops up to house list and if it does, then discard it from the list 
def extra_ad_remover(driver):
    check_list = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located(
        (By.CLASS_NAME, "searchResultsItem")))
    try:
        pop_up_3 = driver.find_element(
        by=By.CLASS_NAME, value="classicNativeAd")
        check_list.remove(pop_up_3)
    except NoSuchElementException:
        pass 

    try:
        house_pop_up = driver.find_element(
            by=By.CLASS_NAME, value="searchResultsPromoSuper")
        if house_pop_up in check_list:
            check_list.remove(house_pop_up)
    except NoSuchElementException:
        pass
    return check_list


def main():
    # Driver object has been created by merging Selenium Webdriver and Service.
    s = Service("C:\Program Files (x86)\chromedriver.exe")
    driver = webdriver.Chrome(service=s)
    
    # Driver object got the internet site.Then the pop ups have been closed.
    driver.get("https://www.sahibinden.com/en/for-sale-flat/izmir-karsiyaka-nergiz-dedebasi-mh.")
    driver.find_element(by=By.XPATH, value="//*[@id='onetrust-accept-btn-handler']").click()
    random_time(1, 2)
    driver.find_element(by=By.XPATH, value="/html/body/div[13]/div[2]").click()

    # Created the necessary variables
    name, m_2_gross, m_2_net, age_of_building, floor_number = [], [], [], [], []
    number_of_bathrooms, number_of_rooms, heating, seller, price = [], [], [], [], []

    # Site Dependent values have been created
    total_ad_number = int((driver.find_element(by=By.CLASS_NAME, value="result-text").text).split()[0])
    house_num_per_page = int(driver.find_element(by=By.CLASS_NAME, value="Limit20").text)
    total_page = (total_ad_number // house_num_per_page) + 1
    

    # The Loop starts
    for _ in range(total_page):
        house_list = extra_ad_remover(driver)
        random_time(5, 6)
        for house_number in range(len(house_list)):
            house_list = extra_ad_remover(driver)   
            house_list[house_number].click()

            try:
                ad_name = driver.find_element(
                    by=By.XPATH, value="//*[@id='classifiedDetail']/div/div[1]/h1")
                ad_m_2_gross = driver.find_element(
                    by=By.XPATH, value="//*[@id='classifiedDetail']/div/div[2]/div[2]/ul/li[5]/span")
                ad_m_2_net = driver.find_element(
                    by=By.XPATH, value="//*[@id='classifiedDetail']/div/div[2]/div[2]/ul/li[6]/span")
                ad_age_of_building = driver.find_element(
                    by=By.XPATH, value="//*[@id='classifiedDetail']/div/div[2]/div[2]/ul/li[8]/span")
                ad_floor_number = driver.find_element(
                    by=By.XPATH, value="//*[@id='classifiedDetail']/div/div[2]/div[2]/ul/li[9]/span")
                ad_number_of_bathrooms = driver.find_element(
                    by=By.XPATH, value="//*[@id='classifiedDetail']/div/div[2]/div[2]/ul/li[12]/span")
                ad_number_of_rooms = driver.find_element(
                    by=By.XPATH, value="//*[@id='classifiedDetail']/div/div[2]/div[2]/ul/li[7]/span")
                ad_heating = driver.find_element(
                    by=By.XPATH, value="//*[@id='classifiedDetail']/div/div[2]/div[2]/ul/li[11]/span")
                ad_price = driver.find_element(
                    by=By.XPATH, value="//*[@id='classifiedDetail']/div/div[2]/div[2]/h3")

                for element in ["user-info-store-name", "storeInfo", "username-info-area"]:   
                    try:
                        ad_seller = driver.find_element(by=By.CLASS_NAME, value=element)
                    except NoSuchElementException:
                        pass
                    
                name.append(ad_name.text)
                m_2_gross.append(ad_m_2_gross.text)
                m_2_net.append(ad_m_2_net.text)
                age_of_building.append(ad_age_of_building.text)
                floor_number.append(ad_floor_number.text)
                number_of_bathrooms.append(ad_number_of_bathrooms.text)
                number_of_rooms.append(ad_number_of_rooms.text)
                heating.append(ad_heating.text)
                seller.append(ad_seller.text)
                price.append(ad_price.text)
            
            except NoSuchElementException:
                pass

            driver.execute_script('window.history.go(-1)')
            random_time(3,4)

            if (house_number + 1)==len(house_list) :
                # Gets all the element/s (Previous and Next button)
                buttons = driver.find_elements(by=By.CLASS_NAME, value="prevNextBut")
                # If it has 1 button and is equal to 20 then it is at the first page.
                if (len(buttons)==1 and len(house_list)==house_num_per_page):
                    buttons[0].click()
                # If it has 2 buttons then it has previous and next buttons and we need to next button.
                elif len(buttons) == 2:
                    buttons[1].click()
                # If we are at the last page then finish the loop.
                else:
                    print("Search is finished")
                    
            random_time(4,6)        
    
    # Writing the values as DataFrames
    df = pd.DataFrame(
        {"name": name,
        "m_2_gross": m_2_gross,
        "m_2_net": m_2_net,
        "age_of_building":age_of_building,
        "floor_number":floor_number,
        "number_of_bathrooms":number_of_bathrooms,
        "number_of_rooms":number_of_rooms,
        "heating":heating,
        "seller":seller,
        "price":price})

    df.to_excel("Dedebaşı.xlsx", sheet_name="1")
    driver.quit()

if __name__ == "__main__":
    main()