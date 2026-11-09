
-- CSC370 TSX Financial Database
-- Kick-off: Initial relational schema
-- AI assistance: ChatGPT helped draft the SQL
-- based on the project owner's design decisions.

CREATE DATABASE IF NOT EXISTS tsx_financial;
USE tsx_financial;

-- 1. Company
CREATE TABLE Company (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    ticker VARCHAR(20) NOT NULL UNIQUE,
    company_name VARCHAR(200) NOT NULL,
    sector VARCHAR(100),
    industry VARCHAR(150)
);

-- 2. Daily Price
CREATE TABLE DailyPrice (
    company_id INT NOT NULL,
    trade_date DATE NOT NULL,
    close_price DECIMAL(18,4),
    volume BIGINT UNSIGNED,

    PRIMARY KEY (company_id, trade_date),

    FOREIGN KEY (company_id)
        REFERENCES Company(company_id),

    CHECK (close_price IS NULL OR close_price >= 0)
);

-- 3. Income Statement
CREATE TABLE IncomeStatement (
    company_id INT NOT NULL,
    fiscal_period_end DATE NOT NULL,
    revenue DECIMAL(24,2),
    gross_profit DECIMAL(24,2),
    operating_income DECIMAL(24,2),
    net_income DECIMAL(24,2),

    PRIMARY KEY (company_id, fiscal_period_end),

    FOREIGN KEY (company_id)
        REFERENCES Company(company_id)
);

-- 4. Balance Sheet
CREATE TABLE BalanceSheet (
    company_id INT NOT NULL,
    fiscal_period_end DATE NOT NULL,
    total_assets DECIMAL(24,2),
    total_liabilities DECIMAL(24,2),
    stockholders_equity DECIMAL(24,2),
    cash_and_equivalents DECIMAL(24,2),
    total_debt DECIMAL(24,2),

    PRIMARY KEY (company_id, fiscal_period_end),

    FOREIGN KEY (company_id)
        REFERENCES Company(company_id)
);

-- 5. Cash Flow Statement
CREATE TABLE CashFlowStatement (
    company_id INT NOT NULL,
    fiscal_period_end DATE NOT NULL,
    operating_cash_flow DECIMAL(24,2),
    investing_cash_flow DECIMAL(24,2),
    financing_cash_flow DECIMAL(24,2),
    capital_expenditure DECIMAL(24,2),

    PRIMARY KEY (company_id, fiscal_period_end),

    FOREIGN KEY (company_id)
        REFERENCES Company(company_id)
);
