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
add_form = """
<h1>Signup</h1>
<form method="post" action="/">
    <table>
        <tr>
            <td class="label">Username</td>
            <td>
                <input name="username" type="text" value="">
            </td>
                <td class="error">%(error_username)s
            </td>
        </tr>
        <tr>
            <td class="label">Password</td>
            <td>
                <input name="password" type="password">
            </td>
                <td class="error">%(error_password)s
            </td>
        </tr>
        <tr>
            <td class="label">Verify Password</td>
            <td>
                <input name="verify" type="password">
            </td>
                <td class="error">%(error_verify)s
            </td>
        </tr>
        <tr>
            <td class="label">Email (optional)</td>
            <td>
                <input name="email" type="email" value="">
            </td>
                <td class="error">%(error_email)s
            </td>
        </tr>
    </table>
    <input type="submit" value="Submit">
</form>
"""


class Index(webapp2.RequestHandler):

    def write_form(self, error_username="", error_password="", error_verify="", error_email=""):
        self.response.out.write(add_form % {"error_username": error_username, "error_password": error_password, "error_verify": error_verify, "error_email": error_email})

    def get(self):
        self.write_form()








    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')


        error = dict(username=username, password=password, verify=verify, email=email)
        if not valid_username(username):
            error['error_username'] = self.write_form("That's not a valid username.")




        elif not valid_password(password):
            error['error_password'] = self.write_form("That wasn't a valid password.")



        elif password != verify:
            error['error_verify'] = self.write_form("Your passwords didn't match.")




        elif not valid_email(email):
            error['error_email'] = self.write_form("That's not a valid email.")




        else:
            self.redirect("/welcome?username=" + username)




class Welcome(webapp2.RequestHandler):

    def get(self):
        username = self.request.get('username')
        sentence = "Welcome, " + username + "!"
        content = page_header + "<h1>" + sentence + "</h1>" + page_footer
        self.response.out.write(content)







app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', Welcome)
], debug=True)
