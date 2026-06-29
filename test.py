from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By

import io
import requests
from bs4 import BeautifulSoup
from PIL import Image

import time
import os

def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)

        file_path = download_path + file_name

        with open(file_path, "wb") as file:
            image.save(file, "JPEG")
            
        print("SUCCESS")
    
    except Exception as e:
        print(f'FAILED - {e}')


def get_images_from_google(wd, url, delay, max_images):
    # Retrieve homepage
    wd.get(url)

    # Store all thumbnails found in list
    thumbnails = wd.find_elements(By.CLASS_NAME, "thumbnail")

    # for i in range(max_images):

    #     if i >= len(thumbnails):
    #         break

    #     thumbnails[i].click()
    #     time.sleep(delay)

    #     try:
    #         img = wd.find_element(By.TAG_NAME, "img")
    #         image_url = img.get_attribute("src")
    #         image_name = img.get_attribute("alt")

    #         print(image_name)

    #         download_image(
    #             "images/",
    #             image_url,
    #             f"image_{i}.jpg"
    #         )

    #     except Exception as e:
    #         print(f"ERROR {e}")

    #     wd.back()

    for i, img in enumerate(thumbnails):
        
        if (i == max_images):
            break
        
        image_url = img.get_attribute("src")

        download_image(
            "images/",
            image_url,
            f"book_{i}.jpg"
        )
        time.sleep(delay)

def main():
    driver_path = os.getenv("DRIVER_FILE_PATH")
    service = Service(executable_path=driver_path)

    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    wd = webdriver.Chrome(options=chrome_options, service=service)

    image_url = "https://books.toscrape.com/"    

    get_images_from_google(wd, image_url, 0.1, 10)
    
    wd.quit()


if __name__ == "__main__":
    main()