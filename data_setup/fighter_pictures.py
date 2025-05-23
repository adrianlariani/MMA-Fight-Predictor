import os

import psycopg2
import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')


def get_images():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
    URL = "https://www.ufc.com/athlete/"
    conn = psycopg2.connect(database=os.getenv("DATABASE_NAME"),
                            host=os.getenv("DATABASE_HOST"),
                            user=os.getenv("DATABASE_USERNAME"),
                            password=os.getenv("DATABASE_PASSWORD")
                            )
    DEFAULT_IMAGE = "https://answers-embed-client.ufc.com.pagescdn.com/static/assets/images/UFC-Male-Fallback-Image.jpg"

    INSERT_QUERY = '''UPDATE fighter_statistics SET image_link = %s WHERE id = %s'''
    with conn.cursor() as curs:
        try:
            curs.execute("SELECT * FROM fighter_statistics")
            rows = curs.fetchall()
            conn.commit()
            curs.execute("SELECT * FROM fighter_statistics")

            for entry in tqdm.tqdm(rows):
                if entry[0] < 2556:
                    continue
                image_link = get_image(entry[1])
                curs.execute(INSERT_QUERY, (image_link, entry[0]))
                conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

def get_image(name):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    DEFAULT_IMAGE = "https://answers-embed-client.ufc.com.pagescdn.com/static/assets/images/UFC-Male-Fallback-Image.jpg"
    URL = "https://www.ufc.com/athlete/"
    name = name.split(" ")[0] + " " + name.split(" ")[len(name.split(" "))-1]
    browser.get(URL + (name.replace(' ', "-")))
    html = browser.page_source
    soup = BeautifulSoup(html, features="html.parser")
    images = soup.find_all("img", class_="hero-profile__image")
    if len(images) >= 1:
        return str(images[0]['src'])
    else:
        return DEFAULT_IMAGE




if __name__ == "__main__":
    get_images()