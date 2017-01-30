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

form = """
<form method= "post">
<h2>Signup</h2>
    <label> Username
    <input type="text" name="username" value="%(username)s">
    </label>
    <span style="color: red">%(error)s</span>
    <br>
    <label> Password
    <input type="password" name="password" value="">
    </label>
    <span style="color: red">%(erro)s</span>
    <br>
    <label> Verify Password
    <input type="password" name="verify" value="">
    </label>
    <span style="color: red">%(err)s</span>
    <br>
    <label> Email(optional)
    <input type="text" name="email" value="%(email)s">
    </label>
    <span style="color: red">%(er)s</span>
    <br>
    <input type="submit">
</form>
"""
def valid_username(username):
    if (" " in username) or (username.strip() == ""):
        return "That's not a valid username."

def valid_password(password):
    if password.strip() == "":
        return "That was not a valid password."
def valid_verify(verify):
    if not verify:
        return "Your password didn't match."
def valid_email(email):
    if string.punctuation not in email:
        return "That's not a valid email."
def escape_html(s):
    return cgi.escape(s,quote=True)

class MainHandler(webapp2.RequestHandler):

    def write_form(self,error="",erro="",err="",er="",username="",email=""):
        self.response.write(form % {"error":error,"username":escape_html(username),
                                    "erro":erro,"err":err,
                                    "er":er,"email":escape_html(email)})

    def get(self):
        self.write_form()

    def post(self):
        user_username = self.request.get("username")
        user_password = self.request.get("password")
        user_verify = self.request.get("verify")
        user_email = self.request.get("email")

        username = valid_username(user_username)
        password =  valid_password(user_password)
        verify = valid_verify(user_verify)
        email = valid_email(user_email)
        if not username:
            self.write_form(username)
        elif not password:
            self.write_form(valid_password)
        elif not verify:
            self.write_form(valid_verify)
        elif not email:
            self.write_form(valid_email)
        else:
            self.redirect("/thanks")

class ThanksHandler(webapp2.RequestHandler):
    def get(self):
         self.response.write("Welcome ")
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/thanks', ThanksHandler)
], debug=True)
