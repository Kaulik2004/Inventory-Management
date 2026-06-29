# Inventory-Management
# Dashboard
<img width="1454" height="744" alt="image" src="https://github.com/user-attachments/assets/10653a63-5a69-4095-8dbd-9e952d006340" />

# Inventory Management & Portfolio Performance Analysis

A comprehensive data engineering and business intelligence project focused on extracting, processing, and analyzing inventory data. This repository features an end-to-end pipeline that ingests data into a local relational database, performs exploratory data analysis (EDA) using Python, and builds dynamic visual reporting dashboards within Power BI.

## 🚀 Key Features

* **Database Integration:** Automates transactional ingestion pipelines directly into a lightweight, local SQLite instance (`inventory.db`).
* **Performance Engineering Metrics:** Custom Python and DAX logic calculating itemized metrics including:
* Gross Profit Margins
* Vendor Purchase Contributions (`PurchaseContri%`)
* Unsold Capital formulas


* **Advanced Statistical Modeling:** Utilizes statistical percentiles (`PERCENTILE.INC`) to systematically flag and dynamically segment low-volume, high-margin items (**"Target Brands"**).
* **Business Intelligence Dashboarding:** Includes a structured Power BI environment showcasing quadrant scatter plots, top vendor rankings, and operational summaries for proactive stakeholder decision-making.


Open the companion Power BI workbook to review live reporting metrics, utilizing filtered visualizations mapping brand segments under custom performance filters.
