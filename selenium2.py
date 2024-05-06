import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
import io
from PIL import Image
import time
from tqdm import tqdm

chromedriver_autoinstaller.install()

# Define search query
search_query = "Cat images"

# Create a directory to save images
folder_name = 'images'
if not os.path.isdir(folder_name):
    os.makedirs(folder_name)


def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image = Image.open(io.BytesIO(image_content))
        file_path = os.path.join(download_path, file_name)

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print(f"Success: {file_name}")
    except Exception as e:
        print(f'FAILED - {e}')


# Initialize Chrome WebDriver
driver = webdriver.Chrome()

search_URL = f"https://www.google.com/search?q={search_query}&source=lnms&tbm=isch"
driver.get(search_URL)

# Wait for the page to fully load
time.sleep(5)

# Scroll to the bottom of the page to load more images
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for dynamic content to load
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Extract image URLs using BeautifulSoup
page_html = driver.page_source
soup = BeautifulSoup(page_html, 'html.parser')
image_elements = soup.select('img')

print(f"Found {len(image_elements)} image elements.")

# Set maximum number of images to download
max_images = 10
images_downloaded = 0

# Create tqdm progress bar
progress_bar = tqdm(total=max_images)

for idx, img in enumerate(image_elements, 1):
    if images_downloaded >= max_images:
        break  # Stop downloading images if the maximum limit is reached

    if 'src' in img.attrs:
        image_url = img['src']
        if image_url.startswith('http'):
            try:
                download_image(folder_name, image_url, f"{idx}.jpg")
                print(f"Downloaded image {idx}/{len(image_elements)}: {image_url}")
                images_downloaded += 1
                progress_bar.update(1)  # Increment progress bar
            except Exception as e:
                print(f"Error downloading image {idx}: {str(e)}")
    else:
        print(f"Skipping image {idx}: No 'src' attribute found")

# Close progress bar
progress_bar.close()

driver.quit()
