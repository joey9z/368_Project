#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
from lxml import html
from google.appengine.api import urlfetch
import jinja2

jinja = jinja2.Environment( loader=jinja2.FileSystemLoader( os.path.join( os.path.dirname(__file__), '') ) )

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja.get_template('index.html')
        html = template.render()
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(html)
        
class APIHandler(webapp2.RequestHandler):
    def get(self):
        url = "https://selfservice.mypurdue.purdue.edu/prod/bwckctlg.p_disp_course_detail?cat_term_in=201420&subj_code_in=PHYS&crse_numb_in=17200"
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            tree = html.fromstring(result.content)
            self.response.write(tree.text_content())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/api/', APIHandler)
], debug=True)
