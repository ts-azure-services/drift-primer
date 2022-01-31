import urllib.request
import json
import os
import ssl

#def allowSelfSignedHttps(allowed):
#    # bypass the server certificate verification on client side
#    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
#        ssl._create_default_https_context = ssl._create_unverified_context
#
#allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.
import pandas as pd
# make a single prediction with the model
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_blobs
# create the inputs and outputs
X, y = make_blobs(n_samples=10000, centers=2, n_features=2, random_state=2)

data_list = []
for i,v in enumerate(X):
    temp_dict = {'att1':X[i][0], 'att2':X[i][1]}
    data_list.append(temp_dict)

data = {
    "Inputs": {
        "data": data_list,
    },
    "GlobalParameters": {
        'method': "predict",
    }
}

## Request data goes here
#data = {
#    "Inputs": {
#        "data":
#        [
#            {
#                'att1': "1.53230788",
#                'att2': "-1.88971185",
#            },
#        ],
#    },
#    "GlobalParameters": {
#        'method': "predict",
#    }
#}

body = str.encode(json.dumps(data))

url = 'https://dsafsadfd.westus.inference.ml.azure.com/score'
api_key = 'EfQ5JpmnaCPdC0PTBI6xdNmcHIGDv6bT' # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)
    result = response.read().decode("utf8", "ignore")
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))
    # Print the headers - they include the request ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(json.loads(error.read().decode("utf8", 'ignore')))
