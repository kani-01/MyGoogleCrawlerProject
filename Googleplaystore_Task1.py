#!C:/Users/Ezhil Malliga/AppData/Local/Programs/Python/Python36/python
# -*- coding: utf-16 -*-

# Author    : Kanimozhi Kalaichelvan
# Professor : Dr.Haroon Malik
# Website   : Google PlayStore (blocks if same url is used repeatedly over and over again)

# import required packages 
import requests # For HTTP requests
from datetime import datetime # Datetime for TimeStamp
# import beautifulsoup
from bs4 import BeautifulSoup
# import for Database Connectivity
import MySQLdb

# Creating TimeStamp
gettime = datetime.now()
mytime= gettime.strftime('%Y-%m-%d %H:%M:%S')
print(mytime)

# Function that implements Task 1 
# websitelink is the URL from which it fetches data
def web(pagenumber,websitelink):
    if(pagenumber > 0):
        parsedata = requests.get(websitelink).text
        count = 0
        # Using BeautifulSoup to Parse Data
        s = BeautifulSoup(parsedata, "html.parser")
        # Connect to MySQL Database
        db = MySQLdb.connect(host="10.103.92.251", user="playstoreinfo", passwd="playstoreinfo", db="playstoreinfo")   
        cur = db.cursor()
        
        try:
            # Checking whether URL data is already present, if present just update the TimeStamp
            cur.execute("""select * from PageInfo where linkprovided =%s""",(websitelink,))
            
            row_count1 = cur.rowcount
            print("Existence in : ",row_count1)  
            # If not present, add the new URL to PageInfo Table
            if row_count1 == 0:
                cur.execute("insert into PageInfo(linkprovided, timestamp) VALUES (%s,%s)",(websitelink, mytime,))
            # If URL already present, just update TimeStamp
            else:
                print("Link Address already present in PageInfo")
                cur.execute("update PageInfo set timestamp  =%s where linkprovided  =%s",(mytime,websitelink)) 
        except:
            print("Error") # If data is already present, primary key doesnt allow to insert the data again         
        
        # Extracting required data such as doc-id, title, hreflink from the html data
        for i in s.findAll('div', {'class':'card no-rationale square-cover apps small'}):
            count = count+1
            print("Count is",count)
            # Extract Doc-id
            docidname = i.get('data-docid')
            print("Doc id : ",docidname)              
            
            # Removes unnecessary characters from the titlename
            for j in i.findAll('a',{'class':'title'}):
                # Extract Title
                titlename = j.get('title')
                print("Title  : ",titlename)
                titlename = titlename.replace('–','-')
                titlename = titlename.replace('’','')
                titlename = titlename.replace('웃','')
                titlename = titlename.replace('—','-')
                titlename = titlename.replace('™','')
                # Extract Href Link
                hreflink = j.get('href')
                print("Link   : ",hreflink)         
                        
            try:
                #cur.execute("""insert into task1_appsinfo (docid,Title,linkaddress,CurrentTimestamp) VALUES (%s,%s,%s,%s) """,(docidname, titlename,hreflink,mytime))
                cur.execute("""select * from task1Appdata where docid =%s and linkaddress =%s""",(docidname,hreflink))
                row_count = cur.rowcount
                # Checks if App Data is already present, if present do not insert again, just update Timestamp, if not present insert the App Data
                print("Existence : ",row_count)
                if row_count == 0:
                    cur.execute("""insert into task1Appdata (docid,Title,linkaddress,CurrentTimestamp) VALUES (%s,%s,%s,%s) """,(docidname, titlename,hreflink,mytime))
                    db.commit() 
                    print('Inserted Successfully')
                else:
                    print("App Data Exists Already")    
                    cur.execute("update task1Appdata set CurrentTimestamp  =%s where linkaddress  =%s",(mytime,hreflink)) 
            except:
                print('Error: ')
            
        
#web(1,'https://play.google.com/store/search?q=games&c=apps&hl=en')

# Gets User Input of URL link
linkprovided = str(input("Enter your Google PlayStore URL :\n")) 
# Please Provide URL like given below : Category may be different
# https://play.google.com/store/apps/collection/topselling_free?hl=en
# https://play.google.com/store/apps/category/GAME_ADVENTURE

# Calls Function to start crawling the provided URL
web(1,linkprovided)