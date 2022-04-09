import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

urls_dict = {
    'https://www.investing.com/funds/amundi-msci-wrld-ae-c': 'amundi-msci-wrld-ae-c',
    'https://www.investing.com/etfs/ishares-global-corporate-bond-$': 'ishares-global-corporate-bond-$',
    'https://www.investing.com/etfs/db-x-trackers-ii-global-sovereign-5': 'db-x-trackers-ii-global-sovereign-5',
    'https://www.investing.com/etfs/spdr-gold-trust': 'spdr-gold-trust',
    'https://www.investing.com/indices/usdollar': 'usdollar'
}


def scrape_data():
    browser = webdriver.Chrome("chromedriver.exe")
    browser.maximize_window()
    browser.get('https://www.investing.com')

    try:
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#onetrust-accept-btn-handler'))).click()  # accept the website's privacy protocol
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#PromoteSignUpPopUp > div.right > i'))).click()  # close sign-up banner
    except TimeoutException:
        pass

    dfs = []

    for url, asset in urls_dict.items():
        browser.get(url + str('-historical-data'))

        # change date
        try:
            browser.find_element(By.CSS_SELECTOR, '#widgetFieldDateRange').click()  # click date-button
            browser.find_element(By.CSS_SELECTOR, '#startDate').clear()
            browser.find_element(By.CSS_SELECTOR, '#startDate').send_keys('01/01/2020')
            browser.find_element(By.CSS_SELECTOR, '#endDate').clear()
            browser.find_element(By.CSS_SELECTOR, '#endDate').send_keys('12/31/2020')
            browser.find_element(By.CSS_SELECTOR, '#applyBtn').click()  # apply date changes

            try:
                element = browser.find_element(By.CSS_SELECTOR, '#closeIconHit')
                if element.is_displayed():
                    element.click()  # cancel pop-up video
            except Exception:
                pass

            WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#curr_table')))

            priced_df = pd.read_html(browser.find_element(By.CSS_SELECTOR, "#curr_table").get_attribute('outerHTML'))[0]  # scrape the price data
            csv_name = r'{}.csv'.format(asset)  # name the csv file based on the asset
            priced_df.to_csv(csv_name)  # save csv file

            dfs.append(priced_df)

        except ElementClickInterceptedException:
            WebDriverWait(browser, 10).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#PromoteSignUpPopUp > div.right > i'))).click()  # close sign-up banner
            continue
    return dfs


dfs = scrape_data()  # call the function
for df in dfs:
    df.describe()
