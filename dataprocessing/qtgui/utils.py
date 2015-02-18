import re

def makeSubStrForListViews(text):
    pos = text.find("\n")
    if pos != -1:
        t = text[0:pos]
    else:
        t = text[0:50]
    return t
