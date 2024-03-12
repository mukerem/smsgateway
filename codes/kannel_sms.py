import requests
# smsbox /home/andalus/Documents/toptech/SMS\ Gateway/kannel/kannel.conf
# bearerbox /home/andalus/Documents/toptech/SMS\ Gateway/kannel/kannel.conf
# /etc/init.d/kannel stop
# from_ = 9650
from_ = "9767"
to = "+251913152485 +251987301169" # for multi receiver separate the phone number by space
to = "+251913152485"
# to = "+251913152485 +251991234267 +251934739566 +251944121626 +251925768702 +251938651329 +251913343633"
to = "+251913343633 +251913152485 +251927721050 +251944121626 +251911714215"
username = "toptech"
password = "top@tech"
text = "أحبك لله"
text = "test from toptech"
text = "የፈርኒቸር ሽያጭዎን በቀላሉ ለመጨመር የፋሚሊሱቅ መተግበሪያን ከፕለይስቶር በማውረድ https://rb.gy/xflfcx  ወይንም በድረገፃችን https://familysooq.com ላይ ያስተዋውቁ!"

print(len(text), text)
coding="2" # used for non english characters only 70 characters is allowed
# if you use enlgish character you should remove coding parameter, otherwise 
# the smpp allowed only 70 characters. but if you remove it, then 160 character is allowed.
charset="UTF-8"

args = {
    'from_':from_, 
    'to':to, 
    'text':text, 
    'username': username, 
    'password': password,
    'coding': coding,
    'charset': charset
}

url = """http://127.0.0.1:6013/ethiotelecom/sendsms?from={from_}&to={to}&text={text}&username={username}&password={password}&coding={coding}&charset={charset}"""\
    .format(**args)
print(url)
def main():
    try:
        r = requests.get(url, data={}, headers={}, verify=False)
        print(r.text)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main() 

# text = "በዚህ ፕሮጀክት ላይ በጣም ፍላጎት አለኝ. ጥረቴን ሁሉ ለዚህ ሥራ ሰጥቻለሁ። ውጤቱ ጥሩ እንደሚሆን ተስፋ አደርጋለሁ. ጊዜዬን አስደሳች በሆኑ መስኮች ማሳለፍ ደስታዬ ነው።"
# text = "I am very interested in this project. I have put forth all this effort. I hope the result is good. I enjoy spending time in exciting fields. This is my message from your brother."