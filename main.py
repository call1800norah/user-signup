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
import cgi
import string

form= """
    <form method="post">
        <h2>Signup</h2>
        <label> Username
        <input type="text" name="username" value="%(username)s">
        <span style="color: red">%(error)s</span>
        </label>

        <br>
        <label> Password
        <input type="password" name="password" value="">
        </label>
        <span style="color: red">%(error)s</span>
        <br>
        <label> Verify Password
        <input type="password" name="verify" value="">
        </label>
        <span style="color: red">%(error)s</span>
        <br>
        <label> Email(optional)
        <input type="text" name="email" value="%(email)s">
        </label>
        <span style="color: red">%(error)s</span>
        <br>
        <input type="submit"/>
    </form>
"""

def escape_html(s):
    return cgi.escape(s,quote=True)

class MainHandler(webapp2.RequestHandler):
    def write_form(self, error='',username='',
                   password='',verify='',email=''):
        self.response.write(form % {"error":error,
                                    "username":escape_html(username),
                                    "password":escape_html(password),
                                    "verify":escape_html(verify),
                                    "email":escape_html(email)})
    def get(self):

        self.write_form("")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        #error = self.request.get("error")

        if (" " in username) or (username.strip() == ""):

            self.write_form("That's not a valid username.",username )


        elif password.strip() == "":
            self.write_form("That wasn't a valid password.",password)


        elif password != verify:
            self.write_form("Your password didn't match.",verify)

        elif string.punctuation not in email:
            self.write_form("That's not a valid email",email)

        else:
           self.redirect("/thanks")

class ThanksHandler(webapp2.RequestHandler):
    def get(self):
         self.response.write("Welcome " + username)
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/thanks', ThanksHandler)
], debug=True)
