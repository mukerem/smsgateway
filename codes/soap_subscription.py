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
url = f"http://{ip}:{port}/SubscribeManageService/services/SubscribeManage"


def main():

   data = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<soapenv:Body>
<ns1:syncOrderRelation
xmlns:ns1="http://www.csapi.org/schema/parlayx/data/sync/v1_0/local">
<ns1:userID>
<ID>+251913152485</ID>
<type>0</type>
</ns1:userID>
<ns1:spID>{username}</ns1:spID>
<ns1:productID>1000000423</ns1:productID>
<ns1:serviceID>0011002000001100</ns1:serviceID>
<ns1:serviceList>0011002000001100</ns1:serviceList>
<ns1:updateType>1</ns1:updateType>
<ns1:updateTime>20130723082551</ns1:updateTime>
<ns1:updateDesc>Addition</ns1:updateDesc>
<ns1:effectiveTime>20130723082551</ns1:effectiveTime>
<ns1:expiryTime>20361231160000</ns1:expiryTime>
<ns1:extensionInfo>
<item>
<key>accessCode</key>
<value>20086</value>
</item>
<item>
<key>chargeMode</key>
<value>0</value>
</item>
<item>
<key>MDSPSUBEXPMODE</key>
<value>1</value>
</item>
<item>
<key>objectType</key>
<value>1</value>
</item>
<item>
<key>isFreePeriod</key>
<value>false</value>
</item>
<item>
<key>payType</key>
<value>0</value>
</item>
<item>
<key>transactionID</key>
<value>504016000001307231624304170004</value>
</item>
<item>
<key>orderKey</key>
<value>999000000000000194</value>
</item>
<item>
<key>keyword</key>
<value>sub</value>
</item>
<item>
<key>cycleEndTime</key>
<value>20130822160000</value>
</item>
<item>
<key>durationOfGracePeriod</key>
<value>-1</value>
</item>
<item>
<key>serviceAvailability</key>
<value>0</value>
</item>
<item>
<key>channelID</key>
<value>1</value>
</item>
<item>
<key>TraceUniqueID</key>
<value>504016000001307231624304170005</value>
</item>
<item>
<key>operCode</key>
<value>zh</value>
</item>
<item>
<key>rentSuccess</key>
<value>true</value>
</item>
<item>
<key>try</key>
<value>false</value>
</item>
<item>
<key>shortMessage</key>
<value>Hello world.</value>
</item>
</ns1:extensionInfo>
</ns1:syncOrderRelation>
</soapenv:Body>
</soapenv:Envelope>"""
   
   header = {
        'Content-Type': 'text/xml; charset=utf-8',
   }
   r = requests.post(url, data=data, headers=header, verify=False)
   print(r.text) #Record the response.

if __name__ == '__main__':
    main() 