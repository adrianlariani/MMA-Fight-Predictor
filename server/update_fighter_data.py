from bs4 import BeautifulSoup
from selenium import webdriver

from data_setup.fighter_stats import fighter_info


def event_update_fighters():
    recent_events_link = "https://www.ufc.com/events#events-list-past"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--remote-debugging-port=9222')
    browser = webdriver.Chrome(options=options)
    browser.get(recent_events_link)
    html = browser.page_source
    soup = BeautifulSoup(html, features="html.parser")
    most_recent_event_link = "https://www.ufc.com" + soup.find_all("a", class_="e-button--white")[14]['href']

    print(most_recent_event_link)

    browser.get(most_recent_event_link)
    html = browser.page_source
    soup = BeautifulSoup(html, features="html.parser")
    divs = soup.find_all("div", class_="c-listing-fight__corner-name")

    last_name = None
    first_name = None

    for fighter in divs:
        try:
            first_name, last_name = fighter.a.text.strip().replace('\n', ' ').split(" ", 1)
            link = "http://ufcstats.com/statistics/fighters/search?query=" + last_name.replace(" ", "+")

        except:
            first_name = fighter.a.text.strip().replace('\n', ' ')
            link = "http://ufcstats.com/statistics/fighters/search?query=" + first_name.replace(" ", "+")

        browser.get(link)
        html = browser.page_source
        soup = BeautifulSoup(html, features="html.parser")
        for row in soup.find_all("tr", class_="b-statistics__table-row"):
            texts = row.find_all("td", class_="b-statistics__table-col")

            if len(texts) > 1 and ((not last_name and  texts[0].text.strip() == first_name)
                                   or (texts[0].text.strip() == first_name and texts[1].text.strip() == last_name)
                                   or (texts[2].text.strip() == first_name and texts[1].text.strip() == last_name)
                                   or (texts[2].text.strip() == last_name and texts[0].text.strip() == first_name)):
                url = row.find("a")['href']
                fighter_info(url)
                break


    return

if __name__ == "__main__":
    event_update_fighters()
