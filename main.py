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
    return USER_RE.match(username)

def validate_password(password):
    return PASS_RE.match(password)

def validate_email(email):
    return EMAIL_RE.match(email)

class Index(webapp2.RequestHandler):
    """Handles requests coming in to '/'"""

    def get(self):
        signup_header = "<h3>Create a Username and Password</h3>"

        username_row = """
        <tr>
            <td>
                <label for="username">Username</label>
            </td>
            <td>
                <input name="username" required="" type="text" value=""/>
                <span class="error"></span>
            </td>
        </tr>
        """

        password_row = """
        <tr>
            <td>
                <label for="password">Password</label>
            </td>
            <td>
                <input name="password" required="" type="password" value=""/>
                <span class="error"></span>
            </td>
        </tr>"""

        verify_row = """
        <tr>
            <td>
                <label for="verify">Verify Password</label>
            </td>
            <td>
                <input name="verify" required="" type="password" value=""/>
                <span class="error"></span>
            </td>
        </tr>
        """

        email_row = """
        <tr>
            <td>
                <label for="email">Email (optional)</label>
            </td>
            <td>
                <input name="email" required="" type="email" value=""/>
                <span class="error"></span>
            </td>
        </tr>
        """

        table_body = "<table><tbody>" + username_row + password_row + verify_row + email_row + "</tbody></table>"

        submit_button = """<input type="submit" value="Submit Info"/>"""

        signup_form = """<form method="post">""" + table_body + submit_button + "</form>"

        content = page_header + signup_header + signup_form + page_footer

        self.response.write(content)

class Username(webapp2.RequestHandler):
    """Handles requests coming in to '/Username'"""

    def post(self):
        username = self.request.get("username")

        if not validate_username(username):
            error = "Invalid Username"
            self.redirect("/?error=" + error)

        #self.response.write(content)


class Password(webapp2.RequestHandler):
    """Handles requests coming in to '/Password'"""

class Email(webapp2.RequestHandler):
    """Handles requests comong in to '/Email'"""

app = webapp2.WSGIApplication([
    ('/', Index)
], debug=True)
