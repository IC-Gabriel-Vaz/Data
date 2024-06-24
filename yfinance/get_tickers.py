import pandas as pd
import yfinance as yf

def get_tickers():

    data = {}

    ############################################
    
    sep500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    sp500_tables = pd.read_html(sep500_url)

    sp500 = sp500_tables[0]['Symbol'].to_list()

    data['SP500'] = sp500

    ############################################

    dax_url = "https://en.wikipedia.org/wiki/DAX"

    dax_tables = pd.read_html(dax_url)

    dax = dax_tables[4]['Ticker'].to_list()

    data['DAX'] = dax

    ############################################

    ibov_url = 'https://en.wikipedia.org/wiki/List_of_companies_listed_on_B3' 

    ibov_tables = pd.read_html(ibov_url)

    ibov = ibov_tables[0]

    ibov.columns = ibov.loc[0]

    ibov = ibov[1:]

    ibov = ibov["Código"].to_list()

    ibov_final = []

    for ticker in ibov:
        ticker = ticker + '.SA'
        ibov_final.append(ticker)
    
    ibov_final = ibov_final[:len(ibov_final)-2]

    data['IBOV'] = ibov_final

    ############################################

    return data

if __name__ == '__main__':

    data = get_tickers()

