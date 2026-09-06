# Databricks notebook source
# MAGIC %md
# MAGIC # Online Retail Sales Analysis
# MAGIC
# MAGIC ## Project Objective
# MAGIC
# MAGIC This project analyses real-world online retail transaction
# MAGIC data using Databricks, PySpark and SQL.
# MAGIC
# MAGIC The objective is to clean and analyse transactional data
# MAGIC and identify trends in sales, products, customers and
# MAGIC geographic performance.
# MAGIC
# MAGIC ## Tools
# MAGIC
# MAGIC - Databricks
# MAGIC - Python
# MAGIC - PySpark
# MAGIC - SQL
# MAGIC
# MAGIC ## Dataset
# MAGIC
# MAGIC UCI Online Retail Dataset
# MAGIC
# MAGIC ## Analysis Areas
# MAGIC
# MAGIC - Data quality
# MAGIC - Sales performance
# MAGIC - Product performance
# MAGIC - Customer behaviour
# MAGIC - Country performance
# MAGIC - Monthly sales trends

# COMMAND ----------

print("Hello Databricks")

# COMMAND ----------

file_path = "/Volumes/workspace/default/online_retail_data/Online Retail.xlsx"

print(file_path)

# COMMAND ----------

# MAGIC %pip install openpyxl

# COMMAND ----------

# MAGIC %restart_python

# COMMAND ----------

file_path = "/Volumes/workspace/default/online_retail_data/Online Retail.xlsx"

print(file_path)

# COMMAND ----------

import pandas as pd

file_path = "/Volumes/workspace/default/online_retail_data/Online Retail.xlsx"

pdf = pd.read_excel(file_path)

print("Rows:", len(pdf))
print("Columns:", len(pdf.columns))

# COMMAND ----------

pdf.head(10)

# COMMAND ----------

pdf.info()

# COMMAND ----------

print("Rows:", pdf.shape[0])
print("Columns:", pdf.shape[1])

# COMMAND ----------

missing_values = pdf.isnull().sum()

print(missing_values)

# COMMAND ----------

missing_summary = pd.DataFrame({
    "Missing Values": pdf.isnull().sum(),
    "Missing %": (pdf.isnull().sum() / len(pdf) * 100).round(2)
})

missing_summary

# COMMAND ----------

total_rows = len(pdf)
distinct_rows = len(pdf.drop_duplicates())

print("Total rows:", total_rows)
print("Distinct rows:", distinct_rows)
print("Duplicate rows:", total_rows - distinct_rows)

# COMMAND ----------

pdf.drop_duplicates()

# COMMAND ----------

cancelled = pdf[
    pdf["InvoiceNo"].astype(str).str.startswith("C")
]

print("Cancelled transactions:", len(cancelled))

# COMMAND ----------

cancelled.head(10)

# COMMAND ----------

print("Cancelled transactions:", len(cancelled))


# COMMAND ----------

negative_quantity = pdf[pdf["Quantity"] <= 0]

print("Transactions with non-positive quantity:", len(negative_quantity))

# COMMAND ----------

negative_quantity.head(10)

# COMMAND ----------

invalid_price = pdf[pdf["UnitPrice"] <= 0]

print("Transactions with non-positive price:", len(invalid_price))

# COMMAND ----------

invalid_price.head(10)

# COMMAND ----------

clean_df = pdf.drop_duplicates()

print("Rows after removing duplicates:", len(clean_df))

# COMMAND ----------

clean_df = clean_df[
    (clean_df["Quantity"] > 0) &
    (clean_df["UnitPrice"] > 0) &
    (~clean_df["InvoiceNo"].astype(str).str.startswith("C"))
]

print("Rows after cleaning:", len(clean_df))

# COMMAND ----------

print("Original rows:", len(pdf))
print("Cleaned rows:", len(clean_df))
print("Rows removed:", len(pdf) - len(clean_df))

# COMMAND ----------

clean_df["Revenue"] = (
    clean_df["Quantity"] * clean_df["UnitPrice"]
).round(2)

clean_df.head(10)

# COMMAND ----------

clean_df["Year"] = clean_df["InvoiceDate"].dt.year
clean_df["Month"] = clean_df["InvoiceDate"].dt.month

clean_df[["InvoiceDate", "Year", "Month"]].head(10)

# COMMAND ----------

print("Rows:", len(clean_df))
print("Columns:", len(clean_df.columns))
print("Total Revenue:", round(clean_df["Revenue"].sum(), 2))

# COMMAND ----------

clean_df["InvoiceNo"] = clean_df["InvoiceNo"].astype(str)
clean_df["StockCode"] = clean_df["StockCode"].astype(str)
clean_df["Description"] = clean_df["Description"].astype(str)
clean_df["Country"] = clean_df["Country"].astype(str)

clean_df["Quantity"] = clean_df["Quantity"].astype("int64")
clean_df["UnitPrice"] = clean_df["UnitPrice"].astype("float64")
clean_df["Revenue"] = clean_df["Revenue"].astype("float64")
clean_df["Year"] = clean_df["Year"].astype("int64")
clean_df["Month"] = clean_df["Month"].astype("int64")

# COMMAND ----------

spark_df = spark.createDataFrame(clean_df)

print("Rows:", spark_df.count())
print("Columns:", len(spark_df.columns))

# COMMAND ----------

display(spark_df.limit(10))

# COMMAND ----------

spark_df.printSchema()

# COMMAND ----------

spark_df.write.mode("overwrite").saveAsTable("online_retail_sales")

# COMMAND ----------

spark.sql("SHOW TABLES").show()

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM online_retail_sales
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     ROUND(SUM(Revenue), 2) AS Total_Revenue
# MAGIC FROM online_retail_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     SUM(Quantity) AS Total_Units_Sold
# MAGIC FROM online_retail_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(DISTINCT InvoiceNo) AS Total_Orders
# MAGIC FROM online_retail_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     ROUND(
# MAGIC         SUM(Revenue) / COUNT(DISTINCT InvoiceNo),
# MAGIC         2
# MAGIC     ) AS Average_Order_Value
# MAGIC FROM online_retail_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     StockCode,
# MAGIC     Description,
# MAGIC     SUM(Quantity) AS Units_Sold,
# MAGIC     ROUND(SUM(Revenue), 2) AS Revenue
# MAGIC FROM online_retail_sales
# MAGIC GROUP BY StockCode, Description
# MAGIC ORDER BY Revenue DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     StockCode,
# MAGIC     Description,
# MAGIC     SUM(Quantity) AS Units_Sold
# MAGIC FROM online_retail_sales
# MAGIC GROUP BY StockCode, Description
# MAGIC ORDER BY Units_Sold DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     StockCode,
# MAGIC     Description,
# MAGIC     SUM(Quantity) AS Units_Sold,
# MAGIC     ROUND(SUM(Revenue), 2) AS Revenue
# MAGIC FROM online_retail_sales
# MAGIC WHERE StockCode NOT IN ('DOT', 'POST', 'M')
# MAGIC GROUP BY StockCode, Description
# MAGIC ORDER BY Revenue DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     Description,
# MAGIC     ROUND(SUM(Revenue), 2) AS Revenue
# MAGIC FROM online_retail_sales
# MAGIC WHERE StockCode NOT IN ('DOT', 'POST', 'M')
# MAGIC GROUP BY Description
# MAGIC ORDER BY Revenue DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     Year,
# MAGIC     Month,
# MAGIC     ROUND(SUM(Revenue), 2) AS Revenue
# MAGIC FROM online_retail_sales
# MAGIC GROUP BY Year, Month
# MAGIC ORDER BY Year, Month;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     CONCAT(CAST(Year AS STRING), '-', LPAD(CAST(Month AS STRING), 2, '0')) AS Month,
# MAGIC     ROUND(SUM(Revenue), 2) AS Revenue
# MAGIC FROM online_retail_sales
# MAGIC GROUP BY Year, Month
# MAGIC ORDER BY Year, Month;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     Country,
# MAGIC     ROUND(SUM(Revenue), 2) AS Revenue,
# MAGIC     SUM(Quantity) AS Units_Sold
# MAGIC FROM online_retail_sales
# MAGIC GROUP BY Country
# MAGIC ORDER BY Revenue DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     CustomerID,
# MAGIC     COUNT(DISTINCT InvoiceNo) AS Orders,
# MAGIC     SUM(Quantity) AS Units_Sold,
# MAGIC     ROUND(SUM(Revenue), 2) AS Revenue
# MAGIC FROM online_retail_sales
# MAGIC WHERE CustomerID IS NOT NULL
# MAGIC GROUP BY CustomerID
# MAGIC ORDER BY Revenue DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     CustomerID,
# MAGIC     COUNT(DISTINCT InvoiceNo) AS Orders,
# MAGIC     ROUND(SUM(Revenue), 2) AS Revenue,
# MAGIC     ROUND(SUM(Revenue) / COUNT(DISTINCT InvoiceNo), 2) AS Average_Order_Value
# MAGIC FROM online_retail_sales
# MAGIC WHERE CustomerID IS NOT NULL
# MAGIC GROUP BY CustomerID
# MAGIC HAVING COUNT(DISTINCT InvoiceNo) >= 2
# MAGIC ORDER BY Average_Order_Value DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     CustomerID,
# MAGIC     ROUND(SUM(Revenue), 2) AS Revenue
# MAGIC FROM online_retail_sales
# MAGIC WHERE CustomerID IS NOT NULL
# MAGIC GROUP BY CustomerID
# MAGIC ORDER BY Revenue DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     CONCAT(CAST(Year AS STRING), '-', LPAD(CAST(Month AS STRING), 2, '0')) AS Month,
# MAGIC     COUNT(DISTINCT InvoiceNo) AS Orders
# MAGIC FROM online_retail_sales
# MAGIC GROUP BY Year, Month
# MAGIC ORDER BY Year, Month;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     Country,
# MAGIC     ROUND(SUM(Revenue), 2) AS Revenue,
# MAGIC     ROUND(
# MAGIC         SUM(Revenue) / (SELECT SUM(Revenue) FROM online_retail_sales) * 100,
# MAGIC         2
# MAGIC     ) AS Revenue_Percentage
# MAGIC FROM online_retail_sales
# MAGIC GROUP BY Country
# MAGIC ORDER BY Revenue DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(DISTINCT CustomerID) AS Unique_Customers
# MAGIC FROM online_retail_sales
# MAGIC WHERE CustomerID IS NOT NULL;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     ROUND(
# MAGIC         SUM(Revenue) / COUNT(DISTINCT CustomerID),
# MAGIC         2
# MAGIC     ) AS Average_Revenue_Per_Customer
# MAGIC FROM online_retail_sales
# MAGIC WHERE CustomerID IS NOT NULL;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     ROUND(SUM(Revenue), 2) AS Top_10_Customer_Revenue,
# MAGIC     ROUND(
# MAGIC         SUM(Revenue) /
# MAGIC         (SELECT SUM(Revenue) FROM online_retail_sales) * 100,
# MAGIC         2
# MAGIC     ) AS Revenue_Percentage
# MAGIC FROM (
# MAGIC     SELECT
# MAGIC         CustomerID,
# MAGIC         SUM(Revenue) AS Revenue
# MAGIC     FROM online_retail_sales
# MAGIC     WHERE CustomerID IS NOT NULL
# MAGIC     GROUP BY CustomerID
# MAGIC     ORDER BY Revenue DESC
# MAGIC     LIMIT 10
# MAGIC );

# COMMAND ----------

# MAGIC %md
# MAGIC # Key Findings
# MAGIC
# MAGIC The analysis of the Online Retail dataset identified several important business trends:
# MAGIC
# MAGIC * **Strong UK market concentration:** The United Kingdom generated £9.00 million in revenue, accounting for 84.59% of total revenue.
# MAGIC * **Seasonal revenue growth:** Revenue increased significantly during the second half of 2011, reaching a peak of £1.50 million in November 2011.
# MAGIC * **November was the strongest trading month:** November recorded 2,769 orders and the highest monthly revenue in the dataset.
# MAGIC * **High-performing products:** Products such as the Regency Cake Stand, Paper Craft Little Birdie and White Hanging Heart T-Light Holder were among the strongest contributors to product revenue.
# MAGIC * **Customer value varies considerably:** Some customers generated substantial revenue from a small number of orders, while others generated revenue through much more frequent purchasing.
# MAGIC * **Moderate customer concentration:** The top 10 customers generated £1.54 million, representing 14.45% of total revenue.
# MAGIC * **Data quality required attention:** The original dataset contained duplicate records, cancellations, missing customer identifiers and non-positive quantities or prices. These issues were investigated and appropriate records were excluded from the main sales analysis.
# MAGIC * **December should be interpreted cautiously:** The dataset ends on 9 December 2011, meaning December represents only part of the month and should not be compared directly with complete months.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # Business Recommendations
# MAGIC
# MAGIC Based on the analysis, the following actions could help improve business performance:
# MAGIC
# MAGIC 1. **Expand international markets**
# MAGIC    With 84.59% of revenue generated in the UK, the business could investigate opportunities to increase sales in other strong-performing markets such as the Netherlands, Ireland, Germany and France. Localised marketing and targeted promotions could help reduce reliance on the UK market.
# MAGIC
# MAGIC 2. **Prepare for seasonal demand**
# MAGIC    November was the strongest month for both revenue and order volume. The business could increase inventory, marketing activity and operational capacity ahead of the seasonal peak to maximise sales opportunities.
# MAGIC
# MAGIC 3. **Prioritise high-performing products**
# MAGIC    Products generating the highest revenue and unit sales should receive particular attention when planning inventory and promotional campaigns. Stock availability should be monitored closely for these products.
# MAGIC
# MAGIC 4. **Develop customer retention strategies**
# MAGIC    High-value customers represent an important source of revenue. The business could introduce targeted loyalty programmes, personalised offers and repeat-purchase campaigns to encourage continued purchasing.
# MAGIC
# MAGIC 5. **Investigate customer purchasing behaviour**
# MAGIC    The significant difference between high-frequency customers and high-value, low-frequency customers suggests that customers could be segmented based on purchasing behaviour. Different marketing strategies could then be developed for each segment.
# MAGIC
# MAGIC 6. **Improve data quality and customer identification**
# MAGIC    A significant proportion of records do not contain a CustomerID. Improving customer identification and data collection would allow the business to perform more complete customer-level analysis and develop more accurate customer segmentation.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # Conclusion
# MAGIC
# MAGIC This project demonstrated how Databricks, PySpark, SQL and Python can be used to analyse a real-world retail dataset and produce actionable business insights.
# MAGIC
# MAGIC The analysis covered data quality assessment, data cleaning, revenue calculation, sales performance, product performance, geographic trends and customer behaviour. The results showed strong UK market concentration, significant seasonal demand and meaningful differences in customer purchasing behaviour.
# MAGIC
# MAGIC The analysis also demonstrated the importance of data quality when working with real-world transactional data. Duplicate records, cancellations, invalid transactions and missing customer identifiers were investigated before conducting the main analysis.
# MAGIC
# MAGIC Overall, the project transformed raw transactional data into a structured analysis that can support decisions around market expansion, inventory planning, product prioritisation and customer retention.
# MAGIC