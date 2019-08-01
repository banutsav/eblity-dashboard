import time
import mysql.connector as mc
from mysql.connector import Error
import pandas as pd
from yattag import Doc
import html
import viz
# Credentials for DB connection
import cred

# Save plot to file
def writeResults(connection):
	doc, tag, text = Doc().tagtext()
	# Generate HTML
	with tag('html'):
		with tag('head'):
			with tag('script', src="https://cdn.plot.ly/plotly-latest.min.js"):
				pass
			with tag('title'):
				text('Eblity')
		with tag('body'):
				with tag('div'):
					text(viz.scatterTopicSubTopics(connection))
	
	result = doc.getvalue()
	f = open("images/results.html", "w")
	f.write(html.unescape(result))
	f.close() 

try:
	print('Starting program execution')
	start = time.time()
	connection = mc.connect(host=cred.SERVER,database=cred.DB,user=cred.USER,password=cred.PASS)
	
	if connection.is_connected():
		db_Info = connection.get_server_info()
		print('Connected to MySQL database:',db_Info)
		writeResults(connection)

	end = time.time()
	print('Execution Time: ' + str(round(end-start,2)) + ' secs')   

except Error as e :
    print ('Error while connecting to MySQL', e)
finally:
    #closing database connection.
    if(connection.is_connected()):
        connection.close()
        print('MySQL connection is closed')