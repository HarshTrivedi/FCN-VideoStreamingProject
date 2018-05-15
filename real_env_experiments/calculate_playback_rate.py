import json
from urlparse import urlparse
import dateutil.parser

har_input = open('video.har')
har_json = json.loads(har_input.read())
output_json = {}
count=0
for entry in har_json['log']['entries']:
    url = entry['request']['url']
    #print url
    if 'video' and 'segment' in url:
        output_json[count]={}
        output_json[count]['time']=entry['startedDateTime']
        url = entry['request']['url'].split("/")[-3]
        output_json[count]['request']=url
        output_json[count]['responseSize']=entry['response']['bodySize']
        count=count+1

bitrates = open('bitrates')
rate_dict={}
for line in bitrates:
    element = line.split()
    request_url = element[0].split('-')[-1]
    bitrate = element[5].rstrip('k,')
    rate_dict[request_url] = bitrates

bitrates.close()

har_data = output_json
#print  har_data
flag=0

for value in har_data.itervalues():

    time_har = value['time']
    request = value['request']
   
    print time_har,request
    if(flag==0):
        start_time = dateutil.parser.parse(time_har)
        flag=1

    #print key,value

    time = dateutil.parser.parse(time_har)
    size = rate_dict[request]
    print ("%s %s %s") % ((time-start_time), ",", size)
