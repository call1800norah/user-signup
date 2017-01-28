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

form= """
    <form method="post">
        <h2>Signup</h2>
        <label> Username
        <input type="text" name="username">
        </label>
        <br>
        <label> Password
        <input type="text" name="password" value="">
        </label>
        <br>
        <label> Verify Password
        <input type="text" name="verify" value="">
        </label>
        <br>
        <label> Email(optional)
        <input type="text" name="email">
        </label>
        <br>
        <input type="submit"/>
    </form>
"""

class MainHandler(webapp2.RequestHandler):

    def get(self):

        error = self.request.get('error')
        content = form + error
        self.response.write(content)


    def post(self):
        username = self.request.get('username')
        if (" " in username) or (username.strip() == ""):
            error = "That's not a valid username."
            error_escaped = cgi.escape(error, quote=True)

            self.redirect("/?error=" + error_escaped)

        password = self.request.get('password')
        if " " in password:
            error = "That wasn't a valid password."
            error_escaped = cgi.escape(error,quote=True)
            self.redirect("/?error=" + error_escaped)

        verify = self.request.get('verify')
        email = self.request.get('email')

        self.response.write(form)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
