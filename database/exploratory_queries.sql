-- Total companies
SELECT COUNT(*) FROM companies;

-- Total records in each table
SELECT COUNT(*) FROM profitandloss;
SELECT COUNT(*) FROM balancesheet;
SELECT COUNT(*) FROM cashflow;

-- Companies by sector
SELECT sector, COUNT(*)
FROM sectors
GROUP BY sector;

-- Top 10 companies by market cap
SELECT company_id, market_cap
FROM market_cap
ORDER BY market_cap DESC
LIMIT 10;

-- Companies having more than 10 years of data
SELECT company_id, COUNT(*)
FROM profitandloss
GROUP BY company_id
HAVING COUNT(*) > 10;

-- Latest stock prices
SELECT company_id, date, close
FROM stock_prices
ORDER BY date DESC;

-- sqlite3 database_name.db < path/to/file.sql
