import sqlite3
import pandas as pd

data = pd.ExcelFile('./data/Choice Data.xlsx')

tables = {}

for table in data.sheet_names:
    df = pd.read_excel(data, sheet_name=table, nrows=0)
    tables[table] = df.columns.to_list()
    
print(tables)

conn = sqlite3.connect('data/choice.db')
cursor = conn.cursor()

for sheet_name in data.sheet_names:
    df = pd.read_excel(data, sheet_name=sheet_name)
    df.to_sql(sheet_name, conn, index=False, if_exists="replace")

rename = """
ALTER TABLE rw_org
RENAME COLUMN '[' TO org_id;
"""

cursor.execute(rename)

prediction = """
CREATE TABLE prediction AS
SELECT header.donationdate posting_date,
header.donorname donor_id,
lines.totalgrossweight gross_weight,
header.warehousename branch_code,
lines.storagerequirement storage_code
FROM amx_donation_header header
JOIN amx_donation_lines lines ON header.donationnumber = lines.donationnumber
"""

cursor.execute(prediction)

conn.commit()
conn.close()