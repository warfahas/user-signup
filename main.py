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
import re

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
    <style type="text/css">
        .error {
        color: red;
        }
    </style>
</head>
<body>

"""

page_footer = """
</body>
</html>
"""
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Index(webapp2.RequestHandler):
    def get(self):
        header = "<h1>Signup</h1>"
        add_form = """
        <form action="/add" method="post">
            <table>
                <tr>
                    <td><label for="username">Username</label></td>
                    <td>
                        <input name="username" type="text" value="">
                        <span class="error"></span>
                    </td>
                </tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td>
                        <input name="password" type="password">
                        <span class="error"></span>
                    </td>
                </tr>
                <tr>
                    <td><label for="verify">Verify Password</label></td>
                    <td>
                        <input name="verify" type="password">
                        <span class="error"></span>
                    </td>
                </tr>
                <tr>
                    <td><label for="email">Email (optional)</label></td>
                    <td>
                        <input name="email" type="email" value="">
                        <span class="error"></span>
                    </td>
                </tr>
            </table>
            <input type="submit" value="Submit">
        </form>
        """
        error = self.request.get("error")
        if error:
            error_esc = cgi.escape(error, quote=True)
            error_element = '<p class="error">' + error_esc + '</p>'
        else:
            error_element = ''
        main_content = header + add_form + error_element
        content = page_header + main_content + page_footer
        self.response.write(content)

class AddInfo(webapp2.RequestHandler):

    def post(self):
        #have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        #params = dict(username = username, email = email)
        if not valid_username(username):
            error_msg = "That's not a valid username."
            self.redirect("/?error=" + error_msg)

        if not valid_password(password):
            error_msg = "That wasn't a valid password."
            self.redirect("/?error=" + error_msg)
        elif password != verify:
            error_msg = "Your passwords didn't match."
            self.redirect("/?error=" + error_msg)

        if not valid_email(email):
            error_msg = "That's not a valid email."
            self.redirect("/?error=" + error_msg)

        username = cgi.escape(username)
        password = cgi.escape(password)
        verify = cgi.escape(verify)
        email = cgi.escape(email)

        sentence = "Welcome, " + username + "!"
        content = page_header + "<h1>" + sentence + "</h1>" + page_footer
        self.response.write(content)







app = webapp2.WSGIApplication([
    ('/', Index),
    ('/add', AddInfo)
], debug=True)
