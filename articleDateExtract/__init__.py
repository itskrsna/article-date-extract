import re, json
from dateutil.parser import parse
import urllib.request as urllib
from bs4 import BeautifulSoup


def parseStrDate(dateString):
    try:
        dateTimeObj = parse(dateString)
        return dateTimeObj
    except:
        return None


# Try to extract from the article URL - simple but might work as a fallback
def _extractFromURL(url):

    # Regex by Newspaper3k  - https://github.com/codelucas/newspaper/blob/master/newspaper/urls.py
    m = re.search(
        r"([\./\-_]{0,1}(19|20)\d{2})[\./\-_]{0,1}(([0-3]{0,1}[0-9][\./\-_])|(\w{3,5}[\./\-_]))([0-3]{0,1}[0-9][\./\-]{0,1})?",
        url,
    )
    if m:
        return parseStrDate(m.group(0))

    return None


def recursivejson(d):
  tocheck = "datePublished"
  for k,v in d.items():
    if isinstance(v, dict):
        return recursivejson(v)
    elif isinstance(v, list):
            for i,z in enumerate(v):
                if tocheck in z:
                    return z[tocheck]        
    elif tocheck in k :
      return v
    elif tocheck in d:
      return d[tocheck]
  

def _extractFromLDJson(parsedHTML):
    jsonDate = None
    try:
        for script in parsedHTML.find_all("script", type="application/ld+json"):
            try:
                # print(script)
                if script is None:
                    return None

                data = json.loads(script.next)

                try:
                    if "datePublished" in script.next_element:
                      jsonDate = parseStrDate(recursivejson(json.loads(script.next_element)))
                except Exception as e:
                    pass

                try:
                    jsonDate = parseStrDate(data["dateCreated"])
                except Exception as e:
                    pass
            except Exception as e:
                pass

    except Exception as e:
        pass

    return jsonDate


def _extractFromMeta(parsedHTML):

    metaDate = None
    for meta in parsedHTML.findAll("meta"):
        metaName = meta.get("name", "").lower()
        itemProp = meta.get("itemprop", "").lower()
        httpEquiv = meta.get("http-equiv", "").lower()
        metaProperty = meta.get("property", "").lower()

        # <meta name="pubdate" content="2015-11-26T07:11:02Z" >
        if "pubdate" == metaName:
            metaDate = meta["content"].strip()
            break

        # <meta name='publishdate' content='201511261006'/>
        if "publishdate" == metaName:
            metaDate = meta["content"].strip()
            break

        # <meta name="timestamp"  data-type="date" content="2015-11-25 22:40:25" />
        if "timestamp" == metaName:
            metaDate = meta["content"].strip()
            break

        # <meta name="DC.date.issued" content="2015-11-26">
        if "dc.date.issued" == metaName:
            metaDate = meta["content"].strip()
            break

        # <meta property="article:published_time"  content="2015-11-25" />
        if "article:published_time" == metaProperty:
            metaDate = meta["content"].strip()
            break
            # <meta name="Date" content="2015-11-26" />
        if "date" == metaName:
            metaDate = meta["content"].strip()
            break

        # <meta property="bt:pubDate" content="2015-11-26T00:10:33+00:00">
        if "bt:pubdate" == metaProperty:
            metaDate = meta["content"].strip()
            break
            # <meta name="sailthru.date" content="2015-11-25T19:56:04+0000" />
        if "sailthru.date" == metaName:
            metaDate = meta["content"].strip()
            break

        # <meta name="article.published" content="2015-11-26T11:53:00.000Z" />
        if "article.published" == metaName:
            metaDate = meta["content"].strip()
            break

        # <meta name="published-date" content="2015-11-26T11:53:00.000Z" />
        if "published-date" == metaName:
            metaDate = meta["content"].strip()
            break

        # <meta name="article.created" content="2015-11-26T11:53:00.000Z" />
        if "article.created" == metaName:
            metaDate = meta["content"].strip()
            break

        # <meta name="article_date_original" content="Thursday, November 26, 2015,  6:42 AM" />
        if "article_date_original" == metaName:
            metaDate = meta["content"].strip()
            break

        # <meta name="cXenseParse:recs:publishtime" content="2015-11-26T14:42Z"/>
        if "cxenseparse:recs:publishtime" == metaName:
            metaDate = meta["content"].strip()
            break

        # <meta name="DATE_PUBLISHED" content="11/24/2015 01:05AM" />
        if "date_published" == metaName:
            metaDate = meta["content"].strip()
            break

        # <meta itemprop="datePublished" content="2015-11-26T11:53:00.000Z" />
        if "datepublished" == itemProp:
            metaDate = meta["content"].strip()
            break

        # <meta itemprop="datePublished" content="2015-11-26T11:53:00.000Z" />
        if "datecreated" == itemProp:
            metaDate = meta["content"].strip()
            break

        # <meta property="og:image" content="http://www.dailytimes.com.pk/digital_images/400/2015-11-26/norway-return-number-of-asylum-seekers-to-pakistan-1448538771-7363.jpg"/>
        if "og:image" == metaProperty or "image" == itemProp:
            url = meta["content"].strip()
            possibleDate = _extractFromURL(url)
            if possibleDate is not None:
                return possibleDate

        # <meta http-equiv="data" content="10:27:15 AM Thursday, November 26, 2015">
        if "date" == httpEquiv:
            metaDate = meta["content"].strip()
            break

    if metaDate is not None:
        return parseStrDate(metaDate)

    return None


def _extractFromHTMLTag(parsedHTML):
    classestolook = 'pubdate|timestamp|article_date|articledate|date|decided'
    # <time>
    for time in parsedHTML.findAll("time"):
        datetime = time.get("datetime", "")
        if len(datetime) > 0:
            return parseStrDate(datetime)

        datetime = time.get("class", "")
        if len(datetime) > 0 and datetime[0].lower() == "timestamp":
            return parseStrDate(time.string)

    tag = parsedHTML.find("span", {"itemprop": "datePublished"})
    if tag is not None:
        dateText = tag.get("content")
        if dateText is None:
            dateText = tag.text
        if dateText is not None:
            return parseStrDate(dateText)

    # class=
    for tag in parsedHTML.find_all(
        ["span", "p", "div"],
        class_=re.compile(
            classestolook, re.IGNORECASE
        ),
    ):
        dateText = tag.string
        if dateText is None:
            dateText = tag.text

        possibleDate = parseStrDate(dateText)

        if possibleDate is not None:
            return possibleDate

    return None


def extractArticlePublishedDate(articleLink, html=None):

    print("Extracting date from " + articleLink)

    articleDate = None

    try:
        articleDate = _extractFromURL(articleLink)
        if html is None:
            request = urllib.Request(articleLink)
            # Using a browser user agent, decreases the change of sites blocking this request - just a suggestion
            request.add_header(
                "User-Agent",
                "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
            )
            html = urllib.build_opener().open(request).read()

        parsedHTML = BeautifulSoup(html, "lxml")

        possibleDate = extractPossibleDate(parsedHTML)
        articleDate = possibleDate

    except Exception as e:
        print("Exception in extractArticlePublishedDate for " + articleLink)
        print(e.args)

    return articleDate


def extractPossibleDate(bsouparsedHTML):
    # bsouparsedHTML = BeautifulSoup(parsedHTML, 'html.parser')
    possibleDate = _extractFromLDJson(bsouparsedHTML)
    if possibleDate is None:
        possibleDate = _extractFromMeta(bsouparsedHTML)
    if possibleDate is None:
        possibleDate = _extractFromHTMLTag(bsouparsedHTML)
    return possibleDate



if __name__ == "__main__":
    d = extractArticlePublishedDate(
        "http://techcrunch.com/2015/11/29/tyro-payments/"
    )
    print(d)
