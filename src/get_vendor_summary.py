import sqlite3
import pandas as pd
import os
import sys
import time
# Adds the root directory (Inventory-Management) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.logger import logging
from src.data_ingestion_db import ingest_db



def create_vendor_summary(conn):
    """ This function merges the tables(sales,purchases annd vendor invoices) in optimised way """

    #COPIED FROM THE NOTEBOOK CELL
    #write all the tables separatwly then join
    #write all the tables separatwly then join
    optimised_df=pd.read_sql_query("""
                                  WITH FreightSummary AS --copy pasted from the prev vendor_invoice sql
                                  (
                                  SELECT VendorNumber, SUM(Freight) AS TotalFreightCost 
                                  FROM vendor_invoice 
                                  GROUP BY VendorNumber 
                                  ),

                                  PurchaseSummary AS   --copy pasted from the prev purchas join sql(without ORDER BY)
                                  (
                                   SELECT 
                                    p.VendorNumber,p.VendorName, p.Brand, p.PurchasePrice,pp.Volume,pp.Description,pp.Price AS ActualPrice,          
                                    SUM(p.Quantity) AS TotalPurchaseQuantity,
                                    SUM(p.Dollars) AS TotalPurchaseDollars
                                    FROM purchases p
                                    JOIN purchase_prices pp 
                                    ON p.Brand = pp.Brand  
                                    WHERE p.PurchasePrice>0     -- to remoev unwanted 0 in table purchase
                          
                                    GROUP BY 
                                    p.VendorNumber,p.VendorName,p.Brand
                                  ),
                                  
                                  SalesSummary AS   --copy pasted from the prev sales sql(WITHOUT ORDER BY)
                                  (
                                    SELECT
                                    VendorNo,
                                    Brand,
                                    SUM(SalesDollars) AS TotalSalesDollars,
                                    SUM(SalesPrice) as TotalSalesPrice,
                                    SUM(SalesQuantity) as TOtalsalesQuantity,
                                    SUM(ExciseTax) AS TotalExciseTax
                                    FROM Sales
                                    GROUP BY VendorNo, Brand
                                  )
                                  ----------then join all of them
                                  SELECT        --- all that is needed from each table
                                  ps.Description,
                                  ps.VendorName,ps.VendorNumber,ps.Brand,ps.PurchasePrice, ps.ActualPrice, ps.Volume,
                                  ps.TotalPurchaseQuantity, ps.TotalPurchaseDollars,
                                  ss.TotalSalesQuantity, ss.TotalSalesDollars, ss.TotalSalesPrice, ss.TotalExciseTax,
                                  fs.TotalFreightCost
                                  FROM PurchaseSummary ps
                                  LEFT JOIN SalesSummary ss
                                     ON ps.VendorNumber=ss.VendorNo
                                     AND ps.Brand=ss.Brand
                                  LEFT JOIN FreightSummary fs
                                     ON ps.VendorNumber=fs.VendorNumber
                                  
                                  ORDER BY ps.TotalPurchasedollars DESC

                                                                          """,conn)
    return optimised_df

def clean_data(df):
    """This function celans ghe dta and creates new columns"""
    #1
    df['Volume']=df['Volume'].astype('float64')
     # fills 0 for those cells where product was bought but no sale(missing values)
    df.fillna(0,inplace=True)

     #removes white spaces in names
    df['VendorName'].str.strip()

    #adding new columns
    df['GrossProfit']=df['TotalSalesDollars']-df['TotalPurchaseDollars']
    df['ProfitMargin']=(df['GrossProfit']/df['TotalSalesDollars'])*100
    df['StockTurnOver']=(df['TOtalsalesQuantity']/df['TotalPurchaseQuantity'])
    #sales to purchase ratio
    df['SalestoPurchaseRatio']=(df['TotalSalesDollars']/df['TotalPurchaseDollars'])
    return df
   




if __name__=='__main__':
 #create the db cinnection
 conn=sqlite3.connect('inventory.db')

 logging.info('Creating the optimised vendor summary table')
 summary_df=create_vendor_summary(conn)
 logging.info(summary_df.head())
 
 logging.info('Cleaning data')
 clean_df=clean_data(summary_df)
 logging.info(clean_df.head())

 logging.info('Ingesting data(cleandf) to convert it to a table')
 ingest_db(clean_df,'vendor_sales_summary',conn) 
 logging.info('Done')
 # the table name passed here is the vendor sales summary

