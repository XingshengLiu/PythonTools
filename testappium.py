import time
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

desired_caps={}

desired_caps['platformName']='Android'
desired_caps['platformVersion']='9.0'
desired_caps['deviceName']='127.0.0.1:62001'
desired_caps['appPackage'] = 'com.orangestudio.calculator'
desired_caps['noReset'] = True
desired_caps['appActivity'] = 'com.orangestudio.calculator.ui.activity.MainActivity'

driver=webdriver.Remote('http://localhost:4723/wd/hub',desired_caps)

el2 = driver.find_element_by_id("com.orangestudio.calculator:id/one")
el2.click()
el3 = driver.find_element_by_id("com.orangestudio.calculator:id/plus")
el3.click()
el4 = driver.find_element_by_id("com.orangestudio.calculator:id/two")
el4.click()
el5 = driver.find_element_by_id("com.orangestudio.calculator:id/equal")
el5.click()
el6 = driver.find_element_by_id("com.orangestudio.calculator:id/tabBMI")
el6.click()
el7 = driver.find_element_by_id("com.orangestudio.calculator:id/heightInput")
el7.send_keys("172")
el8 = driver.find_element_by_id("com.orangestudio.calculator:id/weightInput")
el8.send_keys("65")
el9 = driver.find_element_by_id("com.orangestudio.calculator:id/start_calculate")
el9.click()
time.sleep(2)
TouchAction(driver).press(x=484, y=1048).move_to(x=484, y=670).release().perform()
driver.save_screenshot('stanrdard.png')
time.sleep(3)
driver.quit()