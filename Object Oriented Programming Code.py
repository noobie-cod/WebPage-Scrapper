import requests
from bs4 import BeautifulSoup
import re
import sys
import itertools
import webbrowser
import urllib


STACKOVERFLOW_URL = "http://stackoverflow.com"
QUERY_URL = STACKOVERFLOW_URL + "/search?q="


def sanitizeStr(string):
    return string.encode("ascii", "ignore")

class Question(object):

    __instanceCount = 0

    def __init__(self, question="", upvotes=0, totalAnswers=0, resultLink=None):
        self.text = question
        self.upvotes = upvotes
        self.resultLink = resultLink
        self.totalAnswers = totalAnswers
        self.id = Question.__instanceCount + 1
        Question.__instanceCount += 1

if __name__ == "__main__":
    qry = str(input("Enter the query to be Searched for : ")).strip()
    qry = urllib.parse.quote_plus(qry)

    requestUrl = QUERY_URL + qry;
    try:
        requestObj = requests.get(requestUrl)
    except Exception as e:
        print ("Error occured: " + str(e))
        sys.exit(1)

    if requestObj.status_code != 200:
        print ("Unable to fetch answers from stackoverflow.com. HTTP request returned error: " % requestObj.status_code)
        sys.exit(1)

    soup = BeautifulSoup(requestObj.content, 'html.parser')
                                                                # To extract data with question number.

    topQuestionsObj = soup.find_all("div" ,{"class":"question-summary search-result"})
    questionList = []
    for questionObj in topQuestionsObj:
        question = ""
        resultLink = ""
        voteCount = 0
        totalAnswers = 0
        answerAcceptedObj = questionObj.find("div",{"class":"status answered-accepted"})
        resultLinkObj = questionObj.find("div",{"class":"result-link"})
        voteCountObj = questionObj.find("span",{"class":"vote-count-post"})
        if resultLinkObj:
            question = sanitizeStr(resultLinkObj.text).strip()
            resultLink = resultLinkObj.find("a")
            if resultLink:
                resultLink = sanitizeStr(resultLink["href"])

        if voteCountObj:
            voteCount = int(voteCountObj.text)

        questionObj = Question(question=question, upvotes=voteCount, totalAnswers=totalAnswers,
                            resultLink=resultLink)
        questionList.append(questionObj)
        print ("-" * 20)
        print ("ID: %s" % questionObj.id)
        print ("Question: %s" % questionObj.text)
        print ("Upvotes: %s" % questionObj.upvotes)
        print ("-" * 20)

    if len(questionList) == 0:
        print ("Either no answers found or no answer was selected as accepted")
        sys.exit(1)

    openAnswer = int(input("Do u wish to open any answer?\n1.Yes\t2.No\n"))

    if (openAnswer==1):
        questionID = int(input("Enter the ID of question u want us to open in browser:\n"))
        browserLink = ""
        for question in questionList:
            if questionID == question.id:
                print ("Opening question with id %s in browser" % question.id)
                browserLink = STACKOVERFLOW_URL + question.resultLink
                webbrowser.open(browserLink)
                break
        if browserLink == "":
            print ("You entered an invalid question ID")
            sys.exit(1)
    else:
        print("Thank You")






