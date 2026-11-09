# Relational Design Validation

## 1. Functional Dependencies and Candidate Keys

The initial design contains five relations: Company, DailyPrice, IncomeStatement, BalanceSheet, and CashFlowStatement.

The original Company relation is:

`Company(company_id, ticker, company_name, sector, industry)`

The identified functional dependencies are:

- `company_id → ticker, company_name, sector, industry`
- `ticker → company_id, company_name, sector, industry`
- `industry → sector`

Both `company_id` and `ticker` are candidate keys, assuming unique tickers in the current dataset.

For DailyPrice, the candidate key is `(company_id, trade_date)`.

For each financial statement relation, the candidate key is `(company_id, fiscal_period_end)`.

These composite keys determine the remaining attributes in their respective relations.

## 2. BCNF Decomposition

The original Company relation violates BCNF because `industry → sector` holds while `industry` is not a superkey.

To resolve this, Company is decomposed into:

**Company**

`Company(company_id, ticker, company_name, industry)`

**Industry**

`Industry(industry, sector)`

In the revised design:

- `company_id` is the primary key of Company.
- `ticker` remains unique.
- `industry` is the primary key of Industry.
- `Company.industry` is a foreign key referencing Industry.

The remaining four relations are unchanged, resulting in six relations.

This decomposition assumes that each industry belongs to exactly one sector within the classification system.

## 3. Lossless Join and Dependency Preservation

The decomposition is lossless because `industry → sector`. Joining Company and Industry on `industry` reconstructs the original Company information, assuming each company has a valid industry reference.

The original functional dependencies are also preserved.

For example:

`company_id → industry → sector`

`ticker → industry → sector`

Therefore, both `company_id → sector` and `ticker → sector` can still be derived from the decomposed relations.

## 4. 4NF and Multivalued Dependencies

The revised relations were examined for multivalued dependencies.

Under the current business rules, each company has one representative industry, and each industry belongs to one sector. Daily prices and financial statements are stored using their respective composite keys.

No independent multivalued dependencies requiring further decomposition were identified.

Therefore, the revised design is considered to satisfy 4NF under the current assumptions.

## 5. Industry Classification Decision

Yahoo Finance provides one representative industry classification per company through the selected data fields.

Although a company may operate in multiple industries, the database stores only its representative industry.

This allows companies to be compared by either sector or industry without introducing additional classifications that are not provided by the data source.

If multiple industries per company are required in the future, a many-to-many relationship could be introduced using a `CompanyIndustry` junction table. An `is_primary` attribute could identify the main industry.

This extension is not part of the current design.