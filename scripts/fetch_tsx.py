"""CSC370 prototype: fetch 10 TSX stocks and selected annual financial metrics.
Data source: Yahoo Finance via unofficial yfinance library.
AI-assisted draft: review and validate before submission.
"""
from pathlib import Path
import time
import pandas as pd
import yfinance as yf

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Diverse pilot sample, NOT a verified market-cap top-10 ranking.
TICKERS = ['RY.TO', 'TD.TO', 'BNS.TO', 'SHOP.TO', 'ENB.TO',
           'CNR.TO', 'CP.TO', 'SU.TO', 'BCE.TO', 'TRI.TO']

METRICS = {
    'revenue': ('Total Revenue',),
    'net_income': ('Net Income',),
    'basic_eps': ('Basic EPS',),
    'total_assets': ('Total Assets',),
    'total_liabilities': ('Total Liabilities Net Minority Interest', 'Total Liabilities'),
    'stockholders_equity': ('Stockholders Equity', 'Total Equity Gross Minority Interest'),
    'operating_cash_flow': ('Operating Cash Flow', 'Cash Flow From Continuing Operating Activities'),
}

def get_metric(frame, names, period):
    for name in names:
        if name in frame.index and period in frame.columns:
            value = frame.at[name, period]
            if pd.notna(value):
                return float(value)
    return None

companies, prices, annual, issues = [], [], [], []
for ticker in TICKERS:
    print(f'Fetching {ticker}...', flush=True)
    try:
        stock = yf.Ticker(ticker)
        info = stock.info or {}
        companies.append({
            'ticker': ticker,
            'company_name': info.get('longName') or info.get('shortName') or ticker,
            'sector': info.get('sector'),
            'industry': info.get('industry'),
            'market_cap_snapshot': info.get('marketCap'),
            'snapshot_date': pd.Timestamp.now(tz='UTC').date().isoformat(),
        })
        history = stock.history(period='1mo', interval='1d', auto_adjust=False)
        if history.empty:
            issues.append({'ticker': ticker, 'section': 'daily_price', 'detail': 'No rows returned'})
        else:
            for dt, r in history.iterrows():
                if pd.isna(r.get('Close')) or pd.isna(r.get('Volume')):
                    continue
                prices.append({
                    'ticker': ticker, 'trade_date': dt.date().isoformat(),
                    'open_price': r.get('Open'), 'high_price': r.get('High'),
                    'low_price': r.get('Low'), 'close_price': r.get('Close'),
                    'volume': int(r['Volume']),
                })
        statements = {
            'income': stock.income_stmt,
            'balance': stock.balance_sheet,
            'cashflow': stock.cashflow,
        }
        all_periods = sorted(set().union(*(set(df.columns) for df in statements.values() if not df.empty)))
        if not all_periods:
            issues.append({'ticker': ticker, 'section': 'financials', 'detail': 'No annual statements returned'})
        for period in all_periods:
            row = {'ticker': ticker, 'fiscal_period_end': pd.Timestamp(period).date().isoformat()}
            for field, names in METRICS.items():
                section = ('income' if field in ('revenue', 'net_income', 'basic_eps') else
                           'balance' if field in ('total_assets', 'total_liabilities', 'stockholders_equity') else 'cashflow')
                row[field] = get_metric(statements[section], names, period)
                if row[field] is None:
                    issues.append({'ticker': ticker, 'section': field, 'detail': row['fiscal_period_end'] + ': missing'})
            annual.append(row)
    except Exception as exc:
        issues.append({'ticker': ticker, 'section': 'fetch', 'detail': str(exc)[:300]})
        print(f'  ERROR: {exc}')
    time.sleep(1)

outputs = {
    'companies.csv': (companies, ['ticker','company_name','sector','industry','market_cap_snapshot','snapshot_date']),
    'daily_prices.csv': (prices, ['ticker','trade_date','open_price','high_price','low_price','close_price','volume']),
    'annual_financials.csv': (annual, ['ticker','fiscal_period_end',*METRICS.keys()]),
    'data_issues.csv': (issues, ['ticker','section','detail']),
}
for filename, (rows, cols) in outputs.items():
    pd.DataFrame(rows, columns=cols).to_csv(DATA_DIR / filename, index=False)
    print(f'{filename}: {len(rows)} rows')
print('Review data_issues.csv and source data before designing final schema.')
