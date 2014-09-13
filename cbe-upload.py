import _mssql
import csv

# Takes data directly from last stocktake (using the takestock03 db) 
# to create the required .csv for upload to CBE
# 
# Format is  barcode,qty,YYYY-MM-DD,HH:mm:ss
# Latest entry only incuded whose quantity is a sum of all entries 

conn = _mssql.connect(server='localhost', user='sa', password='waveoman', \
    database='takestock03')
conn.execute_query("SELECT TOP 1 gId, sCustomerCode FROM tblStocktake ORDER BY dStarted DESC;")
for row in conn: 
	g_id = str(row['gId'])
	customer = row['sCustomerCode']
sql = "SELECT sBarcode, fQty, dScanned FROM tblStocktakeLineItem WHERE gStocktakeId = %s ORDER BY dScanned;"
conn.execute_query(sql, g_id)

dict = {}
for row in conn:
	barcode = str(row['sBarcode'])
	qty     = row['fQty']
	date    = str(row['dScanned']).split()[0]
	time    = str(row['dScanned']).split()[1]
	if barcode in dict:
		dict[barcode][0] += qty
		dict[barcode][1] = date
		dict[barcode][2] = time
	else: 
		dict[barcode] = [qty, date, time]
conn.close(); 

# Path set to run in virtual machine machine os 
output_file = "C:\\Documents and Settings\\scando\\Desktop\\CBE Exports\\" + customer + ".csv"
with open(output_file,'w') as f:
    for key in dict: 
    	f.write(key+","+str(dict[key][0])+","+dict[key][1]+","+dict[key][2]+"\n"