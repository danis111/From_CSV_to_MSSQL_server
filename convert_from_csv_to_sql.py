import numpy as np
import pandas as pd
import pyodbc
file_path='C:/Users/Hp/Desktop/From_CSV_to_MSSQL_server/sales.csv'
df=pd.read_csv(file_path)
df.columns=[x.lower().replace("?","_").replace("#","").replace("*","") for x in df.columns]
df=df.dropna(how='any')
df["year"] = df["year"].astype(int)

servername='I deleted my server name so you need put yourself on it'
database='BikeStores'
username='admin'
password='same as well'
conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+servername+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = conn.cursor()
# this is all it takes to connect to our ms sql database I am using AWS.
cursor.execute("drop table if exists sold")
convert={
       "int64":"int",
       "object":"nvarchar(250)",
       "float64":"float",
       "int32":"int"
}
line = ", ".join("{} {}".format(x, y) for (x, y) in zip(df.columns, df.dtypes.replace(convert)))
cursor.execute("create table sold (%s)" % (line))
conn.commit()
names='rank,name,platform,year,genre,publisher,na_sales,eu_sales,jp_sales,other_sales,global_sales'
values='?,?,?,?,?,?,?,?,?,?,?'
cursor.fast_executemany = True
cursor.executemany("insert into sold (%s) values (%s)" % (names,values),df.values.tolist())
print('{} rows inserted to the sold table'.format(len(df)))
cursor.commit()
conn.close()

# it's really so fast that we just inserted 16291 rows within just 10 secs, we cant do it with just this codes belove
#----------------------------------------------------------------------------------------------------------
# for row in x.itertuples():
#       cursor.execute("insert into sales (rank,name,platform,year,genre,pu_lisher,na_sales,eu_sales,\
#                     jp_sales,other_sales,glo_al_sales) values(?,?,?,?,?,?,?,?,?,?,?)",row.rank,row.name,\
#                     row.platform,row.year,row.genre,row.pu_lisher,row.na_sales,row.eu_sales,row.jp_sales,\
#                     row.other_sales,row.glo_al_sales)
# conn.commit()
# cursor.close()
#----------------------------------------------------- its gonna take a lot time to insert them into db with this code structure





