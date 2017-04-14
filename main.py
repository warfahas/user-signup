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
    #Create a function for error.

    def get(self):
        add_form = """
        <h1>Signup</h1>
        <form method="post" action="/">
            <table>
                <tr>
                    <td class="label">Username</td>
                    <td>
                        <input name="username" type="text" value="">
                    </td>
                        <td class="error">{error.error_username}
                    </td>
                </tr>
                <tr>
                    <td class="label">Password</td>
                    <td>
                        <input name="password" type="password">
                    </td>
                        <td class="error">{error.error_password}
                    </td>
                </tr>
                <tr>
                    <td class="label">Verify Password</td>
                    <td>
                        <input name="verify" type="password">
                    </td>
                        <td class="error>{error.error_verify}
                    </td>
                </tr>
                <tr>
                    <td class="label">Email (optional)</td>
                    <td>
                        <input name="email" type="email" value="">
                    </td>
                        <td class="error">{error.error_email}
                    </td>
                </tr>
            </table>
            <input type="submit" value="Submit">
        </form>
        """.format(error)

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        error = {}

        if not valid_username(username):
            error["error_username"] = "That's not a valid username."
            have_error = True


        if not valid_password(password):
            error["error_password"] = "That wasn't a valid password."
            have_error = True

        elif password != verify:
            error["error_verify"] = "Your passwords didn't match."
            have_error = True


        if not valid_email(email):
            error["error_email"] = "That's not a valid email."
            have_error = True







        if have_error:
            self.redirect("/")
        else:
            self.redirect("/welcome?username=" + username)




class Welcome(webapp2.RequestHandler):

    def post(self):

        sentence = "Welcome, " + username + "!"
        content = page_header + "<h1>" + sentence + "</h1>" + page_footer
        self.response.write(content)







app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', Welcome)
], debug=True)
