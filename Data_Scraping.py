import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

urls_dict = {
    'https://www.investing.com/funds/amundi-msci-wrld-ae-c': 'Stocks',
    'https://www.investing.com/etfs/ishares-global-corporate-bond-$': 'Corporate_bonds',
    'https://www.investing.com/etfs/db-x-trackers-ii-global-sovereign-5': 'Public_bonds',
    'https://www.investing.com/etfs/spdr-gold-trust': 'Gold',
    'https://www.investing.com/indices/usdollar': 'Cash'
}


def scrape_data():
    browser = webdriver.Chrome(r'C:\Users\User\PycharmProjects\projectUpm\chromedriver.exe')

    browser.get('https://www.investing.com')

    try:
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#onetrust-accept-btn-handler'))).click()  # accept the website's privacy protocol
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#PromoteSignUpPopUp > div.right > i'))).click()  # close sign-up banner
    except TimeoutException:
        pass

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
                browser.find_element(By.CSS_SELECTOR, '#closeIconHit').click()  # cancel pop-upvideo
            except Exception:
                pass

            WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#curr_table')))

            priced_df = pd.read_html(browser.find_element_by_css_selector("#curr_table").get_attribute('outerHTML'))[
                0]  # scrape the price data
            csv_name = r'pricedata_{}.csv'.format(asset)  # name the csv file based on the asset
            priced_df.to_csv(csv_name)  # save csv file

            print(priced_df)

            return priced_df

        except ElementClickInterceptedException:
            WebDriverWait(browser, 10).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#PromoteSignUpPopUp > div.right > i'))).click()  # close sign-up banner
            continue


df = scrape_data()  # call the function

df.describe()