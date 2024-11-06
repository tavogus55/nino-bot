from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import time
from datetime import date

class SmartConnector:
    def __init__(self, config_file):
        self.config = config_file
        self.account_config = self.config['account']
        self.url_config = self.config['url']
        self.sleep_time = self.config['sleep_time']
        self.raspbeery = self.config['sleep_time']

    def logIn(self, driver):
        account_username = self.account_config['username']
        account_password = self.account_config['password']
        url_base = self.url_config['base']
        url_home = self.url_config['home']
        login_url = url_base + url_home

        driver.get(login_url)

        input_username = driver.find_element(By.ID, "nilogin")
        input_password = driver.find_element(By.ID, "nipasswd")

        input_username.send_keys(account_username)
        input_password.send_keys(account_password)

        login_button = driver.find_element(By.CLASS_NAME, "button1")
        login_button.click()

        return driver

    def getUnreadEmails(self, raspberrypi_mode):
        initialized_driver = webdriver.Chrome()

        if raspberrypi_mode:
            chrome_service = Service("/usr/bin/chromedriver")
            chrome_options = Options()
            chrome_options.binary_location = "/usr/bin/chromium-browser"
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

            initialized_driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

        driver = self.logIn(initialized_driver)

        url_base = self.url_config['base']
        url_workflow = self.url_config['mail']
        mailbox_url = url_base + url_workflow

        time.sleep(self.sleep_time)

        driver.get(mailbox_url)

        time.sleep(self.sleep_time)

        receive_button = driver.find_element(By.ID, "btnrecv")
        receive_button.click()
        time.sleep(self.sleep_time)
        filter_button = driver.find_element(By.ID, "btnstatusso")
        filter_button.click()
        time.sleep(self.sleep_time)
        unopened_button = driver.find_element(By.ID, "menustatusso_0")
        unopened_button.click()
        time.sleep(self.sleep_time)
        submit_button = driver.find_element(By.ID, "menustatusso_sbtn")
        submit_button.click()
        time.sleep(self.sleep_time)
        tbody = driver.find_element(By.XPATH, '/html/body/form/table[4]/tbody/tr/td[2]/div/div[2]/div[2]/table/tbody/tr/td/div/table/tbody')
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        total_rows = len(rows)
        if total_rows == 1 and "ありません" in rows[0].text:
            return 0

        return total_rows



    def inputLateArrival(self):
        initialized_driver = webdriver.Chrome()
        driver = self.logIn(initialized_driver)

        expenses_form_values_config = self.config['expensesFormValues']
        url_base = self.url_config['base']
        url_workflow = self.url_config['workflow']
        workflow_url = url_base + url_workflow
        work_destination_place = expenses_form_values_config['destinationPlace']

        time.sleep(self.sleep_time)

        driver.get(workflow_url)

        time.sleep(self.sleep_time)

        apply_button = driver.find_element(By.XPATH, "/html/body/form/table[4]/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div/button[1]")
        apply_button.click()

        absence_leave_button = driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div[2]/div[2]/table/tbody/tr[2]")
        absence_leave_button.click()

        time.sleep(self.sleep_time)

        application_approver_field = driver.find_element(By.XPATH, "/html/body/form/table[4]/tbody/tr/td/div[3]/div[2]/table/tbody/tr/td/table/tbody/tr[4]/td[2]/select")
        select_approver = Select(application_approver_field)
        select_approver.select_by_value("3")

        work_destination = driver.find_element(By.XPATH, "/html/body/form/table[4]/tbody/tr/td/div[3]/div[2]/table/tbody/tr/td/table/tbody/tr[5]/td[2]/input")
        work_destination.send_keys(work_destination_place)

        type_field = driver.find_element(By.XPATH, "/html/body/form/table[4]/tbody/tr/td/div[3]/div[2]/table/tbody/tr/td/table/tbody/tr[8]/td[1]/select")
        select_type = Select(type_field)
        select_type.select_by_value("8")

        # Get today's date
        today = date.today()
        # Format the date as YYYY/MM/DD
        formatted_date = today.strftime("%Y/%m/%d")
        application_date = driver.find_element(By.XPATH, "/html/body/form/table[4]/tbody/tr/td/div[3]/div[2]/table/tbody/tr/td/table/tbody/tr[8]/td[2]/span/input")
        application_date.send_keys(formatted_date)
        application_date.send_keys(formatted_date)

        time.sleep(self.sleep_time)

        start_time = driver.find_element(By.XPATH, "/html/body/form/table[4]/tbody/tr/td/div[3]/div[2]/table/tbody/tr/td/table/tbody/tr[9]/td[1]/input")
        start_time.send_keys("9:00")

        arrived_time = driver.find_element(By.XPATH, "/html/body/form/table[4]/tbody/tr/td/div[3]/div[2]/table/tbody/tr/td/table/tbody/tr[9]/td[3]/input")
        arrived_time.send_keys("9:35")

        arrived_time = driver.find_element(By.XPATH, "/html/body/form/table[4]/tbody/tr/td/div[3]/div[2]/table/tbody/tr/td/table/tbody/tr[8]/td[8]/div/div[1]/font/div")
        arrived_time.send_keys("text")

        continue_button = driver.find_element(By.XPATH, "/html/body/form/table[4]/tbody/tr/td/div[4]/div/button[2]")
        continue_button.click()

        input("Press enter after you submit")


    def inputExpenses(self):
        initialized_driver = webdriver.Chrome()
        driver = self.logIn(initialized_driver)

        expenses_form_values_config = self.config['expensesFormValues']
        url_base = self.url_config['base']
        url_expense = self.url_config['expense']
        dest_value = expenses_form_values_config['destinationValue']
        train_amount = expenses_form_values_config['trainAmount']
        departure_place = expenses_form_values_config['departurePlace']
        arrival_place = expenses_form_values_config['arrivalPlace']
        dest_place = expenses_form_values_config['destinationPlace']
        memo_text = expenses_form_values_config['memoText']

        expenses_url = url_base + url_expense

        time.sleep(self.sleep_time)

        driver.get(expenses_url)

        time.sleep(self.sleep_time)

        input_time_button = driver.find_element(By.CLASS_NAME, "btnInputExpense")
        input_time_button.click()

        time.sleep(self.sleep_time)

        expenses_input_destination = driver.find_element(By.XPATH,
                                                         "/html/body/div[3]/div[2]/div/div[2]/div[1]/table/tbody/tr/td[1]/div/select")
        expenses_input_amount = driver.find_element(By.XPATH,
                                                    "/html/body/div[3]/div[2]/div/div[2]/div[2]/div[2]/span/input")
        expenses_input_departure = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div[2]/div[4]/input[1]")
        expenses_input_arrival = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div[2]/div[4]/input[2]")
        expenses_input_one_two_way = driver.find_element(By.XPATH,
                                                         "/html/body/div[3]/div[2]/div/div[2]/div[4]/span/span/label/input")
        expenses_input_destination_name = driver.find_element(By.XPATH,
                                                              "/html/body/div[3]/div[2]/div/div[2]/div[4]/input[3]")
        expenses_input_memo = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div[2]/div[7]/input")

        select_destination = Select(expenses_input_destination)
        select_destination.select_by_value(dest_value)

        expenses_input_amount.send_keys(train_amount)
        expenses_input_departure.send_keys(departure_place)
        expenses_input_arrival.send_keys(arrival_place)
        expenses_input_one_two_way.click()
        expenses_input_destination_name.send_keys(dest_place)
        expenses_input_memo.send_keys(memo_text)

        time.sleep(self.sleep_time)

        save_button = driver.find_element(By.CLASS_NAME, "save_closedlg")
        save_button.click()

        time.sleep(self.sleep_time)