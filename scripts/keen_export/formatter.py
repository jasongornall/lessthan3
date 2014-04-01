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
        array_elements=re.findall("(?<=\[).*?(?=\])",text)
        remaining_elements=text.split
        if 'request' in array_elements:
            return True
        else:
            pprint(array_elements)
            return False
    @staticmethod
    def formatRequestData(text=""):
        #Application of data
        data=[{}]
        #pprint(text)
        ##get array elements
        array_elements=re.findall("(?<=\[).*?(?=\])",text)
        
        text=re.sub("\[.+?\]", '', text)

        #get json elements

        temp=re.findall("\{.+?\}",text)
        text=re.sub("\{.+?\}", '', text)

        json_elements=json.loads(temp[0])

        #get remaining elements
        remaining_elements=text.split()
        if 'request' in array_elements:
            #referrer parsing
    

            # basic Breaking
            user_agent_raw=array_elements[1];

            user_agent_paren=re.findall("(?<=\().*?(?=\))",user_agent_raw)
            user_agent_raw=re.sub("\(.+?\)", '', user_agent_raw)

            user_agent_split=user_agent_raw.split()


            #engine
            split=user_agent_split[1].split('/')
            engine_name=split[0]
            engine_version=split[1]

            pprint (array_elements[1])
            pprint (user_agent_split)

            #browser
            split=user_agent_split[2].split('/')
            browser_name=split[0]
            browser_version=split[1]
            version_split=split[1].split('.')
            browser_major= version_split[0] if len(version_split)>0 else None
            browser_minor=version_split[1] if len(version_split)>1 else None
            browser_patch=version_split[2] if len(version_split)>2 else None


            #OS
            # grab first 4_4_4 or 2.2.2
            os_raw=user_agent_paren[0]
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
            "status": json_elements['status'],
            "latency": json_elements['latency'],
            "protocol": json_elements['protocol'],
            "url": remaining_elements[1],
            "cache": json_elements['cache'],
            "user_agent_string": array_elements[1],
            "host": json_elements['host'],
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
            "referrer": remaining_elements[2],
            "path": json_elements['path'],
            "ip_address": remaining_elements[0],
            "method": json_elements['method'],
            "size": json_elements['size']
        }]
        return data

    @staticmethod
    def isPingData(text=""):
        array_elements=re.findall("(?<=\[).*?(?=\])",text)
        remaining_elements=text.split
        if 'ping' in array_elements:
            return True
        else:
            return False
    @staticmethod
    def formatPingData(text=""):
        #Application of data
        data=[{}]
        #pprint(text)
        ##get array elements
        array_elements=re.findall("(?<=\[).*?(?=\])",text)
        
        text=re.sub("\[.+?\]", '', text)

        #get json elements

        temp=re.findall("\{.+?\}",text)
        text=re.sub("\{.+?\}", '', text)

        json_elements=json.loads(temp[0])

        #get remaining elements
        remaining_elements=text.split()
        pprint(array_elements)
        if 'ping' in array_elements:
            #referrer parsing

            ref_str=(remaining_elements[4].split(','))
            ref_string=ref_str[0]
            ref=urlparse(ref_string)
            refParams=dict(parse_qsl(ref.query))

            #url parsing
            url_string=(refParams['url'])
            url=urlparse(url_string)
            queryParams=parse_qsl(url.query)


            #user_agent parsing

            #basic Breaking
            user_agent_raw=array_elements[1];

            user_agent_paren=re.findall("(?<=\().*?(?=\))",user_agent_raw)
            user_agent_raw=re.sub("\(.+?\)", '', user_agent_raw)

            user_agent_split=user_agent_raw.split()


            #engine
            split=user_agent_split[1].split('/')
            engine_name=split[0]
            engine_version=split[1]

            #browser
            split=user_agent_split[3].split('/')
            split_2=user_agent_split[2].split('/')
            browser_name=split[0]
            browser_version=split_2[1]
            browser_major=re.findall("^\d+(?=\.)",split_2[1])
            #OS
            # grab first 4_4_4 or 2.2.2
            os_raw=user_agent_paren[0]
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
                "source": url_string,
                "path": url.path,
                "anchor": ""
            },
            "referrer": {
                "domain": ref.netloc,
                "protocol": ref.scheme,
                "port": ref.port,
                "source": ref_string,
                "path": ref.path,
                "anchor": ""
            },
            "ip_address": array_elements[0],
            "app": {
                "package_id": json_elements['app_package_id'],
                "_id": json_elements['app_id'],
                "package_version": json_elements['app_package_version'],
                "slug": json_elements['app_slug']
            },
            "site": {
                "_id": json_elements['site_id'],
                "slug": json_elements['site_slug']
            },
            "elapsed": json_elements['elapsed'],
            "permanent_tracker": "??????????????",
            "engaged": 
            {
                "10": json_elements['engaged_10'],
                "30": json_elements['engaged_30'],
                "60": json_elements['engaged_60']
            },
            "page": {
                "_id": json_elements['page_id'],
                "type": json_elements['page_type'],
                "slug": json_elements['page_slug']
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
    @staticmethod
    def isPingData(text=""):
        array_elements=re.findall("(?<=\[).*?(?=\])",text)
        remaining_elements=text.split
        if 'ping' in array_elements:
            return True
        else:
            return False
    @staticmethod
    def formatPingData(text=""):
        #Application of data
        data=[{}]
        #pprint(text)
        ##get array elements
        array_elements=re.findall("(?<=\[).*?(?=\])",text)
        
        text=re.sub("\[.+?\]", '', text)

        #get json elements

        temp=re.findall("\{.+?\}",text)
        text=re.sub("\{.+?\}", '', text)

        json_elements=json.loads(temp[0])

        #get remaining elements
        remaining_elements=text.split()
        pprint(array_elements)
        if 'ping' in array_elements:
            #referrer parsing

            ref_str=(remaining_elements[4].split(','))
            ref_string=ref_str[0]
            ref=urlparse(ref_string)
            refParams=dict(parse_qsl(ref.query))

            #url parsing
            url_string=(refParams['url'])
            url=urlparse(url_string)
            queryParams=parse_qsl(url.query)


            #user_agent parsing

            #basic Breaking
            user_agent_raw=array_elements[1];

            user_agent_paren=re.findall("(?<=\().*?(?=\))",user_agent_raw)
            user_agent_raw=re.sub("\(.+?\)", '', user_agent_raw)

            user_agent_split=user_agent_raw.split()


            #engine
            split=user_agent_split[1].split('/')
            engine_name=split[0]
            engine_version=split[1]

            #browser
            split=user_agent_split[3].split('/')
            split_2=user_agent_split[2].split('/')
            browser_name=split[0]
            browser_version=split_2[1]
            browser_major=re.findall("^\d+(?=\.)",split_2[1])
            #OS
            # grab first 4_4_4 or 2.2.2
            os_raw=user_agent_paren[0]
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
                "source": url_string,
                "path": url.path,
                "anchor": ""
            },
            "referrer": {
                "domain": ref.netloc,
                "protocol": ref.scheme,
                "port": ref.port,
                "source": ref_string,
                "path": ref.path,
                "anchor": ""
            },
            "ip_address": array_elements[0],
            "app": {
                "package_id": json_elements['app_package_id'],
                "_id": json_elements['app_id'],
                "package_version": json_elements['app_package_version'],
                "slug": json_elements['app_slug']
            },
            "site": {
                "_id": json_elements['site_id'],
                "slug": json_elements['site_slug']
            },
            "elapsed": json_elements['elapsed'],
            "permanent_tracker": "??????????????",
            "engaged": 
            {
                "10": json_elements['engaged_10'],
                "30": json_elements['engaged_30'],
                "60": json_elements['engaged_60']
            },
            "page": {
                "_id": json_elements['page_id'],
                "type": json_elements['page_type'],
                "slug": json_elements['page_slug']
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