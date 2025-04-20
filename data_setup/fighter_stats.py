import os

import requests
from bs4 import BeautifulSoup
import string
import tqdm
from dotenv import load_dotenv
from data_setup.fighter_pictures import get_image

load_dotenv()


import psycopg2


conn = psycopg2.connect(database=os.environ["DATABASE_NAME"],
                          host=os.environ["DATABASE_HOST"],
                          user=os.environ["DATABASE_USERNAME"],
                          password=os.environ["DATABASE_PASSWORD"]
                          )


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}
URL = "http://ufcstats.com/statistics/fighters?char="
URL_END = "&page=all"


def main():
    create_table()
    for letter in string.ascii_lowercase:
        print(letter)
        page = requests.get(URL + letter + URL_END, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        fighter_table = soup.find_all("tr", class_="b-statistics__table-row")
        fighter_list = list(fighter_table)

        for fighter in tqdm.tqdm(fighter_list):

            links = fighter.find_all("a", class_="b-link")
            if links:
                link = links[0].get('href')
                fighter_info(link)



def create_table():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS fighter_statistics (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        height DECIMAL,  
        weight DECIMAL,  
        reach DECIMAL, 
        stance VARCHAR(11) CHECK (stance IN ('Orthodox', 'Southpaw', 'Switch', 'Open Stance')),
        SLpM DECIMAL,
        Str_Acc DECIMAL,
        SApM DECIMAL,
        Str_Def DECIMAL,
        TD_Avg DECIMAL,
        TD_Acc DECIMAL,
        TD_Def DECIMAL,
        Sub_Avg DECIMAL,
        image_link VARCHAR(255)
    );
    """

    try:
        with conn.cursor() as cur:
            cur.execute(create_table_query)
            conn.commit()
            print("Table created successfully with numeric columns and stance constraints")
    except:
        print("went wrong")
        pass


def validate_and_insert(name, height_str, weight_str, reach_str, stance, slpm, str_acc, sapm, str_def, td_avg, td_acc,
                        td_def, sub_avg):
    try:
        height = float(height_str)
        weight = float(weight_str)
        reach = float(reach_str)
    except:
        print("Height, weight, and reach must be numeric values.")
        print(height_str)
        print(weight_str)
        print(reach_str)
        return

    valid_stances = ['Orthodox', 'Southpaw', 'Switch', 'Open Stance']
    if stance not in valid_stances:
        print(f"Invalid stance value: {stance}. Must be one of {valid_stances}.")
        return
    image = get_image(name)
    insert_data = (name, height, weight, reach, stance, slpm, str_acc, sapm, str_def, td_avg, td_acc, td_def, sub_avg, image)
    update_data = (height, weight, reach, stance, slpm, str_acc, sapm, str_def, td_avg, td_acc, td_def, sub_avg, image, name)
    print(insert_data)

    #try:
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM fighter_statistics WHERE name = %s", (name,))
        result = cur.fetchone()

        if result:
            update_query = """
            UPDATE fighter_statistics SET 
                height=%s, weight=%s, reach=%s, stance=%s, SLpM=%s, Str_Acc=%s, 
                SApM=%s, Str_Def=%s, TD_Avg=%s, TD_Acc=%s, TD_Def=%s, Sub_Avg=%s, image_link=%s
            WHERE name=%s
            """
            cur.execute(update_query, update_data)
            print(f"Updated existing entry for {name}")
        else:
            insert_query = """
            INSERT INTO fighter_statistics (
                name, height, weight, reach, stance, SLpM, Str_Acc, SApM, Str_Def, TD_Avg, TD_Acc, TD_Def, Sub_Avg, image_link
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """
            cur.execute(insert_query, insert_data)
            print(f"Inserted new entry for {name}")

        conn.commit()

    #except Exception as e:
    #    print(f"An error occurred: {e}")




def fighter_info(link: str):
    page = requests.get(link, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    name = soup.find_all("span", class_="b-content__title-highlight")[0].getText(strip=True)
    height = None
    weight = None
    reach = None
    stance = None
    slpm = None
    str_acc = None
    sapm = None
    str_def = None
    td_avg = None
    td_acc = None
    td_def = None
    sub_avg = None

    lists = soup.find_all("li", class_="b-list__box-list-item b-list__box-list-item_type_block")

    for list_item in lists:
        stat = list_item.get_text(strip=True)
        if stat:
            if 'Height' in stat:
                if '--' in stat:
                    height = 0
                else:
                    height = convert_height_to_inches(stat.split(':')[1].strip())
            elif 'Weight' in stat:
                weight = stat.split(':')[1].strip().split()[0]
                if weight == '--':
                    weight = 0
            elif 'Reach' in stat:
                reach = stat.split(':')[1].strip().split()[0]
                reach = reach[0:len(reach) - 1]
                if '-' in reach:
                    reach = 0
            elif 'STANCE' in stat:
                stance = stat.split(':')[1].strip()
                if not stance or stance == '--':
                    stance = 'Orthodox'
            elif 'SLpM' in stat:
                slpm = stat.split(':')[1].strip()
                slpm = float(slpm) if slpm != '--' else 0
            elif 'Str. Acc' in stat:
                str_acc = stat.split(':')[1].strip().replace('%', '')
                str_acc = float(str_acc) if str_acc != '--' else 0
            elif 'SApM' in stat:
                sapm = stat.split(':')[1].strip()
                sapm = float(sapm) if sapm != '--' else 0
            elif 'Str. Def' in stat:
                str_def = stat.split(':')[1].strip().replace('%', '')
                str_def = float(str_def) if str_def != '--' else 0
            elif 'TD Avg' in stat:
                td_avg = stat.split(':')[1].strip()
                td_avg = float(td_avg) if td_avg != '--' else 0
            elif 'TD Acc' in stat:
                td_acc = stat.split(':')[1].strip().replace('%', '')
                td_acc = float(td_acc) if td_acc != '--' else 0
            elif 'TD Def' in stat:
                td_def = stat.split(':')[1].strip().replace('%', '')
                td_def = float(td_def) if td_def != '--' else 0
            elif 'Sub. Avg' in stat:
                sub_avg = stat.split(':')[1].strip()
                sub_avg = float(sub_avg) if sub_avg != '--' else 0
    validate_and_insert(name, height, weight, reach, stance, slpm, str_acc, sapm, str_def, td_avg, td_acc, td_def,
                        sub_avg)


def convert_height_to_inches(height_str):
    height_str = height_str.strip()

    parts = height_str.split("'")

    if len(parts) != 2:
        raise ValueError("Invalid height format. Expected format: X' Y\"")

    feet = int(parts[0].strip())
    inches = int(parts[1].replace('"', '').strip())

    total_inches = feet * 12 + inches

    return total_inches


if __name__ == "__main__":
    main()
