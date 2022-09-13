# importing required libraries
import pyodbc
import sqlalchemy as sa
from sqlalchemy import create_engine
import urllib

# Making connection with the SQLSERVER Database
conn= urllib.parse.quote_plus(
    'Data Source Name= ;'
    'Driver={};'
        'Server=;'
    'Database=;'
    'Trusted_connection=yes;'

)

coxn=create_engine('mssql+pyodbc:///?odbc_connect={}'.format(conn))