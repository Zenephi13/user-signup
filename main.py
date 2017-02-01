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

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Sign-Up</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        User Sign-Up
    </h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S] + @[\S] + .[\S] + $")

def validate_username(username):
    return username and USER_RE.match(username)

def validate_password(password):
    return password and PASS_RE.match(password)

def validate_email(email):
    return not email and EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):
    """Handles requests coming in to '/'"""

    def get(self):
        signup_header = "<h3>Create a Username and Password</h3>"

        username_row = """
        <tr>
            <td>
                <label for="username">Username</label>
            </td>
            <td>
                <input name="username" required="" type="text" value="{0}"/>
                <span class="error">{1}</span>
            </td>
        </tr>
        """.format(username, username_error)

        password_row = """
        <tr>
            <td>
                <label for="password">Password</label>
            </td>
            <td>
                <input name="password" required="" type="password" value=""/>
                <span class="error">{0}</span>
            </td>
        </tr>""".format(password_error)

        verify_row = """
        <tr>
            <td>
                <label for="verify">Verify Password</label>
            </td>
            <td>
                <input name="verify" required="" type="password" value=""/>
                <span class="error">{0}</span>
            </td>
        </tr>
        """.format(verify_error)

        email_row = """
        <tr>
            <td>
                <label for="email">Email (optional)</label>
            </td>
            <td>
                <input name="email" type="email" value="{0}"/>
                <span class="error">{1}</span>
            </td>
        </tr>
        """.format(email, email_error)

        table_body = "<table><tbody>" + username_row + password_row + verify_row + email_row + "</tbody></table>"

        submit_button = """<input type="submit" value="Submit Info"/>"""

        signup_form = """<form method="post">""" + table_body + submit_button + "</form>"

        content = page_header + signup_header + signup_form + page_footer

        self.response.write(content)

    def post(self):
        username = cgi.escape(self.request.get("username"))
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = cgi.escape(self.request.get("email"))

        if not validate_username(username):
            username_error = "Invalid Username"
            self.redirect("/?error=" + username_error)

        if not validate_password(password):
            password_error = "Invalid Password"
            self.redirect("/?error=" + password_error)

        if verify != password:
            verify_error = "Password Doesn't Match"
            self.redirect("/?error=" + verify_error)

        if not validate_email(email):
            email_error = "Invalid Email"
            self.redirect("/?error=" + email_error)

        self.redirect("/welcome?username=" + username)

class Welcome(webapp2.RequestHandler):
    """Handles requests coming in to '/Welcome'"""

    def post(self):   
        user_welcome = "Welcome, " + username + "!"
        content = page_header + "<p>" + user_welcome + "</p>" + page_footer

        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
