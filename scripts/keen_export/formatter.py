from keen.client import KeenClient
import re
import json
from pprint import pprint
import sys
from urlparse import urlparse
from urlparse import parse_qsl
import httpagentparser

class formatter:
    @staticmethod
    # specific stuff done to the augmented string unique to us
    def augmentAgentString(agentString,raw):

        if ('os' in agentString):
            if ('flavor' in agentString):
                agentString['os']=agentString['flavor']
                if ('X' in agentString['os']['version']):
                    agentString['os']['version']=agentString['os']['version'].replace('X',"")
                    agentString['os']['name']+=' X'

            #hack cause they don't grab iphone version too well grab ios
            #looks for 34234_43343_343
            if (not 'version' in agentString['os'] or agentString['os']['version']==""):
                arr=re.findall('\d+_[\d|\_]+(?=\s|\))',raw)
                if (len(arr)>0):
                    agentString['os']['version']=arr[0]

            #hack for looking in the dist.. sometimes that is what we want
            if (not 'version' in agentString['os'] or agentString['os']['version']==""):
                if ('dist' in agentString):
                    agentString['os']=agentString['dist']

            #some OS's have a characters in their version... look for those Linux x86.64 is a example
            if (not 'version' in agentString['os'] and 'name' in agentString['os']):
                arr=re.findall("(?<="+agentString['os']['name']+")[^;]*",raw)
                if (len(arr)==1):
                    agentString['os']['version']=arr[0].strip()
        if ('os' in agentString and 'name' in agentString['os']):
            agentString['os']['version']=agentString['os']['version'].strip()
        return agentString


    @staticmethod
    def isRequestData(text=""):
        array_elements=re.findall("(?<=\[).*?(?=\])",text)
        remaining_elements=text.split
        if 'request' in array_elements:
            return True
        else:
            return False
    @staticmethod
    def formatRequestData(text=""):
        #Application of data
        data=[{}]
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



            data = [{
            "status": json_elements['status'],
            "latency": json_elements['latency'],
            "protocol": json_elements['protocol'],
            "url": remaining_elements[1],
            "cache": json_elements['cache'],
            "user_agent_string": array_elements[1],
            "path": json_elements['path'],
            "ip_address": remaining_elements[0],
            "method": json_elements['method'],
            "size": json_elements['size']
            }]

            agentString=httpagentparser.detect(array_elements[1])

            # browser processing
            browser_major=""
            browser_minor=""
            browser_patch=""
            browser_name=""
            if ('browser' in agentString):
                browser_name=agentString['browser']['name']
                if ('version' in agentString['browser']):
                    agentString['browser']['version'].replace('_','.')
                    split=agentString['browser']['version'].split('.')
                    if (split):
                        browser_major=split[0] if len(split)>0 else ""
                        browser_minor=split[1] if len(split)>1 else ""
                        browser_patch=split[2] if len(split)>2 else ""

            
            # os processing
            os_major=""
            os_minor=""
            os_patch=""
            os_name=""
            os_minor_patch=""
            split=[]
            pprint(agentString)
            agentString=formatter.augmentAgentString(agentString,array_elements[1])
            if ('os' in agentString):
                #make all of them period based
                if ('version' in agentString['os']):
                    agentString['os']['version']=agentString['os']['version'].replace('_','.')
                    split=agentString['os']['version'].split('.')

                    if (split):
                        os_major=split[0] if len(split)>0 else ""
                        os_minor=split[1] if len(split)>1 else ""
                        os_patch=split[2] if len(split)>2 else ""
                        os_minor_patch=split[3] if len(split)>3 else ""
                os_name=agentString['os']['name']



            # device processing
            device_family="Other"
            if ('dist' in agentString and 'name' in agentString['dist']):
                device_family=agentString['dist']['name']



            data[0]["user_agent"] =  {
                "data":agentString,
                "device": {
                    "family":device_family
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
            }


        
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
        ##get array elements
        array_elements=re.findall("(?<=\[).*?(?=\])",text)
        
        text=re.sub("\[.+?\]", '', text)

        #get json elements

        temp=re.findall("\{.+?\}",text)
        text=re.sub("\{.+?\}", '', text)

        json_elements=json.loads(temp[0])

        #get remaining elements
        remaining_elements=text.split()
        if "ping" in array_elements:            
            #url parsing
            url_string=(remaining_elements[1])
            url=urlparse(url_string)
            queryParams=parse_qsl(url.query)

            #basic Breaking
            user_agent_raw=array_elements[1];
            user_agent_paren=re.findall("(?<=\().*?(?=\))",user_agent_raw)
            user_agent_raw=re.sub("\(.+?\)", '', user_agent_raw)
            user_agent_split=user_agent_raw.split()
            agentString=httpagentparser.detect(array_elements[1])
            
            engagedData={}
            if ('engaged_10' in json_elements):
                engagedData['10'] = json_elements['engaged_10']
            if ('engaged_30' in json_elements):
                engagedData['30'] = json_elements['engaged_30']
            if ('engaged_60' in json_elements):
                engagedData['60'] = json_elements['engaged_60']
            if ('engaged_300' in json_elements):
                engagedData['300'] = json_elements['engaged_300']
            if ('engaged_600' in json_elements):
                engagedData['600'] = json_elements['engaged_600']

            data = [{
            "data": agentString,
            "data_raw": array_elements[1],
            "url": {
                "domain": url.netloc,
                "protocol": url.scheme,
                "port": url.port,
                "source": url_string,
                "path": url.path,
                "anchor": ""
            },
            "ip_address": remaining_elements[0],
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
            "engaged": engagedData,
            "page": {
                "_id": json_elements['page_id'],
                "type": json_elements['page_type'],
                "slug": json_elements['page_slug']
            },
        	}]
            #engine
            if (len(user_agent_split)>1 and '/' in user_agent_split[1]):
                split=user_agent_split[1].split('/')
                engine_name=split[0]
                engine_version=split[1]
            elif ('/' in user_agent_split[0]):
                split=user_agent_split[0].split('/')
                engine_name=split[0]
                engine_version=split[1]

            # browser processing
            browser_major=""
            browser_name=""
            browser_version=""
            if ('browser' in agentString):
                browser_name=agentString['browser']['name']
                if ('version' in agentString['browser']):
                    agentString['browser']['version']=agentString['browser']['version'].replace('_','.')
                    split=agentString['browser']['version'].split('.')
                    browser_version=agentString['browser']['version']
                    if (split):
                        browser_major=split[0] if len(split)>0 else ""

            
            # os processing
            os_name=""
            os_version=""
            pprint(agentString)
            agentString=formatter.augmentAgentString(agentString,array_elements[1])
            if ('os' in agentString):
                #make all of them period based
                if ('version' in agentString['os']):
                    agentString['os']['version']=agentString['os']['version'].replace('_','.')
                    os_version=agentString['os']['version']                   
                   
                os_name=agentString['os']['name']


            data[0]["user_agent"] =  {
                "engine": {
                    "version": engine_version,
                    "name": engine_name
                },
                "os": {
                    "version": os_version,
                    "name": os_name
                },
                "browser": {
                    "major": browser_major,
                    "version": browser_version,
                    "name": browser_name
                }
            }

            #we don't always have a referrer
            if (len(remaining_elements)>4):
                ref_str=(remaining_elements[4].split(','))
                ref_string=ref_str[0]
                ref=urlparse(ref_string)
                refParams=dict(parse_qsl(ref.query))
                data[0]["referrer"]= {
                    "domain": ref.netloc,
                    "protocol": ref.scheme,
                    "port": ref.port,
                    "source": ref_string,
                    "path": ref.path,
                    "anchor": ""
                }
                



        return data
    @staticmethod
    def isPageViewData(text=""):
        array_elements=re.findall("(?<=\[).*?(?=\])",text)
        remaining_elements=text.split
        if 'pageview' in array_elements:
            return True
        else:
            return False
    @staticmethod
    def formatPageViewData(text=""):
        #Application of data
        data=[{}]

        ##get array elements
        array_elements=re.findall("(?<=\[).*?(?=\])",text)
        
        text=re.sub("\[.+?\]", '', text)

        #get json elements
        temp=re.findall("\{.+?\}",text)
        text=re.sub("\{.+?\}", '', text)

        json_elements=json.loads(temp[0])

        #get remaining elements
        remaining_elements=text.split()
        if "pageview" in array_elements:            
            #url parsing
            url_string=(remaining_elements[1])
            url=urlparse(url_string)
            queryParams=parse_qsl(url.query)

            #basic Breaking
            user_agent_raw=array_elements[1];
            user_agent_paren=re.findall("(?<=\().*?(?=\))",user_agent_raw)
            user_agent_raw=re.sub("\(.+?\)", '', user_agent_raw)
            user_agent_split=user_agent_raw.split()
            agentString=httpagentparser.detect(array_elements[1])


            data = [{
            "url": {
                "domain": url.netloc,
                "protocol": url.scheme,
                "port": url.port,
                "source": url_string,
                "path": url.path,
                "anchor": ""
            },
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
            "permanent_tracker": "??????????????",
            "page": {
                "_id": json_elements['page_id'],
                "type": json_elements['page_type'],
                "slug": json_elements['page_slug']
            }
            }]
            #engine
            if (len(user_agent_split)>1 and '/' in user_agent_split[1]):
                split=user_agent_split[1].split('/')
                engine_name=split[0]
                engine_version=split[1]
            elif ('/' in user_agent_split[0]):
                split=user_agent_split[0].split('/')
                engine_name=split[0]
                engine_version=split[1]

            # browser processing
            browser_major=""
            browser_name=""
            browser_version=""
            if ('browser' in agentString):
                browser_name=agentString['browser']['name']
                if ('version' in agentString['browser']):
                    agentString['browser']['version']=agentString['browser']['version'].replace('_','.')
                    split=agentString['browser']['version'].split('.')
                    browser_version=agentString['browser']['version']
                    if (split):
                        browser_major=split[0] if len(split)>0 else ""

            
            # os processing
            os_name=""
            os_version=""
            pprint(agentString)
            agentString=formatter.augmentAgentString(agentString,array_elements[1])
            if ('os' in agentString):
                #make all of them period based
                if ('version' in agentString['os']):
                    agentString['os']['version']=agentString['os']['version'].replace('_','.')
                    os_version=agentString['os']['version']                   
                   
                os_name=agentString['os']['name']


            data[0]["user_agent"] =  {
                "engine": {
                    "version": engine_version,
                    "name": engine_name
                },
                "os": {
                    "version": os_version,
                    "name": os_name
                },
                "browser": {
                    "major": browser_major,
                    "version": browser_version,
                    "name": browser_name
                }
            }

            #we don't always have a referrer
            if (len(remaining_elements)>4):
                ref_str=(remaining_elements[4].split(','))
                ref_string=ref_str[0]
                ref=urlparse(ref_string)
                refParams=dict(parse_qsl(ref.query))
                data[0]["referrer"]= {
                    "domain": ref.netloc,
                    "protocol": ref.scheme,
                    "port": ref.port,
                    "source": ref_string,
                    "path": ref.path,
                    "anchor": ""
                }
                



        return data