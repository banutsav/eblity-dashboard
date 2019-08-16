import time
import mysql.connector as mc
from mysql.connector import Error
import pandas as pd
from yattag import Doc
import html
import viz
# Credentials for DB connection
import cred
import dbmodules as dm

# Create the Visualizations
def createVisuals(connection, studentid, subject):
	figures = []
	#figures.append(viz.scatterTopicSubTopics(connection, 8, 'mathematics'))
	#figures.append(viz.scatterTopicProgress(connection, 10, 'mathematics'))
	figures.append(viz.barTopicProgress(connection, 10, 'mathematics'))
	#figures.append(viz.stackedBarPendingTopics(connection, 10, 'mathematics'))
	'''
	user = dm.getUser(connection, studentid); username = user[0]; name = user[1] + ' ' + user[2]
	completed = dm.completedTopics(connection, studentid, subject)
	for row in completed:
		topic = row[0]
		figures.append(viz.scatterCompletedTopics(connection,username,topic))
	'''
	return figures

# Save plot to file
def writeResults(figures, name, subject):
	doc, tag, text = Doc().tagtext()
	# Generate HTML
	with tag('html'):
		with tag('head'):
			with tag('script', src="https://cdn.plot.ly/plotly-latest.min.js"):
				pass
			with tag('title'):
				text(name + ' | ' + subject)
		with tag('body'):
			for figure in figures:	
				with tag('div'):
					text(figure)
				
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
		figures = createVisuals(connection, 1, 'mathematics')
		user = dm.getUser(connection, 1); username = user[0]; name = user[1] + ' ' + user[2]
		writeResults(figures, name, 'mathematics')
		
	end = time.time()
	print('Execution Time: ' + str(round(end-start,2)) + ' secs')   

except Error as e :
    print ('Error while connecting to MySQL', e)
finally:
    #closing database connection.
    if(connection.is_connected()):
        connection.close()
        print('MySQL connection is closed')