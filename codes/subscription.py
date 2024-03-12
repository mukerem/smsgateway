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
url = f"http://{ip}:{port}/{apiVersion}/smsmessaging/outbound/{senderAddress}/subscriptions"



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
    header = {'Authorization': 'WSSE realm="SDP",profile="UsernameToken",type="Appkey"',
              'X-WSSE': buildWSSEHeader(username, password),
              'X-RequestHeader': 'request ServiceId="{}"'.format(serviceID)
              }
    
    formData = {
                "deliveryReceiptSubscription":
                    {
                    "callbackReference":
                        {
                        "notifyURL":"http://10.135.178.84:9088/",
                        "callbackData":"123",
                        "notificationFormat":"json"
                        },
                    "filterCriteria":"6513507551001"
                    }
                }
    
    # {
    #         "outboundSMSMessageRequest": {
    #             "address": receiverAddress,
    #             "senderAddress": senderAccess,
    #             "senderName": senderName,
    #             # "receiptRequest": {
    #             #     "notifyURL":"http://10.135.178.84:9088/",
    #             #     "callbackData":"123",
    #             #     "notificationFormat":"json"
    #             # },
    #             "outboundSMSTextMessage": {
    #                 "message": message
    #             }
    #         }
    #     }
    # print(header)
    # print(url)
    
    r = requests.post(url, data=formData, headers=header, verify=False)
    # print(r.text) #Record the response.

if __name__ == '__main__':
    main() 