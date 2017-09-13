#this makes json files look nice in a terminal
#there are no features. fuck you
#i also didn't test it beyond what i used it for the day i wrote it.
#eat shit
#usage: python wowjson.py [url] [options]
#only option is -p for plain (no-color) mode
#oh and -f for full string length display. this is for idiots if you have bigass strings. 
#get bent

import requests
import json
import sys

BLU = '\033[96m'
GRN = '\033[92m'
YEL = '\033[93m'
END = '\033[0m'
BOLD = '\033[1m'

def getjson(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            try:
                return json.loads(r.text)
            except ValueError, e:
                bye("That shit isn't JSON.\n" + str(e))
            return json.loads(r.text)
        else:
            bye(str(r.status_code))
    except requests.ConnectionError, e:
        bye("The link is probably bad idiot.\n" + str(e))
    return None

def recur(jobj, level=0):
    currlevel = "    " * level
    if type(jobj) == dict:
        for i in jobj.keys():
            print BLU + currlevel + " " + i + ":" + END
            recur(jobj[i], level+1)
    elif type(jobj) == int:
        print GRN + currlevel + " " + str(jobj) + END
    elif type(jobj) == unicode or type(jobj) == str:
        if trunc:
            print currlevel + " " + jobj
        else:
            printthis = jobj.strip().replace('\n','').replace('\t','')
            while "  " in printthis:
                printthis = printthis.replace('  ',' ')
            if len(printthis) > 200:
                printthis = printthis[:199].strip() + BOLD + "..." + END
            print currlevel + " " + printthis
    elif type(jobj) == list:
        for i in jobj:
            recur(i, level+1)
    elif type(jobj) == bool:
        print YEL + currlevel + " " + str(jobj) + END

def bye(err=None):
    if err:
        print "Nice try idiot. Check this out:", str(err)
    else:
        print "\nUsage: python nicejson.py [url] [options]"
        print "\nOptions:\n\t-p\tPlain mode. No colors. Fuck you."
        print "\t-f\tFull file. Do not truncate strings at 200 chars."
        print "\ni'm not a genious so don't be a smartass\n"
    sys.exit(1)

if len(sys.argv) < 2:
    bye()

trunc = True
for i in sys.argv:
    if "://" in i:
        url = i
    if i == "-p":
        BLU = GRN = YEL = END = BOLD = ''
    if i == "-f":
        trunc = False #you're fuckin off yoru shit for this
recur(getjson(sys.argv[1]))
