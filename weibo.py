# -*- coding: utf8 -*-
from google.appengine.api import urlfetch
from poster.encode import multipart_encode
import re
import logging
import urllib

def send_weibo_by_gsid(content,pic_data):
    #gsid for crowdfund_research
    url="http://weibo.cn/mblog/sendmblog?vt=4&gsid=4u2h340d1aVCaKYlTuCEReLCHc0&st=2c29"
    form_fields = {
      "content":content,
      "pic" : pic_data,
    }
    payloadgen, headers = multipart_encode(form_fields)
    # urlfetch cannot use a generator an argument for payload so
    # build the payload as a string.
    payload = str().join(payloadgen)
    result = urlfetch.fetch(url=url,
                            payload=payload,
                            method=urlfetch.POST,
                            headers=headers,
                            deadline=10)
    if result.status_code == 200 and re.search("发布成功!",result.content):
        logging.debug(u"发布成功!")
        return True
    else:
        logging.debug(result.content)
        urlfetch.fetch(url='http://jpauto.sinaapp.com/mail/to:jackandking@gmail.com||title:send_weibo failed!||body:'+str(result.status_code),
                       deadline=10)
        return False

def send_weibo(content,pic_data):
    url="http://jpauto.sinaapp.com/weibo"
##    url="http://localhost:8080/weibo"
    form_fields = {
      "content":content,
      "pic" : pic_data,
    }
##    print form_fields
    payloadgen, headers = multipart_encode(form_fields)
##    print headers
##    print payloadgen
    # urlfetch cannot use a generator an argument for payload so
    # build the payload as a string.
    payload = str().join(payloadgen)
    result = urlfetch.fetch(url=url,
                            payload=payload,
                            method=urlfetch.POST,
                            headers=headers,
                            deadline=10)
    if result.status_code == 200 and "ok" == result.content:
        logging.debug("send weibo ok")
        return True
    else:
        logging.debug(result.content)
##        urlfetch.fetch(url='http://jpauto.sinaapp.com/mail/to:jackandking@gmail.com||title:send_weibo failed!||body:'+str(result.status_code),
##                       deadline=10)
        return False
   
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    from google.appengine.api import apiproxy_stub_map,urlfetch_stub

    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap() 
    apiproxy_stub_map.apiproxy.RegisterStub('urlfetch', urlfetch_stub.URLFetchServiceStub())

    from StringIO import StringIO
    rv=StringIO(open('ywhs.png','rb').read())
    setattr(rv,'name','ywhs.png')
    if send_weibo("Hello StringIO", rv):
        print "ok"
    else:
        print "ko"
##    quit(1)
    if send_weibo("Hello", open('ywhs.png','rb')):
        print "ok"
    else:
        print "ko"
