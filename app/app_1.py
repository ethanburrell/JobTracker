from flask import Flask, render_template, Response,request
import boto3
import json
import decimal

app = Flask(__name__)
# java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb -port 2345
#export FLASK_APP=app_1.py
#flask run

#https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.03.html
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

#https://aws.amazon.com/blogs/database/how-to-create-a-fast-and-globally-available-user-profiling-system-by-using-amazon-dynamodb-global-tables/
@app.route('/app')
def hello_world():
    # For a Boto3 client.
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:2345', region_name='us-west-2')
    table = dynamodb.Table('UserProfiles_1')

    response = table.get_item(
        Key={
            'user_id': '1'
        }
    )
    json_str = json.dumps(response["Item"], cls=DecimalEncoder)
    #print(json_str)
    #cleaned_json = json.loads(json_str)
    return render_template("input_template.html", job_input=json_str)

@app.route('/user/update_job', methods=['POST'])
def update_job():
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:2345', region_name='us-west-2')
    table = dynamodb.Table('UserProfiles_1')
    # helpful
    # https://stackoverflow.com/questions/51911927/update-nested-map-dynamodb
    #insert_values = request.values.get("body")
    #print(request.json)
    job_id = request.json["key_id"]

    response = table.update_item(
          Key={
            'user_id': '1'
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
    #print(response)

    return str(response)

@app.route('/user/remove_job', methods=['POST'])
def remove_job():
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:2345', region_name='us-west-2')
    table = dynamodb.Table('UserProfiles_1')
    # helpful
    # https://stackoverflow.com/questions/51911927/update-nested-map-dynamodb
    #insert_values = request.values.get("body")
    #print(request.json)
    job_id = request.json["key_id"]

    response = table.update_item(
          Key={
            'user_id': '1'
          },
          UpdateExpression="REMOVE #itms.#n",
          ExpressionAttributeNames={
            '#itms': 'items',
            '#n': job_id,
          },
        )

    #print(response)

    return str(response)







"""
ddb1 = boto3.client('dynamodb', endpoint_url='http://localhost:2345', region_name='us-west-2')
response = ddb1.list_tables()
print(response)
"""
"""
client = boto3.client('dynamodb', endpoint_url='http://localhost:2345', region_name='us-west-2')
#paginator = client.get_paginator('UserProfiles')
#table = client.Table('UserProfiles')

res = client.get_item(
    TableName='UserProfiles',
    Key={'user_id':{'S':str(1)}}
    )
print(res)
"""
"""
Key={
        'user_id': '1'
}
"""

"""
table = client.Table('UserProfiles')

response = table.scan()
data = response['Items']

while 'LastEvaluatedKey' in response:
    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    data.extend(response['Items'])
"""
