from scraper_functions import *


def main():
    driver_path = os.getenv("DRIVER_FILE_PATH")
    service = Service(executable_path=driver_path)

    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    wd = webdriver.Chrome(options=chrome_options, service=service)

    # image_url = "https://books.toscrape.com/"    
    # get_images_from_books_scape(wd, image_url, 0.1, 10)
    
    image_url = "https://commons.wikimedia.org/wiki/Category:Eukaryota"
    wiki(wd, image_url, 0, 200)

    wd.quit()


if __name__ == "__main__":
    main()