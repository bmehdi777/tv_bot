import urllib.request
import json
import xmltodict
import datetime


def get_guide():
    time = datetime.datetime.now()
    if (time.day < 10):   
        url_channel = "https://webnext.fr/epg_cache/programme-tv-rss_0"+str(time.day)+"-"+str(time.month)+"-"+str(time.year)+".xml"
    else:
        url_channel = "https://webnext.fr/epg_cache/programme-tv-rss_"+str(time.day)+"-"+str(time.month)+"-"+str(time.year)+".xml"

    x  = urllib.request.urlopen(url_channel).read()
    print(url_channel)
    o = xmltodict.parse(x)

    return o

    """for i in o["rss"]["channel"]["item"]:
        if ("TF1" in i["title"]):
            print(i["title"].split("|"))"""

if __name__ == "__main__":
    print(get_guide())