import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

# Start wirtualnego wyświetlacza
display = Display(visible=0, size=(800, 800))
display.start()

def web_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--verbose")
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')  # Działa w tle (bez GUI)
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1920,1200")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.binary_location = "/usr/bin/chromium-browser"

    driver = webdriver.Chrome(options=options)
    return driver

driver = web_driver()

# Otwórz stronę
driver.get("https://rwgservices.rwg.nl/Modality/VesselArrivalTimes")

time.sleep(10)
# show - do wybrania 100 wierszy
#select_element = driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div[1]/div[1]/label/select")
select_element = driver.find_element(By.CSS_SELECTOR,'#list_length > label > select')
select = Select(select_element)

sto = driver.find_element(By.CSS_SELECTOR, "#list_length > label > select > option:nth-child(4)")
select.select_by_value('100')

# cookie zasłaniało filtr,trzeba kliknąć żeby znikło
cookie_button= driver.find_element(By.XPATH,"/html/body/div[1]/div/a")
cookie_button.click()

# filtr w kolumnie Modality
filter_button = driver.find_element (By.XPATH, "/html/body/div[3]/div[2]/div/table/thead/tr/th[9]/i")
filter_button.click()

#znajdujemy rail i barge
checkbox_1 = driver.find_element(By.XPATH, "//label[contains(text(), 'BARGE')]")
checkbox_2 = driver.find_element(By.XPATH, "//label[contains(text(), 'RAIL')]")


# Kliknięcie checkboxów
checkbox_1.click()
checkbox_2.click()

# znajdz tabelę
table = driver.find_element(By.ID, "list")

# pobierz nagłówki
headers = [th.text for th in table.find_elements(By.TAG_NAME, "th")]

# Pobierz dane z wierszy tabeli
data = []
rows = table.find_elements(By.TAG_NAME, "tr")[1:]  
for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    data.append([col.text for col in cols])

# Konwersja do DataFrame
df = pd.DataFrame(data, columns=headers)

driver.quit()

# Zapis do pliku Excel
file_path = "Rotterdam_schedule.csv"
df.to_csv(file_path, index=False, encoding = 'utf-8')

# Zakończenie działania wirtualnego wyświetlacza
display.stop(

