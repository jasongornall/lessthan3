from keen.client import KeenClient
import re
import json
from pprint import pprint
import sys
from urlparse import urlparse
from urlparse import parse_qsl

class formatter:
    @staticmethod
    def isRequestData(text=""):
        arrayElements=re.findall("(?<=\[).*?(?=\])",text)
        remainingElements=text.split
        if 'request' in arrayElements:
            return True
        else:
            pprint(arrayElements)
            return False
    @staticmethod
    def formatRequestData(text=""):
        #Application of data
        data=[{}]
        #pprint(text)
        ##get array elements
        arrayElements=re.findall("(?<=\[).*?(?=\])",text)
        
        text=re.sub("\[.+?\]", '', text)

        #get json elements

        temp=re.findall("\{.+?\}",text)
        text=re.sub("\{.+?\}", '', text)

        jsonElements=json.loads(temp[0])

        #get remaining elements
        remainingElements=text.split()
        if 'request' in arrayElements:
            #referrer parsing
    


             #basic Breaking
            userAgentRaw=arrayElements[1];

            userAgentParen=re.findall("(?<=\().*?(?=\))",userAgentRaw)
            userAgentRaw=re.sub("\(.+?\)", '', userAgentRaw)

            userAgentSplit=userAgentRaw.split()


            #engine
            split=userAgentSplit[1].split('/')
            engine_name=split[0]
            engine_version=split[1]

            pprint (arrayElements[1])
            pprint (userAgentSplit)

            #browser
            split=userAgentSplit[2].split('/')
            browser_name=split[0]
            browser_version=split[1]
            version_split=split[1].split('.')
            browser_major= version_split[0] if len(version_split)>0 else None
            browser_minor=version_split[1] if len(version_split)>1 else None
            browser_patch=version_split[2] if len(version_split)>2 else None


            #OS
            # grab first 4_4_4 or 2.2.2
            os_raw=userAgentParen[0]
            os_version=re.findall("[\d][\d\._]+[\d]",os_raw)[0]
            os_version=re.sub('_','.',os_version)
            version_split=os_version.split('.')
            os_major= version_split[0] if len(version_split)>0 else None
            os_minor= version_split[1] if len(version_split)>1 else None
            os_patch= version_split[2] if len(version_split)>2 else None
            os_minor_patch= version_split[3] if len(version_split)>3 else None

            os_raw=re.sub("[\d][\d\._]+[\d]","",os_raw)
            os_raw=re.sub("  "," ",os_raw)
            os_pieces=os_raw.split(';')
            os_name=os_pieces[1].strip()

            pprint (os_version)

            data = [{
            "status": jsonElements['status'],
            "latency": jsonElements['latency'],
            "protocol": jsonElements['protocol'],
            "url": remainingElements[1],
            "cache": jsonElements['cache'],
            "user_agent_string": arrayElements[1],
            "host": jsonElements['host'],
            "user_agent": {
                "device": {
                    "family": "Other"
                },
                "os": {
                    "major": os_major,
                    "patch_minor": os_minor_patch,
                    "minor": os_minor,
                    "family": os_name,
                    "patch": os_patch
                },
                "browser": {
                    "major": browser_major,
                    "minor": browser_minor,
                    "family": browser_name,
                    "patch": browser_patch
                }
            },
            "referrer": remainingElements[2],
            "path": jsonElements['path'],
            "ip_address": remainingElements[0],
            "method": jsonElements['method'],
            "size": jsonElements['size']
        }]
        return data
    @staticmethod
    def isPingData(text=""):
        arrayElements=re.findall("(?<=\[).*?(?=\])",text)
        remainingElements=text.split
        if 'ping' in arrayElements:
            return True
        else:
            return False
    @staticmethod
    def formatPingData(text=""):
        #Application of data
        data=[{}]
        #pprint(text)
        ##get array elements
        arrayElements=re.findall("(?<=\[).*?(?=\])",text)
        
        text=re.sub("\[.+?\]", '', text)

        #get json elements

        temp=re.findall("\{.+?\}",text)
        text=re.sub("\{.+?\}", '', text)

        jsonElements=json.loads(temp[0])

        #get remaining elements
        remainingElements=text.split()
        pprint(arrayElements)
        if 'ping' in arrayElements:
            #referrer parsing

            refStr=(remainingElements[4].split(','))
            refString=refStr[0]
            ref=urlparse(refString)
            refParams=dict(parse_qsl(ref.query))

            #url parsing
            urlString=(refParams['url'])
            url=urlparse(urlString)
            queryParams=parse_qsl(url.query)


            #user_agent parsing

            #basic Breaking
            userAgentRaw=arrayElements[1];

            userAgentParen=re.findall("(?<=\().*?(?=\))",userAgentRaw)
            userAgentRaw=re.sub("\(.+?\)", '', userAgentRaw)

            userAgentSplit=userAgentRaw.split()


            #engine
            split=userAgentSplit[1].split('/')
            engine_name=split[0]
            engine_version=split[1]

            #browser
            split=userAgentSplit[3].split('/')
            split_2=userAgentSplit[2].split('/')
            browser_name=split[0]
            browser_version=split_2[1]
            browser_major=re.findall("^\d+(?=\.)",split_2[1])
            #OS
            # grab first 4_4_4 or 2.2.2
            os_raw=userAgentParen[0]
            os_version=re.findall("[\d][\d\._]+[\d]",os_raw)[0]
            os_version=re.sub('_','.',os_version)
            os_raw=re.sub("[\d][\d\._]+[\d]","",os_raw)
            os_raw=re.sub("  "," ",os_raw)
            os_pieces=os_raw.split(';')
            os_name=os_pieces[1].strip()


            data = [{
            "url": {
                "domain": url.netloc,
                "protocol": url.scheme,
                "port": url.port,
                "source": urlString,
                "path": url.path,
                "anchor": ""
            },
            "referrer": {
                "domain": ref.netloc,
                "protocol": ref.scheme,
                "port": ref.port,
                "source": refString,
                "path": ref.path,
                "anchor": ""
            },
            "ip_address": arrayElements[0],
            "app": {
                "package_id": jsonElements['app_package_id'],
                "_id": jsonElements['app_id'],
                "package_version": jsonElements['app_package_version'],
                "slug": jsonElements['app_slug']
            },
            "site": {
                "_id": jsonElements['site_id'],
                "slug": jsonElements['site_slug']
            },
            "elapsed": jsonElements['elapsed'],
            "permanent_tracker": "??????????????",
            "engaged": 
            {
                "10": jsonElements['engaged_10'],
                "30": jsonElements['engaged_30'],
                "60": jsonElements['engaged_60']
            },
            "page": {
                "_id": jsonElements['page_id'],
                "type": jsonElements['page_type'],
                "slug": jsonElements['page_slug']
            },
            "user_agent": {
                "engine": {
                    "version": engine_version,
                    "name": engine_name
                },
                "os": {
                    "version": os_version,
                    "name": os_name
                },
                "browser": {
                    "major": browser_major[0],
                    "version": browser_version,
                    "name": browser_name
                }
            }
        	}]
        return data