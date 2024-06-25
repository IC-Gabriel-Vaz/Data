import sqlite3
import yfinance as yf

from get_tickers import get_tickers as ct

def create_yfinance_db(benchmarks):

    conn = sqlite3.connect('PathToYourDIR/finance2.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Benchmarks (
        Name TEXT PRIMARY KEY
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Tickers (
        Benchmark TEXT,
        Ticker TEXT,
        FOREIGN KEY (Benchmark) REFERENCES Benchmarks (Name)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Prices (
        Benchmark TEXT,
        Ticker TEXT,
        Date TEXT,
        Open REAL,
        High REAL,
        Low REAL,
        Close REAL,
        Adj_Close REAL,
        Volume INTEGER,
        FOREIGN KEY (Ticker) REFERENCES Tickers (Ticker)
    )
    ''')

    conn.commit()

    for benchmark in benchmarks:
        cursor.execute('INSERT OR IGNORE INTO Benchmarks (Name) VALUES (?)', (benchmark,))

    for benchmark, tickers in benchmarks.items():
        for ticker in tickers:
            cursor.execute('INSERT OR IGNORE INTO Tickers (Benchmark, Ticker) VALUES (?, ?)', (benchmark, ticker))

    for benchmark, tickers in benchmarks.items():
        for ticker in tickers:
            print(f"Obtendo dados para {ticker}")
            hist = yf.download(ticker)
            for date, row in hist.iterrows():
                cursor.execute('''
                    INSERT INTO Prices (Benchmark, Ticker, Date, Open, High, Low, Close, Adj_Close, Volume)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (benchmark, ticker, date.strftime('%Y-%m-%d'), row['Open'], row['High'], row['Low'], row['Close'], row['Adj Close'], row['Volume']))

    conn.commit()
    conn.close()

    return None

if __name__ == '__main__':

    data = ct()

    create_yfinance_db(data)