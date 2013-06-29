#!/usr/bin/python
import logging, os, StringIO, cgi
try: import webapp2
except: pass  # when ran directly from command line
import subprocess
def no_popen(*args, **kwargs): raise OSError("forbjudet")
subprocess.Popen = no_popen  # not allowed in GAE, missing from module
subprocess.PIPE = None
subprocess.STDOUT = None
#os.environ["MATPLOTLIBDATA"] = os.getcwdu()  # own matplotlib data
#os.environ["MPLCONFIGDIR"] = os.getcwdu()    # own matplotlibrc
import numpy, matplotlib, matplotlib.pyplot as plt
import re
from weibo import send_weibo

def dynamic_png():
    try:
        plt.title("Dynamic PNG")
        for i in range(5): plt.plot(sorted(numpy.random.randn(25)))
        rv = StringIO.StringIO()
        plt.savefig(rv, format="png")
        plt.clf()
        return """<img src="data:image/png;base64,%s"/>""" % rv.getvalue().encode("base64").strip()
    finally:
        plt.clf()
        
from google.appengine.api import urlfetch

def get_histogram_pic(id):
    url="http://jpauto.sinaapp.com/data"
    result = urlfetch.fetch(url=url,deadline=10)
    if result.status_code == 200:
        array=get_count_array(id,result.content)
        try:
            plt.title("histogram_"+str(id))
            plt.plot(array)
            rv = StringIO.StringIO()
            plt.savefig(rv, format="png")
            plt.clf()
            setattr(rv,'name','histogram.png')
            return rv
        finally:
            plt.clf()
    return None

def histogram(id):
    url="http://jpauto.sinaapp.com/data"
    result = urlfetch.fetch(url)
    if result.status_code == 200:
        array=get_count_array(id,result.content)
        try:
            plt.title("histogram_"+str(id))
            plt.plot(array)
            rv = StringIO.StringIO()
            plt.savefig(rv, format="png")
            plt.clf()
            return """<img src="data:image/png;base64,%s"/>""" % rv.getvalue().encode("base64").strip()
        finally:
            plt.clf()

def get_count_array(id,content):
    lines=content.split("<br/>")
    array=[]
    for line in lines:
        m = re.search("\(\('\d+', '(\d+)', '4', '(\d+)', '.*'\),\)",line)
        if m:
            if id == int(m.group(1)):
                array.append(m.group(2))
##            else:
##                logging.debug("ignore id: "+line)
##        else:
##            logging.debug("ignore line:"+line)
    print array
    return array

def dynamic_svg():
    try:
        plt.title("Dynamic SVG")
        for i in range(5): plt.plot(sorted(numpy.random.randn(25)))
        rv = StringIO.StringIO()
        plt.savefig(rv, format="svg")
        return rv.getvalue().partition("-->")[-1]
    finally:
        plt.clf()

try: dynamic_png()  # crashes first time because it can't cache fonts
except: logging.exception("don't about it")

class WeiboHandler(webapp2.RequestHandler):
    def get(self):
        pic_data=get_histogram_pic(6)
        if send_weibo("Hello World",pic_data):
            self.response.write("""<img src="data:image/png;base64,%s"/>""" % pic_data.getvalue().encode("base64").strip())
        else:
            self.response.write('ko')

class DailyHandler(webapp2.RequestHandler):
    def get(self):
        pic_data=get_histogram_pic(6)
        if send_weibo("Daily Report",pic_data):
            self.response.write('ok')
            logging.info("Daily Report ok")
        else:
            self.response.write('ko')
            logging.error("Daily Report ko")
            
if __name__ != "__main__":
    class MainHandler(webapp2.RequestHandler):
        def get(self):
            self.response.write("""<html><head><title>Histogram</title></head><body>""")
            #self.response.write(dynamic_png())
            for i in range(6,11):
                self.response.write(histogram(i))
            #self.response.write("<pre>%s</pre>" % cgi.escape(file(__file__.rstrip("c")).read()))  # source, dev runs .py, gae runs .pyc
            self.response.write("""</body> </html>""")

    app = webapp2.WSGIApplication([
        ('/', MainHandler),
        ('/weibo', WeiboHandler),
        ('/cron/daily', DailyHandler),
    ], debug=True)
