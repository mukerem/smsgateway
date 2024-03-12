import time
import uuid
import hashlib
import base64
import requests
import json

f = open("config.json")
config = json.load(f)
username = config["username"]
password = config["password"]
ip = config["ip"]
port = config["port"]
apiVersion = config["apiVersion"]
senderAccess = config["senderAccess"]
senderName = config["senderName"]
message = config["message"]
receiverAddress = config["receiverAddress"]
serviceID = senderAccess
senderAddress = senderAccess
url = f"http://{ip}:{port}/{apiVersion}/smsmessaging/outbound/{senderAddress}/requests"
# url = f"http://{ip}:{port}/SendSmsService/services/SendSms"



'''
Construct the value of X-WSSE.
@param appKey: string
@param appSecret: string
@return: string
'''
def buildWSSEHeader(username, password):
    now = time.strftime('%Y-%m-%dT%H:%M:%SZ') #Created
    nonce = str(uuid.uuid4()).replace('-', '') #Nonce
    digest = hashlib.sha256((nonce + now + password).encode()).hexdigest()

    digestBase64 = base64.b64encode(digest.encode()).decode() #PasswordDigest
    return 'UsernameToken Username="{}",PasswordDigest="{}",Nonce="{}",Created="{}"'.format(username, digestBase64, nonce, now);

def main():
    #Request headers
    header = {
            'Authorization': 'WSSE realm="SDP",profile="UsernameToken",type="Appkey"',
            'X-WSSE': buildWSSEHeader(username, password),
            'X-RequestHeader': 'request ServiceId="{}", FA="tel:12312312123",PresentId="12132131",LinkId="12132131"'.format(serviceID),
            'Accept-Encoding': 'gzip,deflate',
            'Accept': 'application/xml',
            # 'User-Agent': 'Jakarta Commons-HttpClient/3.1',
            'Host': '10.190.10.16:8313',
            'Content-Type': 'application/xml; charset=UTF-8',
            'Content-Length': '758'
              }
    
    formData = {
            "outboundSMSMessageRequest": {
                "address": receiverAddress,
                "senderAddress": senderAccess,
                "senderName": senderName,
                # "receiptRequest": {
                #     "notifyURL":"http://10.135.178.84:9088/",
                #     "callbackData":"123",
                #     "notificationFormat":"json"
                # },
                "outboundSMSTextMessage": {
                    "message": message
                }
            }
        }
    data = f"""<?xml version="1.0" encoding="UTF-8"?>
        <sms:outboundSMSMessageRequest xmlns:sms="urn:oma:xml:rest:sms:1">
        <address>{receiverAddress}</address>
        <senderAddress>{senderAccess}</senderAddress>
        <senderName>{senderName}</senderName>
        <receiptRequest>
        <notifyURL>https://209.97.154.21/</notifyURL>
        <callbackData>12345</callbackData>
        <notificationFormat>xml</notificationFormat>
        </receiptRequest>
        <outboundSMSTextMessage>
        <message>{message}</message>
        </outboundSMSTextMessage>
        <clientCorrelator>67893</clientCorrelator>
        </sms:outboundSMSMessageRequest>"""
    try:
        r = requests.post(url, data={}, headers=header, verify=False)
        print(r.text) #Record the response.
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main() 