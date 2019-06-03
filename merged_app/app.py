from pprint import pformat
from time import time
import boto3
import json
from flask import Flask, request, redirect, session, url_for, render_template, Response
from flask.json import jsonify
import requests
from requests_oauthlib import OAuth2Session
import decimal
import botocore


app = Flask(__name__)
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

app.secret_key = os.urandom(24)

# This information is obtained upon registration of a new Google OAuth
# application at https://code.google.com/apis/console
client_id = '125069500182-rss8qgel94h6u3as9vtobuhvnilioq3r.apps.googleusercontent.com'
client_secret = 'ESRcT2283QlVou54alm83AJE'
redirect_uri = 'http://127.0.0.1:5000/callback'

# Uncomment for detailed oauthlib logs
#import logging
#import sys
#log = logging.getLogger('oauthlib')
#log.addHandler(logging.StreamHandler(sys.stdout))
#log.setLevel(logging.DEBUG)

# OAuth endpoints given in the Google API documentation
authorization_base_url = "https://accounts.google.com/o/oauth2/auth"
token_url = "https://accounts.google.com/o/oauth2/token"
refresh_url = token_url # True for Google but not all providers.
scope = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/login")
def demo():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Google)
    using an URL with a few key OAuth parameters.
    """
    google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    authorization_url, state = google.authorization_url(authorization_base_url,
        # offline for refresh token
        # force to always make user click authorize
        access_type="offline", prompt="select_account")

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    print(session['oauth_state'])
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.
@app.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    google = OAuth2Session(client_id, redirect_uri=redirect_uri,
                           state=session['oauth_state'])
    token = google.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)

    # We use the session as a simple DB for this example.
    session['oauth_token'] = token
    """
    email = jsonify(google.get('https://www.googleapis.com/oauth2/v1/userinfo').json())
    print(google.get('https://www.googleapis.com/oauth2/v1/userinfo'))

    dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:2345', region_name='us-west-2')
    table = dynamodb.Table('UserProfiles_1')
    response = table.put_item(
        Item = {
            'user_id': email,
            "items":{
               '132': {
                    "key_id":132, "company":"Google", "position": "SE Intern", "next_steps": ["Coding", "phone"]
                }
            }
        },
         ConditionExpression ="attribute_not_exists(user_id)",
    )
    print("Did it create a new item for user", response)
    """
    #return redirect(url_for('.menu'))
    return redirect(url_for('.profile'))


@app.route("/menu", methods=["GET"])
def menu():
    """"""
    return """
    <h1>Congratulations, you have obtained an OAuth 2 token!</h1>
    <h2>What would you like to do next?</h2>
    <ul>
        <li><a href="/profile"> Get account profile</a></li>
        <li><a href="/automatic_refresh"> Implicitly refresh the token</a></li>
        <li><a href="/manual_refresh"> Explicitly refresh the token</a></li>
        <li><a href="/validate"> Validate the token</a></li>
    </ul>

    <pre>
    %s
    </pre>
    """ % pformat(session['oauth_token'], indent=4)


@app.route("/profile", methods=["GET"])
def profile():
    """Fetching a protected resource using an OAuth 2 token.
    """
    google = OAuth2Session(client_id, token=session['oauth_token'])
    #print("googe user info", jsonify(google.get('https://www.googleapis.com/oauth2/v1/userinfo')).json()["email"])
    #print("type whats", )
    email = json.loads(google.get('https://www.googleapis.com/oauth2/v1/userinfo').text)["email"]
    session["email"] = email
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:2345', region_name='us-west-2')
    table = dynamodb.Table('UserProfiles_1')
    print("user email", email)
    try:
        response = table.put_item(
            Item = {
                'user_id': email,
                "items":{
                   '6969': {
                        "key_id":6969, "company":"Company", "position": "Position", "next_steps": ["Interview"]
                    }
                }
            },
             ConditionExpression="attribute_not_exists(user_id)",
        )
        print("Created a new item for the user", response)
    except botocore.exceptions.ClientError as e:
        # Ignore the ConditionalCheckFailedException, bubble up
        # other exceptions.
        print("user was already defined")
        if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise
    #return jsonify(google.get('https://www.googleapis.com/oauth2/v1/userinfo').json())

    response = table.get_item(
        Key={
            'user_id': email
        }
    )
    print("response to get", response)
    json_str = json.dumps(response["Item"], cls=DecimalEncoder)
    #print(json_str)
    #cleaned_json = json.loads(json_str)
    return render_template("input_template.html", job_input=json_str)
"""

"""

@app.route("/userinfo", methods=["GET"])
def userinfo():
    google = OAuth2Session(client_id, token=session['oauth_token'])
    return jsonify(google.get('https://www.googleapis.com/oauth2/v1/userinfo').json())

@app.route("/automatic_refresh", methods=["GET"])
def automatic_refresh():
    """Refreshing an OAuth 2 token using a refresh token.
    """
    token = session['oauth_token']

    # We force an expiration by setting expired at in the past.
    # This will trigger an automatic refresh next time we interact with
    # Googles API.
    token['expires_at'] = time() - 10

    extra = {
        'client_id': client_id,
        'client_secret': client_secret,
    }

    def token_updater(token):
        session['oauth_token'] = token

    google = OAuth2Session(client_id,
                           token=token,
                           auto_refresh_kwargs=extra,
                           auto_refresh_url=refresh_url,
                           token_updater=token_updater)

    # Trigger the automatic refresh
    jsonify(google.get('https://www.googleapis.com/oauth2/v1/userinfo').json())
    return jsonify(session['oauth_token'])


@app.route("/manual_refresh", methods=["GET"])
def manual_refresh():
    """Refreshing an OAuth 2 token using a refresh token.
    """
    token = session['oauth_token']

    extra = {
        'client_id': client_id,
        'client_secret': client_secret,
    }

    google = OAuth2Session(client_id, token=token)
    session['oauth_token'] = google.refresh_token(refresh_url, **extra)
    return jsonify(session['oauth_token'])

@app.route("/validate", methods=["GET"])
def validate():
    """Validate a token with the OAuth provider Google.
    """
    token = session['oauth_token']

    # Defined at https://developers.google.com/accounts/docs/OAuth2LoginV1#validatingtoken
    validate_url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?'
                    'access_token=%s' % token['access_token'])

    # No OAuth2Session is needed, just a plain GET request
    return jsonify(requests.get(validate_url).json())



@app.route('/user/update_job', methods=['POST'])
def update_job():
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:2345', region_name='us-west-2')
    table = dynamodb.Table('UserProfiles_1')

    google = OAuth2Session(client_id, token=session['oauth_token'])
    email = json.loads(google.get('https://www.googleapis.com/oauth2/v1/userinfo').text)["email"]
    # helpful
    # https://stackoverflow.com/questions/51911927/update-nested-map-dynamodb
    #insert_values = request.values.get("body")
    #print(request.json)
    job_id = request.json["key_id"]

    ### =====================================
    # CHECK TO SEE IF KEY EXISTS YET
    response = table.get_item(
        Key={
            'user_id': email
        },
        AttributesToGet = [
        "items","132"
    ]
    )
    try:
        err = response["items"][job_id]
        #if response["items"][job_id]["company"] == request.json["company"]

    except Exception as e:
        print(e)




    response = table.update_item(
          Key={
            'user_id': email
          },
          UpdateExpression="SET #itms.#n = :locVal",
          ExpressionAttributeNames={
            '#itms': 'items',
            '#n': job_id,
          },
          ExpressionAttributeValues={
            ':locVal': request.json,
          },
        )
    print("update_job", email, job_id, response)

    return str(response)

@app.route('/user/remove_job', methods=['POST'])
def remove_job():
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:2345', region_name='us-west-2')
    table = dynamodb.Table('UserProfiles_1')
    # helpful
    # https://stackoverflow.com/questions/51911927/update-nested-map-dynamodb
    #insert_values = request.values.get("body")
    #print(request.json)

    google = OAuth2Session(client_id, token=session['oauth_token'])
    email = json.loads(google.get('https://www.googleapis.com/oauth2/v1/userinfo').text)["email"]

    job_id = request.json["key_id"]

    response = table.update_item(
          Key={
            'user_id': email
          },
          UpdateExpression="REMOVE #itms.#n",
          ExpressionAttributeNames={
            '#itms': 'items',
            '#n': job_id,
          },
        )

    #print(response)

    return str(response)


@app.route('/viz', methods=['GET'])
def viz():
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:2345', region_name='us-west-2')
    table = dynamodb.Table('UserProfiles_1')
    # helpful
    # https://stackoverflow.com/questions/51911927/update-nested-map-dynamodb
    #insert_values = request.values.get("body")
    #print(request.json)

    google = OAuth2Session(client_id, token=session['oauth_token'])
    email = json.loads(google.get('https://www.googleapis.com/oauth2/v1/userinfo').text)["email"]

    response = table.get_item(
        Key={
            'user_id': email
        }
    )
    print("response to get", response)
    json_str = json.dumps(response["Item"], cls=DecimalEncoder)
    json_obj = json.loads(json_str)

    arr = []
    agg_arr = []
    for i in json_obj["items"]:
        company = json_obj["items"][i]["company"]
        next_steps = json_obj["items"][i]["next_steps"]
        stacked_arr = [[company]] + next_steps
        agg_stacked_arr = [["Applied"]] + next_steps
        for j in range(0, len(stacked_arr) - 1):
            arr.append([stacked_arr[j][0], stacked_arr[j+1][0], 1])
            agg_arr.append([agg_stacked_arr[j][0], agg_stacked_arr[j+1][0], 1])
    print(arr)
    str_arr = []
    for i in agg_arr:
        str_arr.append(str(i))
    print(str_arr)
    counts_dic = {i : str_arr.count(i) for i in str_arr}
    aggregrated_arr = []
    #single_objects = list(set(arr))
    print(counts_dic)
    for i in counts_dic.keys():
        temp = eval(i)
        count = counts_dic[i]
        first = temp[0]
        second = temp[1]
        c = temp[2]
        aggregrated_arr.append([first, second, count])
    print(aggregrated_arr)
    """
    for i in counts_dic.keys():
        temp = i
        temp = temp[2] =
        aggregrated_arr.append()
    """
    return render_template("visualization.html", data=arr, aggregrate_data=aggregrated_arr)



def huffmanDecode(dictionary, text):
    res = "["
    while text:
        for k in dictionary:
            if text.startswith(k):
                res += dictionary[k] + ", "
                text = text[len(k):]
    return res[:-2] + "]"

encoding_dict = {"1111": "On-Site",
"1110": "Coding Challenge",
"110": "Follow Up",
"101": "Denied",
"100": "Accepted",
"011": "Phone Screen 1",
"010": "No response",
"001": "Phone Screen 3",
"000": "Phone Screen 2"}

@app.route("/company", methods=["GET"])
def company_page():
    company_name = request.args.get('name')
    school = request.args.get('school')
    year = request.args.get('year')
    if not school and not year:
        print(company_name, type(company_name))
        #return company_name
        json = { "google": {
                "Software Engineering Intern" :{
                  "UC Berkeley": {
                      "Freshman": {
                        "011000": 4,
                        "1110101": 2
                      },
                      "Sophomore": {
                        "1110011000001101": 65,
                        "11100110000011111100": 2
                      }
                  }
                }
              }
            }
    print(huffmanDecode(encoding_dict, "11100110000011111100"))
    return str(json[company_name])


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    import os
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

    app.secret_key = os.urandom(24)
    app.run(debug=True)
