# -*- coding: utf-8 -*-
import time
import uuid
import hashlib
import base64
import requests #Run pip install requests to install the dependency.

#Mandatory. The values here are example values only. Obtain the actual values based on Development Preparation.
url = 'https://smsapi.ap-southeast-1.myhuaweicloud.com:443/sms/batchSendSms/v1' #Application access address and API access URI
APP_KEY = "c8RWg3ggEcyd4D3p94bf3Y7x1Ile" #Application Key
APP_SECRET = "q4Ii87BhST9vcs8wvrzN80SfD7Al" #Application Secret
sender = "csms12345678" #Channel number for Chinese mainland SMS or international SMS
TEMPLATE_ID = "8ff55eac1d0b478ab3c06c3c6a492300" #Template ID

#Mandatory for Chinese mainland SMS. This parameter is valid and mandatory when Template Type corresponding to templateId is Universal template. The signature name must be approved and be the same type as the template.
#This parameter is not required for international SMS.
signature = "HUAWEI CLOUD SMS test"; #Signature name

#Mandatory. Global number format (including the country code), for example, +8615123456789. Use commas (,) to separate multiple numbers.
receiver = "+8615123456789, +8615234567890" #Recipient number

# Optional. Address for receiving SMS status reports. The domain name is recommended. If this parameter is set to an empty value or left unspecified, customers do not receive status reports.
statusCallBack = ""

'''
Optional. If a template with no variable is used, assign an empty value to this parameter, for example, TEMPLATE_PARAM = '';
Example of a single-variable template: If the template content is "Your verification code is ${NUM_6}", TEMPLATE_PARAM can be set to '["369751"]'.
Example of a dual-variable template: If the template content is "You have ${NUM_2} parcels delivered to ${TXT_20}", TEMPLATE_PARAM can be set to '["3","main gate of People's Park"]'.
To view more information, choose Service Overview > Template and Variable Specifications.
'''
TEMPLATE_PARAM = '["369751"]' #Template variable. The following uses a single-variable verification code SMS message as an example. The customer needs to generate a 6-digit verification code and define it as a character string to prevent the loss of first digits 0 (for example, 002569 is changed to 2569).

'''
Construct the value of X-WSSE.
@param appKey: string
@param appSecret: string
@return: string
'''
def buildWSSEHeader(appKey, appSecret):
    now = time.strftime('%Y-%m-%dT%H:%M:%SZ') #Created
    nonce = str(uuid.uuid4()).replace('-', '') #Nonce
    digest = hashlib.sha256((nonce + now + appSecret).encode()).hexdigest()

    digestBase64 = base64.b64encode(digest.encode()).decode() #PasswordDigest
    return 'UsernameToken Username="{}",PasswordDigest="{}",Nonce="{}",Created="{}"'.format(appKey, digestBase64, nonce, now);

def main():
    #Request headers
    header = {'Authorization': 'WSSE realm="SDP",profile="UsernameToken",type="Appkey"',
              'X-WSSE': buildWSSEHeader(APP_KEY, APP_SECRET)}
    # Request body
    formData = {'from': sender,
                'to': receiver,
                'templateId': TEMPLATE_ID,
                'templateParas': TEMPLATE_PARAM,
                'statusCallback': statusCallBack,
#                'signature': signature #Uncomment this line if the universal template for Chinese mainland SMS is used.
                }
    print(header)
    
    # Ignore the certificate trust issues to prevent API calling failures caused by HTTPS certificate authentication failures.
    r = requests.post(url, data=formData, headers=header, verify=False)
    print(r.text) #Record the response.

if __name__ == '__main__':
    main() 
