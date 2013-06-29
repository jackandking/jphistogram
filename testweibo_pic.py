# -*- coding: utf8 -*-



##import MultipartPostHandler, urllib2, cookielib
##
##url="http://weibo.cn/mblog/sendmblog?vt=4&gsid=4u2h340d1aVCaKYlTuCEReLCHc0&st=2c29"
##form_fields = {
##  "content": "Hello World",
##  "pic": open('D:\chrome_download\ywhs.jpg','rb'),
##  "visible": "0",
##}
##
##cookies = cookielib.CookieJar()
##opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies),
##                                MultipartPostHandler.MultipartPostHandler)
####params = { "username" : "bob", "password" : "riviera",
####             "file" : open("filename", "rb") }
##r=opener.open(url, form_fields)
##print r.read()
##
##quit()
##
##import urllib
##from google.appengine.api import urlfetch
##from google.appengine.api import apiproxy_stub_map,urlfetch_stub 
##
##
##print open('D:\chrome_download\ywhs.jpg','rb')
##print form_fields
##form_data = urllib.urlencode(form_fields)
##print form_data
##quit(0)

##from google.appengine.ext import db
from google.appengine.api import urlfetch
from poster.encode import multipart_encode, MultipartParam
import re
from google.appengine.api import apiproxy_stub_map,urlfetch_stub

apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap() 
apiproxy_stub_map.apiproxy.RegisterStub('urlfetch', 
urlfetch_stub.URLFetchServiceStub()) 

url="http://weibo.cn/mblog/sendmblog?vt=4&gsid=4u2h340d1aVCaKYlTuCEReLCHc0&st=2c29"
form_fields = {
##  MultipartParam("content",value= "Hello World"),
##  MultipartParam("pic",filename='ywhs.jpg',value= open('D:\chrome_download\ywhs.jpg','rb')),
##  MultipartParam("visible",value= "0"),
  "content":"Hello World",
  "pic" : open('D:\chrome_download\ywhs.jpg','rb'),
}
payloadgen, headers = multipart_encode(form_fields)
print headers
print payloadgen
# urlfetch cannot use a generator an argument for payload so
# build the payload as a string.
payload = str().join(payloadgen)
print payload
result = urlfetch.fetch(url=url,
                        payload=payload,
                        method=urlfetch.POST,
                        headers=headers,
                        deadline=10)
if re.search("发布成功!",result.content):
    print u"发布成功!"
else:
    print result.content
print result.status_code
print result.headers
print result.final_url
