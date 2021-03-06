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

# main body of signup page
username_row = """
<tr>
    <td>
        <label for="username">Username</label>
    </td>
    <td>
        <input name="username" type="text" value="{}"/>
        <span class="error">{}</span>
    </td>
</tr>
"""

password_row = """
<tr>
    <td>
        <label for="password">Password</label>
    </td>
    <td>
        <input name="password" type="password" value=""/>
        <span class="error">{}</span>
    </td>
</tr>"""

verify_row = """
<tr>
    <td>
        <label for="verify">Verify Password</label>
    </td>
    <td>
        <input name="verify" type="password" value=""/>
        <span class="error">{}</span>
    </td>
</tr>
"""

email_row = """
<tr>
    <td>
        <label for="email">Email (optional)</label>
    </td>
    <td>
        <input name="email" value="{}"/>
        <span class="error">{}</span>
    </td>
</tr>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def validate_username(username):
    return username and USER_RE.match(username)

def validate_password(password):
    return password and PASS_RE.match(password)

def validate_email(email):
    return not email or EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):
    """Handles requests coming in to '/'"""



    def get(self):
        username = self.request.get("username")
        username_error = self.request.get("username_error")
        password_error = cgi.escape(self.request.get("password_error"))
        verify_error = cgi.escape(self.request.get("verify_error"))
        email = cgi.escape(self.request.get("email"))
        email_error = cgi.escape(self.request.get("email_error"))

        signup_header = "<h3>Create a Username and Password</h3>"

        table_body = "<table><tbody>" + username_row.format(username, username_error) + password_row.format(password_error) + verify_row.format(verify_error) + email_row.format(email, email_error) + "</tbody></table>"

        submit_button = """<input type="submit" value="Submit Info"/>"""

        signup_form = """<form action="/" method="post">""" + table_body + submit_button + "</form>"

        content = page_header + signup_header + signup_form + page_footer

        self.response.write(content)

    def post(self):
        have_error = False
        username = self.request.get("username")
        password = cgi.escape(self.request.get("password"))
        verify = cgi.escape(self.request.get("verify"))
        email = cgi.escape(self.request.get("email"))

        url_string = "/?username=" + username + "&email=" + email

        if not validate_username(username):
            username_error = "Invalid Username"
            url_string += "&username_error=" + username_error
            have_error = True

        if not validate_password(password):
            password_error = "Invalid Password"
            url_string += "&password_error=" + password_error
            have_error = True

        if verify != password:
            verify_error = "Password Doesn't Match"
            url_string += "&verify_error=" + verify_error
            have_error = True

        if not validate_email(email):
            email_error = "Invalid Email"
            url_string += "&email_error=" + email_error
            have_error = True

        if have_error:
            self.redirect(url_string)
        else:
            self.redirect("/welcome?username=" + username)

class Welcome(webapp2.RequestHandler):
    """Handles requests coming in to '/Welcome'"""

    def get(self):
        username = self.request.get("username")   
        user_welcome = "Welcome, " + username + "!"
        content = page_header + "<p>" + user_welcome + "</p>" + page_footer

        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
