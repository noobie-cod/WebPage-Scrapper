                                                                #Modules Needed to Script the data from html

import requests 
from bs4 import BeautifulSoup
import re
import itertools
import webbrowser
import urllib


                                                # Query to be requested and Variable and list to be created in order to save data.
                                                
                                                
i = 1 ;
URL = []
qry = str(input("Enter the query to be Searched for : \n").strip())
qry = urllib.parse.quote_plus(qry)


                                                                            # Scrippting part
                                                                            
url = "http://stackoverflow.com/search?q="
k = "http://stackoverflow.com/"
r = url+qry;
html = requests.get(r)
soup = BeautifulSoup(html.content, 'html.parser')


                                                            # To extract data with question number.


g_data = soup.find_all("div" ,{"class":"search-results js-search-results"},{"id":"question-summary-"})
for item in g_data:
	n_data = item.find_all("div",{"class":"result-link"})
	m_data = item.find_all("span",{"class":"vote-count-post"})
	a_data = item.find_all("div",{"class":"status answered-accepted"})
	for a,b,c in zip(n_data,m_data,a_data):
		print(i ,(a.text).strip())
		print("Votes",(b.text).strip())
		print(((c.text)).strip())
		print ("-" * 40)
		i = i + 1;
		

                                                                #  To Extract the url of the link of the question.

                                                                
for item in g_data:
	n_data = item.find_all("div",{"class":"result-link"})
	for a in n_data:
		k_data = a.find_all("a")
		for b in k_data:
			a = str(b.get("href"))
			URL.insert(i-1,a)
			i=i+1
		
                                                        # To ask wheather user wants to open any answer to the question :
                                                        

ans = int(input("Do u wish to open any answer?\n1.Yes\t2.No\n"))


                                                            # To open the question requested to open in the browser.


if (ans==1):
	val = int(input("Enter the number of questions u want us to open in browser:\n"))
	HTML = k+URL[val-1]
	webbrowser.open(HTML)
else:
	print("Thank You")	
	





