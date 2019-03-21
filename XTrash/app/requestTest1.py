
import requests



url = 'https://pushbear.ftqq.com/sub?sendkey={7147-a3f6a24070355615a1e7a7a837f7ed9d}&text={%E5%93%88%E5%93%88}'

print(url)

jsonStr ={
  "sendkey": "7147-a3f6a24070355615a1e7a7a837f7ed9d",
  "text": "推送测试",
  "desp": "李松的推送测试"
}
response = requests.post(url, data=jsonStr)

print(response.text)

print(response)

