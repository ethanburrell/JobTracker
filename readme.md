NEW TABLES
var params = {
 AttributeDefinitions:[
            {
                'AttributeName': 'user_id',
                'AttributeType': 'S'
            },
        ],
        TableName:'UserProfiles_1',
        KeySchema:[
            {
                'AttributeName': 'user_id',
                'KeyType': 'HASH'
            },
        ],
        ProvisionedThroughput: {
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
}
 dynamodb.createTable(params, function(err, data) {
   if (err) console.log(err, err.stack); // an error occurred
   else     console.log(data);
 });

 var params = {
   TableName: 'UserProfiles_1',
   Item: {
   "user_id": '1',
   "items":{
     '132': {"key_id":132, "company":"Google", "position": "SE Intern", "next_steps": ["Coding", "phone"]},
     '133': {"key_id":133, "company":"FaceBook", "position": "DS Intern", "next_steps": ["Onsite", "Offer"]},
     "134": {"key_id":134, "company":"twitter", "position": "architectre", "next_steps": ["coffeechat", "denail"]},
     "135": {"key_id":135, "company":"oracle", "position": "sleeping", "next_steps": []}
   }
 }
};
docClient.put(params, function(err, data) {
   if (err) ppJson(err); // an error occurred
   else ppJson(data); // successful response
});

To GET
var params = {
    TableName: 'UserProfiles_1',
    Key: { // a map of attribute name to AttributeValue for all primary key attributes

        user_id: '1', //(string | number | boolean | null | Binary)
        // more attributes...

    }
};
docClient.get(params, function(err, data) {
    if (err) ppJson(err); // an error occurred
    else ppJson(data); // successful response
});


OTHER STUFF


var params = {
 AttributeDefinitions:[
            {
                'AttributeName': 'user_id',
                'AttributeType': 'S'
            },
        ],
        TableName:'UserProfiles',
        KeySchema:[
            {
                'AttributeName': 'user_id',
                'KeyType': 'HASH'
            },
        ],
        ProvisionedThroughput: {
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
}
 dynamodb.createTable(params, function(err, data) {
   if (err) console.log(err, err.stack); // an error occurred
   else     console.log(data);
 });




 var params = {
    TableName: 'UserProfiles',
    Item: {
        'user_id' : "1",
        "items":[
    {"key_id":132, "company":"Google", "position": "SE Intern", "next_steps": ["Coding", "phone"]
    },


    {"key_id":133, "company":"FaceBook", "position": "DS Intern", "next_steps": ["Onsite", "Offer"]
    },
    {"key_id":134, "company":"twitter", "position": "architectre", "next_steps": ["coffeechat", "denail"]
    },
    {"key_id":135, "company":"oracle", "position": "sleeping", "next_steps": []
    }
  ]

    }
};
docClient.put(params, function(err, data) {
    if (err) ppJson(err); // an error occurred
    else ppJson(data); // successful response
});
