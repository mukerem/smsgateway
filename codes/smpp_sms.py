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
url = f"http://{ip}:{port}/SendSmsService/services/SendSms"


data = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                xmlns:v2="http://www.huawei.com.cn/schema/common/v2_1"
                xmlns:loc="http://www.csapi.org/schema/parlayx/sms/send/v2_2/local">
                <soapenv:Header>
                    <v2:RequestSOAPHeader>
                        <v2:spId>{username}</v2:spId>
                        <v2:spPassword>{password}</v2:spPassword>
                        <v2:serviceId>{serviceID}</v2:serviceId>
                        <v2:timeStamp>20220408064245</v2:timeStamp>
                        <v2:OA>8612312345678</v2:OA>
                        <v2:FA>8612312345678</v2:FA>
                        <v2:linkid>12345678901111</v2:linkid>
                        <v2:presentid>22345678901113</v2:presentid>
                    </v2:RequestSOAPHeader>
                </soapenv:Header>
                <soapenv:Body>
                    <loc:sendSms>
                        <loc:addresses>tel:{receiverAddress}</loc:addresses>
                        <loc:senderName>{senderName}</loc:senderName>
                        <loc:message>{message}</loc:message>
                        <loc:receiptRequest>
                            <endpoint>http://10.138.38.139:9080/notify</endpoint>
                            <interfaceName>SmsNotification</interfaceName>
                            <correlator>00001</correlator>
                        </loc:receiptRequest>
                    </loc:sendSms>
                </soapenv:Body>
            </soapenv:Envelope>"""

header = {
    'Content-Type': 'text/xml; charset=utf-8',
}


def main():

    try:
        r = requests.post(url, data=data, headers=header, verify=False)
        print(r.text) #Record the response.
    except Exception as e:
        print(e)





def sms():
    import urllib3
    http = urllib3.PoolManager()

    try:
        send_message = http.request('POST', url, body=data, headers=header)
        print(send_message.status)
    except TimeoutError:
        print("Request timed out")
    except Exception as e:
        print(e)




if __name__ == '__main__':
    sms() 