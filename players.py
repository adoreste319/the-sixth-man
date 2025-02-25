import pandas as pd
from requests import get
from bs4 import BeautifulSoup
from datetime import date

try:
    from utils import get_player_suffix
except:
    from basketball_reference_scraper.utils import get_player_suffix

"""Alexis changes: added an incrementing player ID in case of repeated name,
   added variable suffix1, specifically looks for player participation last year.
   Retrieves either career stats by year or specific year stats. Added overwriting
   functionality consistent with changes in utils.py, only executes upon thrown
   exception."""
def get_stats(name, stat_type='PER_GAME', season=0, playoffs=False, career=False):
    try:
        suffix1 = get_player_suffix(name, False).replace('/', '%2F')
        for i in range(1, 6):
            suffix = suffix1[:-6] + str(i) + ".html"
            selector = stat_type.lower()
            if playoffs:
                selector = 'playoffs_'+selector
            r = get(f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url={suffix}&div=div_{selector}')
            if r.status_code==200:
                soup = BeautifulSoup(r.content, 'html.parser')
                table = soup.find('table')
                df = pd.read_html(str(table))[0]
                df.rename(columns={'Season': 'SEASON', 'Age': 'AGE',
                          'Tm': 'TEAM', 'Lg': 'LEAGUE', 'Pos': 'POS'}, inplace=True)
                career_index = df[df['SEASON']=='Career'].index[0]
                if career:
                    df = df.iloc[career_index+2:, :]
                else:
                    df = df.iloc[:career_index, :]

                df = df.reset_index().dropna(axis=1).drop('index', axis=1)
                if season and season >= 1949 and season <= int(date.today().year):
                    season1 = str(season - 1) + "-" + str(season)[2:]
                    if len(df.loc[df['SEASON']==season1].head(1)) != 0:
                        return df.loc[df['SEASON']==season1].head(1).reset_index(drop=True)

                else:
                    return df

    except:
        suffix1 = get_player_suffix(name, True).replace('/', '%2F')
        for i in range(1, 6):
            suffix = suffix1[:-6] + str(i) + ".html"
            selector = stat_type.lower()
            if playoffs:
                selector = 'playoffs_'+selector
            r = get(f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url={suffix}&div=div_{selector}')
            if r.status_code==200:
                soup = BeautifulSoup(r.content, 'html.parser')
                table = soup.find('table')
                df = pd.read_html(str(table))[0]
                df.rename(columns={'Season': 'SEASON', 'Age': 'AGE',
                          'Tm': 'TEAM', 'Lg': 'LEAGUE', 'Pos': 'POS'}, inplace=True)
                career_index = df[df['SEASON']=='Career'].index[0]
                if career:
                    df = df.iloc[career_index+2:, :]
                else:
                    df = df.iloc[:career_index, :]

                df = df.reset_index().dropna(axis=1).drop('index', axis=1)
                if season and season >= 1949 and season <= int(date.today().year):
                    season1 = str(season - 1) + "-" + str(season)[2:]
                    if len(df.loc[df['SEASON']==season1].head(1)) != 0:
                        return df.loc[df['SEASON']==season1].head(1).reset_index(drop=True)

                else:
                    return df
            
    return df

def get_game_logs(name, start_date, end_date, playoffs=False):
    suffix = get_player_suffix(name).replace('/', '%2F').replace('.html', '')
    start_date_str = start_date
    end_date_str = end_date
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    years = list(range(start_date.year, end_date.year+2))
    if playoffs:
        selector = 'div_pgl_basic_playoffs'
    else:
        selector = 'div_pgl_basic'
    final_df = None
    for year in years:
        r = get(f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url={suffix}%2Fgamelog%2F{year}&div={selector}')
        if r.status_code==200:
            soup = BeautifulSoup(r.content, 'html.parser')
            table = soup.find('table')
            if table:
                df = pd.read_html(str(table))[0]
                df.rename(columns = {'Date': 'DATE', 'Age': 'AGE', 'Tm': 'TEAM', 'Unnamed: 5': 'HOME/AWAY', 'Opp': 'OPPONENT',
                        'Unnamed: 7': 'RESULT', 'GmSc': 'GAME_SCORE'}, inplace=True)
                df['HOME/AWAY'] = df['HOME/AWAY'].apply(lambda x: 'AWAY' if x=='@' else 'HOME')
                df = df[df['Rk']!='Rk']
                df = df.drop(['Rk', 'G'], axis=1)
                df = df.loc[(df['DATE'] >= start_date_str) & (df['DATE'] <= end_date_str)]
                active_df = pd.DataFrame(columns = list(df.columns))
                for index, row in df.iterrows():
                    if len(row['GS'])>1:
                        continue
                    active_df = active_df.append(row)
                if final_df is None:
                    final_df = pd.DataFrame(columns=list(active_df.columns))
                final_df = final_df.append(active_df)
    return final_df
