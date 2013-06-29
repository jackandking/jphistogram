# -*- coding: utf8 -*-
import urllib
from google.appengine.api import urlfetch
from google.appengine.api import apiproxy_stub_map,urlfetch_stub 
import re

apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap() 
apiproxy_stub_map.apiproxy.RegisterStub('urlfetch', 
urlfetch_stub.URLFetchServiceStub()) 

url="http://weibo.cn/mblog/sendmblog?vt=4&gsid=4u2h340d1aVCaKYlTuCEReLCHc0&st=2c29"
form_fields = {
  "rl": 0,
  "content": "Hello World",
}
form_data = urllib.urlencode(form_fields)
result = urlfetch.fetch(url=url,
                        payload=form_data,
                        method=urlfetch.POST,
                        headers={'Content-Type': 'application/x-www-form-urlencoded'},
                        deadline=10)
if re.search("发布成功!",result.content):
    print u"发布成功!"
else:
    print result.content
print result.status_code
print result.headers
print result.final_url
