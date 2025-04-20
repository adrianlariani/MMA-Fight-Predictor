import os

import pandas as pd
import psycopg2
from psycopg2 import sql
from tqdm import tqdm

from dotenv import load_dotenv

csv_file_path = 'large_dataset.csv'
load_dotenv(dotenv_path='.env')

conn = psycopg2.connect(database=os.getenv("DATABASE_NAME"),
                        host=os.getenv("DATABASE_HOST"),
                        user=os.getenv("DATABASE_USERNAME"),
                        password=os.getenv("DATABASE_PASSWORD")
                        )
conn.autocommit = True
cur = conn.cursor()

stance_to_id = {
    "Orthodox": 0,
    "Southpaw": 1,
    "Switch": 2,
    "Open Stance": 3
}

winner = {
    "Red": 0,
    "Blue": 1
}

valid_stances = ['Orthodox', 'Southpaw', 'Switch', 'Open Stance']


def main():
    create_table()
    df = pd.read_csv(csv_file_path)
    new_df = setup_table_values(df)
    insert_data_to_postgresql(new_df, 'fights')
    cur.close()
    conn.close()


def create_table():
    create_table_query = """
        CREATE TABLE IF NOT EXISTS fights (
            id SERIAL PRIMARY KEY,
            winner INT,
            weight_diff DECIMAL,
            height_diff DECIMAL,
            reach_diff DECIMAL,
            r_stance DECIMAL,
            b_stance DECIMAL,
            SLpM_total_diff DECIMAL,
            sig_str_acc_total_diff DECIMAL,
            SApM_total_diff DECIMAL,
            str_def_total_diff DECIMAL,
            td_avg_diff DECIMAL,
            td_acc_total_diff DECIMAL,
            td_def_total_diff DECIMAL,
            sub_avg_diff DECIMAL
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


def setup_table_values(df):
    df['r_stance'] = df['r_stance'].apply(lambda x: x if x in valid_stances else 'Orthodox')
    df['r_stance'] = df['r_stance'].map(stance_to_id)
    df['b_stance'] = df['b_stance'].apply(lambda x: x if x in valid_stances else 'Orthodox')
    df['b_stance'] = df['b_stance'].map(stance_to_id)

    winner = {
        "Red": 1,
        "Blue": 0
    }
    df['winner'] = df['winner'].map(winner)

    columns_to_keep = ['winner',
                       'weight_diff',
                       "height_diff",
                       "reach_diff",
                       "r_stance",
                       "b_stance",
                       "SLpM_total_diff",
                       "sig_str_acc_total_diff",
                       "SApM_total_diff",
                       "str_def_total_diff",
                       "td_avg_diff",
                       "td_acc_total_diff",
                       "td_def_total_diff",
                       "sub_avg_diff"]

    df1 = df[columns_to_keep].copy()
    df2 = df[columns_to_keep].copy()

    numerical_columns = ['SLpM_total_diff', 'sig_str_acc_total_diff', 'SApM_total_diff',
                         'str_def_total_diff', 'td_avg_diff', 'td_acc_total_diff',
                         'td_def_total_diff', 'sub_avg_diff', 'weight_diff',
                         'height_diff', 'reach_diff']
    df2[numerical_columns] = -df2[numerical_columns]

    df2['r_stance'] = df1['b_stance']
    df2['b_stance'] = df1['r_stance']
    df2['winner'] = (1 - df1['winner'])

    final_df = pd.concat([df1, df2], ignore_index=True)
    filtered_df = final_df.fillna(0)
    return filtered_df


def insert_data_to_postgresql(df, table_name):
    columns = ', '.join(df.columns)
    values_template = ', '.join(['%s'] * len(df.columns))

    insert_query = sql.SQL(
        f"INSERT INTO {table_name} ({columns}) VALUES ({values_template})"
    )

    # Insert each row
    for i, row in tqdm(df.iterrows(), total=len(df)):
        cur.execute(insert_query, row.tolist())


if __name__ == "__main__":
    main()
