#!C:/Users/Ezhil Malliga/AppData/Local/Programs/Python/Python36/python
# -*- coding: utf-16 -*-

# Author    : Kanimozhi Kalaichelvan
# Professor : Dr.Haroon Malik
# Website   : Appbrain

# import required packages 
from datetime import datetime
#import os, sys
import requests # For HTTP requests
# import beautifulsoup
from bs4 import BeautifulSoup
# import for database connectivity
import MySQLdb

# Declaring Queues for scrolling all pages of a particular Category in Appbrain Website
Queue=[]
ReferenceQueue=['https://www.appbrain.com/stats/google-play-rankings']
count = 0
# Creating TimeStamp
gettime = datetime.now()
mytime= gettime.strftime('%Y-%m-%d %H:%M:%S')
print(mytime)

# Function that implements Task 2 
# Pagenumber keeps track of number of page it is fetching the apps from since it fetches all app data from all 5 pages of a given Category.
# websitelink is the URL from which it fetches data
def web(pagenumber,websitelink,count):
    global mytime
    ReferenceQueue.append(websitelink)
    # Scrolls all Pages
    if(pagenumber > 0):
        parsedata = requests.get(websitelink).text
        count = count
        flag = 0
        s = BeautifulSoup(parsedata, "html.parser")
        db = MySQLdb.connect(host="10.103.92.251", user="playstoreinfo", passwd="playstoreinfo", db="playstoreinfo")  
        cur = db.cursor()       
        
        # Fetching Category of the Page
        for ct in s.findAll('meta',{'name':'description'}):
            categoryofpage = ct.get('content')
            print("Category of the page is ",categoryofpage)
            print(type(categoryofpage))
            
        try:
            # Check if the Category has already been fetched, if yes - just update time, if no - add Category Info to taskappbraincategoryinfo Table
            #cur.execute("""select * from taskappbraincategoryinfo""",categoryofpage) 
            cur.execute("""select * from taskappbraincategoryinfo where Pagevisited =%s""",(categoryofpage,)) 
            row_count1 = cur.rowcount
            print("Existence in : ",row_count1)  
            if row_count1 == 0:
                 #cur.execute("insert into PageInfo(linkprovided, timestamp) VALUES (%s,%s)",(websitelink, mytime,))
                cur.execute("insert into taskappbraincategoryinfo (Pagevisited,CurrentTimestamp) VALUES (%s,%s)",(categoryofpage, mytime,))
            else:
                print("Link Address already present in taskappbraincategoryinfo")
                cur.execute("update taskappbraincategoryinfo set timestamp  =%s where Pagevisited  =%s",(mylogtime,categoryofpage)) 
        except:
            print("Error") # If data is already present, primary key doesnt allow to insert the data again            
        
        for q in s.findAll('tr'):
            for i in q.findAll('td', {'class':'ranking-app-cell'}):
                count = count + 1
                print("Count is",count)
                k = 0
                for j in i.findAll('a'):
                    if k == 0:
                        # Fetches Data such AppName, hreflink
                        hreflink = j.get('href')
                        print("Href is : ",hreflink) 
                        Appname = j.get_text()
                        print("App Name is : ",Appname)
                        Appname = Appname.replace('–','-')
                        Appname = Appname.replace('’','')
                        Appname = Appname.replace('웃','')
                        Appname = Appname.replace('—','-')
                        Appname = Appname.replace('™','')
                        #Appname = Appname.replace('™️','')️
                        #Appname = Appname.replace(r"[,.;’@#?!&$]+\*",'')
                        #print("App Name is : ",Appname)
                    k = 1
                    
                    # Fetches Data such Rating of the App
            for h in q.findAll('td', {'class':'ranking-rating-cell'}):
                for p in h.findAll('span'):
                    rating = p.get_text()
                    print("Rating is : ",rating)
                    flag = 1

            if flag == 1:
                #statusflag=1
                try:
                    # Check if Data already exists if yes - check rating value
                    cur.execute("""select * from task2appbrain where NameofApp =%s and href =%s""",(Appname,hreflink))
                    row_count = cur.rowcount
                    print("Existence : ",row_count)  
                    if row_count == 0:
                        statusflag=1
                        cur.execute("insert into task2appbrain(href,NameofApp,Rating,CurrentTimestamp,statusflag) VALUES (%s,%s,%s,%s,%s)",(hreflink, Appname, rating, mytime,statusflag))
                    else:
                        # Check if Rating is also same for the Existing App if yes just update timestamp, if no, Update the new Rating
                        cur.execute("""select * from task2appbrain where NameofApp =%s and href =%s and Rating =%s""",(Appname,hreflink,rating))
                        row_count1 = cur.rowcount
                        if row_count1 != 0 :
                            #statusflag=1
                            print("Data already exists")
                            print("Existence 1 : ",row_count1)
                            cur.execute("update task2appbrain set CurrentTimestamp  =%s, statusflag =%s where href  =%s",(mytime,statusflag,hreflink))
                        else:
                            statusflag = 1;
                            cur.execute("""update task2appbrain set Rating =%s, CurrentTimestamp  =%s, statusflag =%s where NameofApp =%s and href =%s""",(rating,mytime,statusflag,Appname,hreflink,))
                            print("Rating and Timestamp Alone is updated")
                    db.commit() 
                    
                except:
                    print('Error: ')
                else:
                    print('Success')    
            flag = 0
        
        for u in s.findAll('div', {'class':'list-pagination'}): 
            #global n
            for v in u.findAll('a'):
                nextpage = v.get('href')
                #print("Href is : ",nextpage)
                # Adding all 5 Pages of given Category to fetch Data from
                nextcrawlingpage = 'https://www.appbrain.com' + nextpage
                if nextcrawlingpage not in Queue and nextcrawlingpage not in ReferenceQueue:
                    Queue.append(nextcrawlingpage)
                    ReferenceQueue.append(nextcrawlingpage)                   
                    
        print()
        # Prints the Queue that contains Remaining pages to crawl
        print("The Queue of pages to crawl is :")            
        print(Queue)
        
        
        while(len(Queue)!=0):
            try:
                # Fetch the next URL
                nextvistinglink = Queue.pop(0)
                print(nextvistinglink)
                web(1, nextvistinglink,count)
            except:
                # Prints when all Pages have been Crawled
                print("ALL PAGES HAVE BEEN CRAWLED")

# Gets User Input of URL link
givelink = str(input("Enter your Google PlayStore URL :\n")) # https://www.appbrain.com/stats/google-play-rankings/top_free/all/us

# Calls Function to start crawling the provided URL
web(1,givelink,count) 
# Please Provide URL like given below : Category may be different
# https://www.appbrain.com/stats/google-play-rankings/top_free/libraries_demo/us
# https://www.appbrain.com/stats/google-play-rankings/top_free/education/us
# https://www.appbrain.com/stats/google-play-rankings/top_paid/food_drink/us

#web(1,'https://www.appbrain.com/stats/google-play-rankings/top_paid/action/us',count)
 