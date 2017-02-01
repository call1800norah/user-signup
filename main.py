##!/usr/bin/env python
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
import re

form = """
<form method= "post">
<h2>Signup</h2>
    <label> Username&nbsp;&nbsp;&nbsp;
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <input type="text" name="username" value="%(username)s">
    </label>
    <span style="color: red">%(user_error)s</span>
    <br>
    <label> Password &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            &nbsp;&nbsp;
    <input type="password" name="password" value="">
    </label>
    <span style="color: red">%(password_error)s</span>
    <br>
    <label> Verify Password
    <input type="password" name="verify" value="">
    </label>
    <span style="color: red">%(verify_error)s</span>
    <br>
    <label> Email(optional)&nbsp;
    <input type="text" name="email" value="%(email)s">
    </label>
    <span style="color: red">%(email_error)s</span>
    <br>
    <input type="submit">
</form>
"""
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)
PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)

def escape_html(s):
    return cgi.escape(s,quote=True)

class MainHandler(webapp2.RequestHandler):

    def write_form(self,user_error="",password_error="",verify_error="",
                   email_error="",username="",email=""):
        self.response.write(form % {"user_error":user_error,"password_error":password_error,
                                    "verify_error":verify_error,
                                    "email_error":email_error,
                                    "username":escape_html(username),
                                    "email":escape_html(email)})

    def get(self):
        self.write_form()

    def post(self):
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        user_error = ""
        if not valid_username(username):
            user_error="That's not a valid username."
            have_error = True
        password_error = ""
        if not valid_password(password):
            password_error="That was not a valid password."
            have_error = True

        verify_error = ""
        if password != verify:
             verify_error="Your passwords didn't match."
             have_error = True

        email_error = ""
        if not valid_email(email):
            email_error = "That's not a valid email."
            have_error = True

        if have_error:
            self.write_form(user_error=user_error,password_error=password_error,
                            verify_error=verify_error,email_error=email_error,
                            username=username,email=email)
        else:
            self.redirect("/unit2/Welcome?username=" + username)

class WelcomeHandler(webapp2.RequestHandler):

    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            content = '<h1>' + "Welcome, " + username + "!" + '</h1>'
            self.response.write(content)
        else:
            self.redirect('/')
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/unit2/Welcome', WelcomeHandler)
], debug=True)
