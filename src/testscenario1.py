from selenium import webdriver
import unittest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FlightTests(unittest.TestCase):
    def setUp(self):
        self.FROM = input("Enter a from airport: ")
        self.TO = input("Enter a to airport: ")
        self.DEPART_ON = input("Enter a depart on date format should be: 'DayOfWeek, D Month YYYY': ")
        self.RETURN_ON = input("Enter a return on date format should be: 'DayOfWeek, D Month YYYY': ")
        self.driver = webdriver.Chrome()
    
    def pickDate(self, dateType: str):
        if dateType == "DEPART_ON":
            departurePicker = self.driver.find_element(By.XPATH, "//*[@id='DepartureDate']")
            departurePicker.click()
            time.sleep(1)
            selectedDate = self.findDateElement(self.DEPART_ON)
            if selectedDate == None:
                print("Plase enter a valid date")
            else:
                self.driver.execute_script("arguments[0].click();", selectedDate)

        elif dateType == "RETURN_ON":
            returnOnPicker = self.driver.find_element(By.XPATH, "//*[@id='ReturnDate']")
            returnOnPicker.click()
            selectedDate = self.findDateElement(self.RETURN_ON)
            if selectedDate == None:
                print("Plase enter a valid date")
            else:
                self.driver.execute_script("arguments[0].click();", selectedDate)
    
    def findDateElement(self, dateValue: str):
        dates = self.driver.find_elements(By.CLASS_NAME, "CalendarDay")

        if len(dates) == 0:
            return None

        for date in dates:
            aria_label = date.get_attribute("aria-label")
            if dateValue in aria_label:
                return date
        
        forwardArrow = self.driver.find_element(By.XPATH, "//*[@id='FlightSearchForm']/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]")

        if forwardArrow == None:
            return None

        forwardArrow.click()
        return self.findDateElement(dateValue)
    
    def test_scenario1(self):
        self.driver.get("https://www.enuygun.com/")
        self.driver.maximize_window()
        fromElement = self.driver.find_element(By.XPATH, "//*[@id='OriginInput']")
        fromElement.send_keys(self.FROM)
        time.sleep(1)
        fromElement.send_keys(Keys.ENTER)
        toElement = self.driver.find_element(By.XPATH, "//*[@id='DestinationInput']")
        toElement.send_keys(self.TO)
        time.sleep(1)
        toElement.send_keys(Keys.ENTER)
        self.pickDate("DEPART_ON")
        time.sleep(1)
        self.pickDate("RETURN_ON")
        time.sleep(1)
        nonStopElement = self.driver.find_element(By.XPATH, "//*[@id='transitFilter']")
        nonStopElement.click()
        passengerInputElement = self.driver.find_element(By.XPATH, "//*[@id='FlightSearchForm']/div/div[3]/div[1]/button")
        passengerInputElement.click()
        time.sleep(1)
        increaseAdultPassengerCountElement = self.driver.find_element(By.XPATH, "//*[@id='FlightSearchForm']/div/div[3]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/button[2]")
        increaseAdultPassengerCountElement.click()
        time.sleep(0.5)
        increaseStudentPassengerCountElement = self.driver.find_element(By.XPATH, "//*[@id='FlightSearchForm']/div/div[3]/div[1]/div[3]/div[1]/div[1]/div[5]/div[2]/button[2]")
        increaseStudentPassengerCountElement.click()
        time.sleep(1)
        ticketTypeElement = self.driver.find_element(By.XPATH, "//*[@id='FlightSearchForm']/div/div[3]/div[1]/div[3]/div[1]/div[2]/div[2]/button")
        ticketTypeElement.click()
        time.sleep(1)
        okButtonElement = self.driver.find_element(By.XPATH, "//*[@id='FlightSearchForm']/div/div[3]/div[1]/div[3]/div[2]/button")
        okButtonElement.click()
        time.sleep(1)
        submitButtonElement = self.driver.find_element(By.XPATH, "//*[@id='FlightSearchForm']/div/div[3]/div[2]/button")
        submitButtonElement.click()

        referenceElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id='add-to-favorite-root']/div/button")
            )
        )

        self.assertIsNotNone(referenceElement)

if __name__ == '__main__':
    unittest.main()


        



