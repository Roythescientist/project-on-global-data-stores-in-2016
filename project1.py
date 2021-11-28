import pandas as pd
import numpy as np
from pandas.core.algorithms import value_counts

global_datadf=pd.read_csv('C:/Users/ROY/Downloads/Pandas_Project_Session/Pandas_Project_Session/data/global_superstore/global_superstore.csv')
print(global_datadf)
pd.set_option('display.min_rows',1000)
pd.set_option('display.max_rows',50)
pd.set_option('max_colwidth',100)

print(global_datadf.head())
print(global_datadf.describe())
print(global_datadf.info())
order_date=global_datadf['Order Date'].to_list()
ship_date=global_datadf['Ship Date'].to_list()

order_datetime=pd.to_datetime(order_date)
ship_datetime=pd.to_datetime(ship_date)
Order_date=pd.Series(order_datetime,name='Order_Date')
Ship_date=pd.Series(ship_datetime,name='Ship_Date')
print(order_datetime,ship_datetime)

value_columns=global_datadf.columns.values
print(value_columns)
#dropping unwanted column
global_datadf.drop(columns=['Row ID','Order Date','Ship Date','Customer ID','Postal Code'])
global_data=pd.concat([global_datadf, Order_date, Ship_date],axis=1)
print(global_data)
global_data=global_data.reindex(columns=['Order ID', 'Order_Date', 'Ship_Date', 'Ship Mode','Customer Name', 'Segment', 'Postal Code', 'City','State', 'Country', 'Region', 'Market', 'Product ID', 'Category',
       'Sub-Category', 'Product Name', 'Sales', 'Quantity', 'Discount', 'Profit', 'Shipping Cost', 'Order Priority'])
print(global_data.head(n=4))

print(global_data['Shipping Cost'].astype(int)[:10])

## check whether all the values of columns 'Sales' & 'Profit' contains $ symbol or not
if global_data['Sales'].str.contains('$').any():
    print('Yes: $ is present in the column sales')
if global_data['Profit'].str.contains('$').any():
    print('Yes: $ is present in column of profit')

# clean the columns 'Sales' & 'Profit' which consists of '$', '(', & ')' symbols
global_data['Sales']=global_data['Sales'].str.replace('$','',regex=True)
global_data['Sales']=global_data['Sales'].str.replace(',','',regex=True)
print(global_data[:10])
global_data['Profit']=global_data['Profit'].str.replace('$','')
print(global_data[:10])
global_data['Profit']=global_data['Profit'].str.replace('(','')
print(global_data[:10])
global_data['Profit']=global_data['Profit'].str.replace(')','')
print(global_data[:20])
global_data['Profit']=global_data['Profit'].str.replace(',','')
print(global_data[:20])
global_data['Sales']=global_data['Sales'].str.replace(')','',regex=True)
global_data['Sales']=global_data['Sales'].str.replace('(','',regex=True)
# After removing the symbols, convert them to a numeric columns and of type 'int'
global_data['Profit']=pd.to_numeric(global_data['Profit'], downcast='signed')
global_data['Sales']=pd.to_numeric(global_data['Sales'],downcast='integer')
print(global_data)
global_data['Profit']=global_data['Profit'].astype(int)
global_data['Sales']=global_data['Sales'].astype(int)
global_data.info()

## 1. Total how many orders have cross the shipping cost of 500?
condition1=(global_data['Shipping Cost']>500.00)
shipping_500=global_data[condition1]

print(len(shipping_500['Order ID']))

#Count the number of segments, countries, regions, markets, categories, and sub-categories present in the global_superstore_2016 data
print(global_data['Segment'].value_counts())
print(global_data['Region'].value_counts())
print(len(global_data['Region'].value_counts()))
print(global_data['Country'].value_counts())
print(len(global_data['Country'].value_counts()))
print(global_data['Market'].value_counts())
print(len(global_data['Market'].value_counts()))
print(global_data['Category'].value_counts())
print(len(global_data['Category'].value_counts()))
print(global_data['Sub-Category'].value_counts())
print(len(global_data['Sub-Category'].value_counts()))

# Get the list of Order ID's where the Indian customer's 
# have bought the things under the category 'Technology' after paying the Shipping Cost more than 500.
cond_india=(global_data['Country']=='India')&(global_data['Category']=='Technology')&(global_data['Shipping Cost']>500)
list_ID=global_data[cond_india]
#Get the list of Order ID's where the Indian customer's have bought the things under the category 'Technology'  where the Sales is greater than 500
indian_Id=list_ID['Order ID'].to_list()
print(indian_Id)
#How many people from the State 'Karnataka' have bought the things under the category 'Technology'
people_karnata_cond=(global_data['Country']=='India')&(global_data['Category']=='Technology')
state_cond=global_data[people_karnata_cond]
print(len(state_cond[state_cond['State']=='Karnataka']))

#Get the list of countries where the 'Profit' and 'Shipping Cost's are greater than or equal to 2000 and 300 respectively.
grouped_data=(global_data['Profit']>=2000)&(global_data['Shipping Cost']>=300)
global_grouped=global_data[grouped_data]
print(global_grouped[:5])
list_of_industries=global_grouped['Country'].drop_duplicates()
print(list_of_industries)
print('the total number of countries is:',len(list_of_industries))

#Find the list of Indian states where the people have purchased the things under the category Technology
indian_state=(global_data['Country']=='India')&(global_data['Category']=='Technology')
indian_states=global_data[indian_state]
india_states=indian_states['State'].drop_duplicates().to_list()
print(india_states)
print(len(india_states))

#Find the overall rank of "India" where the 'Profit' is maximum under the category 'Technology'
maximum_rank=((global_data['Country']=='India')&(global_data['Category']=='Technology'))
maxima_rank=global_data[maximum_rank]
maxi=maxima_rank['State'].max()
print('the state with maximum profit is:',maxi)
print('the maximum profit is:',max(global_data['Profit']))

#Display the data with min, max, average and std of 'Profit' & 'Sales' for each Sub-Category under each Category
sort_data=global_data.groupby(by=['Country','Category','Sub-Category'],as_index=True)
functions=[('min_value','min'),('max_value','max'),('std_value','std')]
sort_Data=sort_data['Profit','Sales'].agg(functions)
print(sort_Data)