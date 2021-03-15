from selenium import webdriver
from time import sleep


def takeScreen(url):

    driver = webdriver.Chrome("/Users/baptistedugue/Desktop/chromedriver")
    driver.get('https://edtmobiliteng.wigorservices.net//WebPsDyn.aspx?action=posEDTBEECOME&serverid=C&Tel=baptiste.dugue&date=03/15/2021')
    sleep(1)

    driver.get_screenshot_as_file("feuhfgiue.png")
    driver.quit()
    print("end...")
