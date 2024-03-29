# Web3-Auth-Django

Web3-Auth-Django allows user to login to the Django application with the help of meta-mask. 

**Note:** This project is not entirely built from scratch, this is the newest version of an old project which we found on the internet. The old project had lot of errors but this version is coming with complete bug fixes and upgrades (The older version was causing a lot of errors.). Also this package perfectly works fine in linux machines, but when it comes to windows it has the following error. (Check at end)

## Back-end Setup

Install the package

`pip install web3-authentication-django`

Add it to your **INSTALLED_APPS**:

```django
INSTALLED_APPS = (
    ...
    'web3auth.apps.Web3AuthConfig',
    ...
)
```

Set 'web3auth.backend.Web3Backend' as your authentication backend:

``` django
AUTHENTICATION_BACKENDS = [
'django.contrib.auth.backends.ModelBackend',
'web3auth.backend.Web3Backend'
]
```
Add web3-Auth-Django to URL patterns:

```
from web3auth import urls as web3auth_urls
from django.urls import re_path

urlpatterns = [
    ...
    re_path(r'^', include(web3auth_urls)),
    ...
]
```

## Frontend Setup

Inside templates folder of your project, create a new folder called **web3auth**

and inside that create a file called **signup.html** and add this code

```
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
  </head>
  <body>
    <form action="" method="POST">
      {% csrf_token %}
      {{ form.as_p }}
      <button type="submit">Sign Up</button>
    </form>
  </body>
</html>

```

**Note**: Use **crispy forms**  to make the sign-up form beautiful.

**Now add the sign-up and login buttons in the required HTML file**

```
<a href="{% url 'web3auth:web3auth_signup' %}"><button>Sign Up using Metamask</button></a> 

<button onclick="startLogin()" type=submit>Login using Metamask</button>
```

Note: You can customise the buttons as you like but don't change the URL inside it

**Now need to add the following scripts to make the login button work**

```
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>



<script src="https://cdn.jsdelivr.net/npm/web3@latest/dist/web3.min.js"></script>
<!-- if the above script did not work use the below script -->
<script src="https://cdn.jsdelivr.net/gh/ethereum/web3.js@1.0.0-beta.34/dist/web3.min.js"></script>
   

<script>
 function startLogin() {
    let web3 = new Web3(window.ethereum);


    function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function loginWithSignature(address, signature, login_url, onLoginRequestError, onLoginFail, onLoginSuccess) {
    var request = new XMLHttpRequest();
    request.open('POST', login_url, true);
    request.onload = function () {
        if (request.status >= 200 && request.status < 400) {
            // Success!
            var resp = JSON.parse(request.responseText);
            if (resp.success) {
                if (typeof onLoginSuccess == 'function') {
                    onLoginSuccess(resp);
                }
            } else {
                if (typeof onLoginFail == 'function') {
                    onLoginFail(resp);
                }
            }
        } else {
            // We reached our target server, but it returned an error
            console.log("Autologin failed - request status " + request.status);
            if (typeof onLoginRequestError == 'function') {
                onLoginRequestError(request);
            }
        }
    };

    request.onerror = function () {
        console.log("Autologin failed - there was an error");
        if (typeof onLoginRequestError == 'function') {
            onLoginRequestError(request);
        }
        // There was a connection error of some sort
    };
    request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    var formData = 'address=' + address + '&signature=' + signature;
    request.send(formData);
}

function checkWeb3(callback) {
    web3.eth.getAccounts(function (err, accounts) { // Check for wallet being locked
        if (err) {
            throw err;
        }
        callback(accounts.length !== 0);
    });
}

function web3Login(login_url, onTokenRequestFail, onTokenSignFail, onTokenSignSuccess, // used in this function
                   onLoginRequestError, onLoginFail, onLoginSuccess) {
    // used in loginWithSignature

    // 1. Retrieve arbitrary login token from server
    // 2. Sign it using web3
    // 3. Send signed message & your eth address to server
    // 4. If server validates that you signature is valid
    // 4.1 The user with an according eth address is found - you are logged in
    // 4.2 The user with an according eth address is NOT found - you are redirected to signup page


    var request = new XMLHttpRequest();
    request.open('GET', login_url, true);

    request.onload = async function () {
        if (request.status >= 200 && request.status < 400) {
            // Success!
            var resp = JSON.parse(request.responseText);
            var token = resp.data;
            console.log("Token: " + token);
            var msg = web3.utils.toHex(token);
            var from = await web3.eth.getAccounts();
            web3.eth.personal.sign(msg, from[0], function (err, result) {
                if (err) {
                    if (typeof onTokenSignFail == 'function') {
                        onTokenSignFail(err);
                    }
                    console.log("Failed signing message \n" + msg + "\n - " + err);
                } else {
                    console.log("Signed message: " + result);
                    if (typeof onTokenSignSuccess == 'function') {
                        onTokenSignSuccess(result);
                    }
                    loginWithSignature(from, result, login_url, onLoginRequestError, onLoginFail, onLoginSuccess);
                }
            });

        } else {
            // We reached our target server, but it returned an error
            console.log("Autologin failed - request status " + request.status);
            if (typeof onTokenRequestFail == 'function') {
                onTokenRequestFail(request);
            }
        }
    };

    request.onerror = function () {
        // There was a connection error of some sort
        console.log("Autologin failed - there was an error");
        if (typeof onTokenRequestFail == 'function') {
            onTokenRequestFail(request);
        }
    };
    request.send();
}    
  if (typeof web3 !== 'undefined') {
    checkWeb3(async function (loggedIn) {
      if (!loggedIn) {
        // web3 = await window.ethereum.enable();
        web3 = await window.ethereum.request({method: 'eth_requestAccounts'})
        window.web3 = new Web3(window.ethereum);
        // alert("Please unlock your web3 provider (probably, Metamask)")
      } else {
        var login_url = "{% url 'web3auth:web3auth_login_api' %}";
        web3Login(login_url, console.log, console.log, console.log, console.log, console.log, function (resp) {
          console.log(resp);
          window.location.replace(resp.redirect_url);
        });
      }
    });

  } else {
    alert('web3 missing');
  }
}

 </script> 
```

Make Sure to add LOGIN_REDIRECT_URL in the settings.py file

```
LOGIN_REDIRECT_URL = 'route where you want to redirect after login'
```

To fetch the login successful message in the frontend side use this
``` 
{% if messages %}
    {% for message in messages %}
        <div class="alert alert-success">
            {{ message }}
        </div>
    {% endfor %}
{% endif %}

```
**Note**: You can create your own success message class.

Congrats, now you have successfully added meta mask authentication to your Django project

**Output:**

https://youtu.be/O19PeGDL8Fk


## Common Issues

**Linux**

while installing the main package you will face some installation issue that can be overcome by running the below commands

```
sudo apt-get install python3-dev
sudo apt install libpython3.9-dev
```

In second command replace 3.9 with the version you are using.

**Windows**
while installing the main package in windows you may get the following issue:
https://github.com/ethereum/ethash/issues/131 (this has the solution for the issue).

## Contributers

<a href="https://github.com/ahn1305/web3-django-authentication/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ahn1305/web3-django-authentication" />
</a>

Made with [contrib.rocks](https://contrib.rocks).
