from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from io import BytesIO 
import requests
from bs4 import BeautifulSoup
from PIL import Image

import time
import os

def download_image(download_path, url, file_name):
    try:
        # Create folder if it does not exist
        if not os.path.exists(download_path):
            os.makedirs(download_path)
            
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        
        #Pass headers to the request
        response = requests.get(url, headers=headers, stream=True, timeout=20)
        
        # Check if the server returned an error code
        response.raise_for_status() 
                
        full_path = os.path.join(download_path, file_name)
        with open(full_path, "wb") as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)
        print(f"SAVED - {full_path}")
        
    except Exception as e:
        print(f"FAILED - {e}")



def get_images_from_books_scape(wd, url, delay, max_images):
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


def wiki(wd, url, delay, max_images):
    # Retrieve homepage
    wd.get(url)

    # Store all thumbnails & corresponding links found in list
    thumbnails = wd.find_elements(By.CLASS_NAME, "mw-file-description")
    page_urls = [link.get_attribute("href") for link in thumbnails[:max_images]]

    print(page_urls)

    # Parse through all links & download images
    for i, page_url in enumerate(page_urls):
        try:
            wd.get(page_url)

            full_res_link = WebDriverWait(wd, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "internal"))
            )
            print(full_res_link)

            image_url = full_res_link.get_attribute("href")

            if image_url.lower().endswith(".svg"):
                print("Skipping SVG")
                continue

            download_image(
                "images/",
                image_url,
                f"image_{i}.jpg"
            )
            time.sleep(delay)


        except Exception as e:
            print(f"ERROR {e}")

        wd.back()


