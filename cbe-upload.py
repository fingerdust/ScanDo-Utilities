import _mssql
import uuid
conn = _mssql.connect(server='localhost', user='sa', password='waveoman', \
    database='takestock03')
conn.execute_query("SELECT TOP 1 gId FROM tblStocktake ORDER BY dStarted DESC;")
for row in conn: 
	g_id = str(row['gId'])
sql = "SELECT  sBarcode, fQty, dScanned FROM tblStocktakeLineItem WHERE gStocktakeId = %s;"
conn.execute_query(sql, g_id)
for row in conn:
	print(str(row['sBarcode'])+', '+str(row['fQty'])+', '+str(row['dScanned']))