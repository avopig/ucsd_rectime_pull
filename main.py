import time, requests, re, pandas as pd, numpy as np
from os.path import exists
from datetime import datetime
from bs4 import BeautifulSoup

def pull_date_hours(url="https://recreation.ucsd.edu/open-rec/"):

    response = requests.get(url)
    if response.status_code != 200: print("Failed to retrieve the website.")

    pattern = re.compile(r'^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday), .+', re.MULTILINE)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = [p.get_text() for p in soup.find_all('p')]
    paragraphs = [p for p in paragraphs if pattern.match(p)]

    date_hours = []
    for p in paragraphs:
        date_str = p.split('\n')[0]
        rimac_hours = [court_hour for court_hour in p.split('\n')[1:] if 'RIMAC' in court_hour]
        if len(rimac_hours) == 0: continue
        date_hours.append([date_str, 
            '-'.join([rimac_hours[0].split('-')[0], rimac_hours[0].split('-')[1]])])

    return date_hours

def make_dataframe(date_hours):
    '''Takes a list of lists of date and hours and returns a dataframe
        [['Monday, 10/16', '6:30am-2:30pm'], 
         ['Tuesday, 10/17', '6:30am-6:30pm'], 
         ['Wednesday, 10/18', '6:30am-2:30pm']]
    '''
    now = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    dates, hours = np.array(date_hours).T
    return pd.DataFrame({
        'Scheduled Date': dates,
        f'Scheduled open rec hrs as of {now}': hours
    })

def save_dataframe(df, filename='log.csv'): df.to_csv(filename, index=False)

def load_dataframe(filename='log.csv'): return pd.read_csv(filename)

def merge_dfs(df1, df2):

    try:
        if (df1['Scheduled Date'] == df1['Scheduled Date']).all() \
        and (df1[df1.keys()[-1]] == df2[df2.keys()[-1]]).all(): return df2
    except: pass

    df = pd.merge(df1, df2, on='Scheduled Date', how='outer')
    return df



if __name__ == '__main__':
    fname = 'log.csv'
    while True:

        if not exists(fname): 
            df1 = make_dataframe(pull_date_hours())
            save_dataframe(df1, fname)
        else:
            df1 = load_dataframe(fname)
        
        df2 = make_dataframe(pull_date_hours())
        save_dataframe(merge_dfs(df1, df2), fname)
        time.sleep(3600)    # 1 hour