import os
import json
import time
from datetime import datetime
from datetime import date
import pandas as pd

DATA_FILE = u"notebook.json"
OUT_DATA_FILE = u"cleaned_notebook.json"
OUTPUT_DIR = u""
FILENAME = date.today().strftime('%Y-%m-%d')

def load_file():
    """
    load and pre-process notebook.json file
    """
    try:
        with open('notebook.json') as f:
            words = json.load(f)
        
        # last_updated = time.ctime(words['timestamp']/1000)
        words = words['words']

        # select cols and covert date, trans variables
        words_DF = pd.DataFrame(words)[['date', 'text', 'trans', 'context']]
        words_DF['date'] = words_DF.apply(lambda row: datetime.fromtimestamp(row['date']/1000).strftime('%Y-%m-%d %H:%M:%S')[:10], axis = 1)
        words_DF['trans'] = words_DF.apply(lambda row: row['trans'].split("\n", 1)[0], axis = 1)
        # count new words by date
        daily_count = words_DF.groupby(['date']).size().to_frame(name = 'daily_count')
        return words_DF.join(daily_count, on = 'date')
    except (IOError, ValueError):
        return{}

def save_cleaned_file(df):
    """
    save cleaned json file to local folder
    """
    df_json = df.to_json(orient = 'records')
    with open(OUT_DATA_FILE, 'w') as f:
        json.dump(df_json, f)

def export_to_md(df, output_name = FILENAME):
    '''
    export words to a formated md file
    '''
    filename = os.path.join(OUTPUT_DIR, u"%s.md" % output_name)
    date = ''
    with open(filename, 'w') as f:
        for index, row in df.iterrows():
            if row['date'] != date:
                date = row['date']
                daily_count = row['daily_count']
                f.write("## "+ date + " (" + str(daily_count) + ")" + "\n")
                f.write("- **" + row['text'] + ": **" + "\n" + row['trans']+ '\n')
                if row['context']:
                    f.write("   >" + row['context'] + '\n')
            else:
                f.write("- **" + row['text'] + ": **" + "\n" + row['trans']+ '\n')
                if row['context']:
                    f.write("   >" + row['context'] + '\n')

def main():
    # load & pre-process file
    df = load_file()
    # export words file to .md document
    export_to_md(df)
    # save a copy of the cleaned file to a new .json document
    save_cleaned_file(df)
    print('Done without error.')

if __name__ == '__main__':
    main()
