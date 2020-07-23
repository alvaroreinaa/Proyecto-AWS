import json
import sys, os, base64, datetime, hashlib, hmac 

access_key = 'ASIATJAQLWKNDPBBOVR6'
secret_key = '2Rh23G6652k3utYrv8KwcjcoRvsInYe6Sli4pZda'
securityToken = 'FwoGZXIvYXdzEFQaDI9opbEr36ioMIOAWyLKAdAI1supAXlKJ97PJO6rs/sfNvKaK7Kr+rnTuIBrTN819xfHq1qAwcM/lH/LMuB7aS4m/QaF93PV6kbhsSxRMFmq9N0JYWQKdiEDNDtORuJH21O6avEIon1rwwu3snNv73dVk/V4WkVal8c45jpf0oX/Ak+3THmwOFkIDzIH0CspjPdL+lOjZFkbW6T6neEjZhLrsYjlG5ZYVNk7OolOOFRVfTKXU8GTkzXfsNQoi0CLRpvIvdIliUCyUi6cfdIJTpJ4dL0Oy8hXtFIosMfB9QUyLfKuC3ctzmtSmMBTnSVZeJF0nF6TtXoxwc7Psih3AfLVDnuB+GlUoYUagJgBmQ=='

bucket = "webdistribuidos"
bucketUrl = "http://webdistribuidos.s3.us-east-1.amazonaws.com/"
region = 'us-east-1'
service = 's3'

t = datetime.datetime.utcnow()
amzDate = t.strftime('%Y%m%dT%H%M%SZ')
dateStamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope
    
def poli(user_event):
    policy = """{"expiration": "2020-12-30T12:00:00.000Z",
    "conditions": [
    {"bucket": \"""" + bucket + """\"},
    ["starts-with", "$key", ""],
    {"acl": "public-read"},
    {"success_action_redirect": \""""+ bucketUrl+"""templates/perfil.html#""" + user_event + """\"},
        {"x-amz-credential": \""""+ access_key+"/"+dateStamp+"/"+region+"""/s3/aws4_request"},
        {"x-amz-algorithm": "AWS4-HMAC-SHA256"},
        {"x-amz-date": \""""+amzDate+"""\" },
        {"x-amz-security-token": \"""" + securityToken +"""\"  }
      ]
    }"""
    
    return policy

# Key derivation functions. See:
# http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning


def lambda_handler(event, context):
    # TODO implement
    stringToSign= b""
    # Almaceno el nombre de usuario
    user_event = event["queryStringParameters"]["nombre_usuario"]
    policy = poli(user_event)
    stringToSign=base64.b64encode(bytes((policy).encode("utf-8")))

    
    signing_key = getSignatureKey(secret_key, dateStamp, region, service)
    signature = hmac.new(signing_key, stringToSign, hashlib.sha256).hexdigest()
    
    #print(dateStamp)
    #print(signature)
    print(policy)
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin' : '*' },
        'body':json.dumps({ 'stringSigned' :  signature , 'stringToSign' : stringToSign.decode('utf-8') , 'xAmzCredential' : access_key+"/"+dateStamp+"/"+region+ "/s3/aws4_request" , 'dateStamp' : dateStamp , 'amzDate' : amzDate , 'securityToken' : securityToken })
    }