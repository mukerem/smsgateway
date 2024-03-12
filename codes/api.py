import requests
import json
IP = "10.153.222.60"
Port = 1394
apiVersion = 1
senderAddress = "34100995005"
url = f"http://{IP}:{Port}/{apiVersion}/smsmessaging/outbound/{senderAddress}/subscriptions"

headers = {
    'Authorization': 'WSSE realm="SDP", profile="UsernameToken"', 
    'X-WSSE': 'UsernameToken Username="muke", PasswordDigest="SXoO32oqIKFOl63mvsMoW+HPcHo=", Nonce="2013042718064200001", Created="2018-11-11T10:50:49+00:00"', 
    "Content-Length": "137",
    "Content-Type": "application/json; charset=UTF-8",
    "X-RequestHeader": 'request ServiceId="35000001000001"',
    "Accept-Encoding": 'gzip,deflate',
    "Accept": 'application/json',
    "User-Agent": 'Jakarta Commons-HttpClient/3.1',
    "Host": '10.137.213.125:14312'
    }

data = {
    "from":"1069031221280012",
    "smsContent":[
        {
            "to":[
                "+8615512345678","+8615512345679"
            ],
            "templateId":"abcdefghabcdefghabcdefghabcdefgh",
            "templateParas":["062569"]},
        {
            "to":["+8615512345680"],
            "templateId":"hgfedcbahgfedcbahgfedcbahgfedcba",
            "templateParas":["605623"]}],
    "statusCallback":"http://205.145.111.168:9330/report"
}

r = requests.post(url, data=json.dumps(data), headers=headers)
