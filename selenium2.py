import os
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

# Directory
folder_name = 'images'
if not os.path.isdir(folder_name):
    os.makedirs(folder_name)

def download_image(url, folder_name, num):
    # Write image to file
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(folder_name, f"{num}.jpg"), 'wb') as file:
            file.write(response.content)

# Initialize Chrome WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # Optional: run in headless mode
driver = webdriver.Chrome(options=chrome_options)

search_URL = "https://www.google.com/search?q=quotes&source=lnms&tbm=isch"
driver.get(search_URL)

# Scroll to the bottom of the page to load more images
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Adjust sleep time as necessary
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Extract image URLs using BeautifulSoup
page_html = driver.page_source
soup = BeautifulSoup(page_html, 'html.parser')
image_elements = soup.find_all('img', class_='rg_i')

for idx, img in enumerate(image_elements, 1):
    if 'src' in img.attrs:
        image_url = img['src']
        if image_url.startswith('http'):
            try:
                download_image(image_url, folder_name, idx)
                print(f"Downloaded image {idx}/{len(image_elements)}: {image_url}")
            except Exception as e:
                print(f"Error downloading image {idx}: {str(e)}")
    else:
        print(f"Skipping image {idx}: No 'src' attribute found")

driver.quit()
