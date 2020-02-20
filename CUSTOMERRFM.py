import warnings

import pandas as pd

warnings.filterwarnings('ignore')
df = pd.read_excel("D:Online Retail.xlsx")
# print("**",df)
df.head()
df1 = df
df1.Country.nunique()
df1.Country.unique()
customer_country = df1[['Country', 'CustomerID']].drop_duplicates()
customer_country.groupby(['Country'])['CustomerID'].aggregate('count').reset_index().sort_values('CustomerID',
                                                                                                 ascending=False)
df1 = df1.loc[df1['Country'] == 'United Kingdom']
df1.isnull().sum(axis=0)
print(df1.shape)
df1 = df1[pd.notnull(df1['CustomerID'])]
print(df1.shape)
print(df1.UnitPrice.min())
print(df1.Quantity.min())

df1 = df1[(df1['Quantity'] > 0)]
print(df1.shape)
print(df1.info())
# TUFAN EKLEDI 

def unique_counts(df1):
    for i in df1.columns:
        count = df1[i].nunique()
        print(i, ": ", count)


unique_counts(df1)

df1['TotalPrice'] = df1['Quantity'] * df1['UnitPrice']
df1['InvoiceDate'].min()
df1['InvoiceDate'].max()
import datetime as dt

NOW = dt.datetime(2011, 12, 10)
df1['InvoiceDate'] = pd.to_datetime(df1['InvoiceDate'])

rfmTable = df1.groupby('CustomerID').agg({'InvoiceDate': lambda x: (NOW - x.max()).days,
                                          'InvoiceNo': lambda x: len(x),
                                          'TotalPrice': lambda x: x.sum()})

rfmTable['InvoiceDate'] = rfmTable['InvoiceDate'].astype(int)
rfmTable.rename(columns={'InvoiceDate': 'recency',
                         'InvoiceNo': 'frequency',
                         'TotalPrice': 'monetary_value'}, inplace=True)
rfmTable.head()
first_customer = df1[df1['CustomerID'] == 12346.0]
print(first_customer)

quantiles = rfmTable.quantile(q=[0.25, 0.5, 0.75])
print(quantiles)
quantiles = quantiles.to_dict()
segmented_rfm = rfmTable
print(segmented_rfm)


def RScore(x, p, d):
    if x <= d[p][0.25]:
        return 1
    elif x <= d[p][0.50]:
        return 2
    elif x <= d[p][0.75]:
        return 3
    else:
        return 4


def FMScore(x, p, d):
    if x <= d[p][0.25]:
        return 4
    elif x <= d[p][0.50]:
        return 3
    elif x <= d[p][0.75]:
        return 2
    else:
        return 1


segmented_rfm['r_quartile'] = segmented_rfm['recency'].apply(RScore, args=('recency', quantiles,))
segmented_rfm['f_quartile'] = segmented_rfm['frequency'].apply(FMScore, args=('frequency', quantiles,))
segmented_rfm['m_quartile'] = segmented_rfm['monetary_value'].apply(FMScore, args=('monetary_value', quantiles,))
print(segmented_rfm)

segmented_rfm['RFMScore'] = segmented_rfm.r_quartile.map(str) + segmented_rfm.f_quartile.map(
    str) + segmented_rfm.m_quartile.map(str)

segmented_rfm.head()

segmented_rfm[segmented_rfm['RFMScore'] == '111'].sort_values('monetary_value', ascending=False).head(10)
