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
        
#from google.appengine.api import urlfetch

def histogram():
    url="http://jpauto.sinaapp.com/data"
    result = urlfetch.fetch(url)
    if result.status_code == 200:
        array=get_count_array(6,result.content)
        try:
            plt.title("histogram")
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
        #print line
        m = re.search("\(\('\d+', '(\d+)', '4', '(\d+)', '.*'\),\)",line)
        if m:
            if id == int(m.group(1)):
                array.append(m.group(2))
            else:
                logging.debug("ignore id: "+line)
        else:
            logging.debug("ignore line:"+line)
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

if __name__ != "__main__":
    class MainHandler(webapp2.RequestHandler):
        def get(self):
            self.response.write("""<html><head><title>Histogram</title></head><body>""")
            #self.response.write(dynamic_png())
            self.response.write(histogram())
            #self.response.write("<pre>%s</pre>" % cgi.escape(file(__file__.rstrip("c")).read()))  # source, dev runs .py, gae runs .pyc
            self.response.write("""</body> </html>""")

    app = webapp2.WSGIApplication([
        ('/', MainHandler)
    ], debug=True)
else:
    
    content='''<br/> (('1', '6', '4', '999000', '2013-06-12 16:24:52'),) <br/> (('2', '7', '4', '948000', '2013-06-12 16:24:52'),) <br/> (('3', '8', '4', '2', '2013-06-12 16:24:52'),) <br/> (('4', '9', '4', '16', '2013-06-12 16:24:53'),) <br/> (('5', '10', '4', '317000', '2013-06-12 16:24:53'),) <br/> (('6', '6', '4', '999000', '2013-06-12 20:00:57'),) <br/> (('7', '7', '4', '947000', '2013-06-12 20:00:57'),) <br/> (('8', '8', '4', '2', '2013-06-12 20:00:58'),) <br/> (('9', '9', '4', '16', '2013-06-12 20:00:58'),) <br/> (('10', '10', '4', '317000', '2013-06-12 20:00:58'),) <br/> (('11', '6', '4', '957000', '2013-06-16 20:00:56'),) <br/> (('12', '7', '4', '924000', '2013-06-16 20:01:00'),) <br/> (('13', '8', '4', '2', '2013-06-16 20:01:00'),) <br/> (('14', '9', '4', '17', '2013-06-16 20:01:00'),) <br/> (('15', '10', '4', '313000', '2013-06-16 20:01:01'),) <br/> (('16', '6', '4', '957000', '2013-06-17 20:00:57'),) <br/> (('17', '7', '4', '925000', '2013-06-17 20:00:58'),) <br/> (('18', '8', '4', '2', '2013-06-17 20:00:58'),) <br/> (('19', '9', '4', '19', '2013-06-17 20:00:59'),) <br/> (('20', '10', '4', '313000', '2013-06-17 20:00:59'),) <br/> (('21', '6', '4', '957000', '2013-06-18 20:01:03'),) <br/> (('22', '7', '4', '926000', '2013-06-18 20:01:06'),) <br/> (('23', '6', '4', '957000', '2013-06-19 20:00:58'),) <br/> (('24', '7', '4', '927000', '2013-06-19 20:00:59'),) <br/> (('25', '8', '4', '2', '2013-06-19 20:01:00'),) <br/> (('26', '9', '4', '20', '2013-06-19 20:01:00'),) <br/> (('27', '10', '4', '312000', '2013-06-19 20:01:00'),) <br/> (('28', '6', '4', '959000', '2013-06-20 20:00:57'),) <br/> (('29', '7', '4', '1110000', '2013-06-20 20:00:57'),) <br/> (('30', '8', '4', '7', '2013-06-20 20:00:58'),) <br/> (('31', '9', '4', '356', '2013-06-20 20:00:58'),) <br/> (('32', '10', '4', '315000', '2013-06-20 20:00:58'),) <br/> (('33', '6', '4', '960000', '2013-06-21 20:00:57'),) <br/> (('34', '7', '4', '1110000', '2013-06-21 20:00:58'),) <br/> (('35', '8', '4', '7', '2013-06-21 20:00:58'),) <br/> (('36', '9', '4', '360', '2013-06-21 20:00:59'),) <br/> (('37', '10', '4', '315000', '2013-06-21 20:00:59'),) <br/> (('38', '6', '4', '959000', '2013-06-22 20:00:56'),) <br/> (('39', '7', '4', '1110000', '2013-06-22 20:00:58'),) <br/> (('40', '8', '4', '7', '2013-06-22 20:00:59'),) <br/> (('41', '9', '4', '360', '2013-06-22 20:00:59'),) <br/> (('42', '10', '4', '314000', '2013-06-22 20:01:00'),)'''
    res=get_count_array(6,content)
    print len(res)
    
