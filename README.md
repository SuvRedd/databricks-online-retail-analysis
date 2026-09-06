# Online Retail Sales Analysis Using Databricks

## Project Overview

This project analyses real-world online retail transaction data using Databricks, PySpark, SQL and Python.

The objective was to transform raw transactional data into a clean analytical dataset and identify trends in sales performance, products, geographic markets and customer behaviour.

The project demonstrates an end-to-end data analysis workflow, including data exploration, data quality assessment, cleaning, transformation, SQL analysis, visualisation and business recommendations.

## Tools & Technologies

* Databricks
* PySpark
* SQL
* Python
* Pandas
* Spark DataFrames
* GitHub

## Dataset

The project uses the **Online Retail** dataset from the UCI Machine Learning Repository.

The dataset contains **541,909 transaction records** from a UK-based online retailer covering transactions between December 2010 and December 2011.

The dataset contains 8 fields:

* InvoiceNo
* StockCode
* Description
* Quantity
* InvoiceDate
* UnitPrice
* CustomerID
* Country

Dataset source: [UCI Machine Learning Repository – Online Retail](https://archive.ics.uci.edu/dataset/352/online%2Bretail)

## Data Preparation

The original dataset was assessed for data-quality issues before analysis.

The preparation process included:

* Identifying missing values
* Identifying duplicate records
* Investigating cancelled transactions
* Identifying non-positive quantities
* Identifying non-positive prices
* Removing exact duplicate records
* Excluding cancellation and non-positive sales transactions from the main sales analysis
* Creating a calculated Revenue field using Quantity × UnitPrice
* Creating Year and Month fields for time-based analysis

The resulting analytical dataset contained **524,878 records**.

## Analysis Performed

### Sales Analysis

Key performance indicators were calculated including:

* Total revenue
* Total units sold
* Total orders
* Average order value
* Monthly revenue
* Monthly order volume

### Product Analysis

Products were analysed based on:

* Revenue generated
* Units sold

Service-related codes such as postage and manual charges were excluded when ranking physical products.

### Geographic Analysis

Revenue and units sold were analysed by country to identify the strongest geographic markets.

### Customer Analysis

Customer-level analysis examined:

* Customer revenue
* Number of orders
* Units purchased
* Average order value
* Revenue contribution from the highest-value customers

## Key Findings

* Total revenue was **£10.64 million**.
* The dataset contained **5.57 million units sold** across **19,960 orders**.
* Average revenue per order was **£533.17**.
* There were **4,338 customers with a recorded CustomerID**.
* Average revenue per identifiable customer was **£2,048.69**.
* The United Kingdom generated **84.59% of total revenue**.
* November 2011 was the strongest month, generating approximately **£1.50 million** in revenue across **2,769 orders**.
* The top 10 customers generated **£1.54 million**, representing **14.45% of total revenue**.
* Customer purchasing behaviour varied considerably, with some high-value customers placing relatively few orders while others generated value through frequent purchases.
* December 2011 represents only part of the month because the dataset ends on 9 December 2011.

## Business Recommendations

Based on the analysis, potential business actions include:

1. Investigate opportunities to expand sales in international markets and reduce reliance on the UK market.
2. Prepare inventory and marketing activity ahead of seasonal demand peaks.
3. Prioritise high-performing products when planning inventory and promotions.
4. Develop targeted retention strategies for high-value customers.
5. Segment customers based on purchasing frequency and value.
6. Improve customer identification and data collection to enable more complete customer analysis.

## Project Structure

```text
databricks-online-retail-analysis/
│
├── README.md
│
├── notebooks/
│   └── 01_Online_Retail_Analysis
│
└── screenshots/
    ├── data_quality.png
    ├── monthly_revenue.png
    ├── monthly_orders.png
    ├── top_products.png
    ├── country_revenue.png
    └── customer_analysis.png
```

## Author

**Suvaan Reddy**

This project was created as a demo Data Analyst project to demonstrate practical experience with Databricks, PySpark, SQL and Python.
