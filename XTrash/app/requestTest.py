
import requests

appid ='wx99ba17c0da954a2e'
secret ='65de82af8ed4e280e619ea62bc79640c'

js_code = '061nh0rR0ihYK827HXtR0iJ9rR0nh0rT'

url = 'https://api.weixin.qq.com/sns/oauth2/access_token'

url = 'https://api.weixin.qq.com/sns/jscode2session'


base_url= url+'?appid=' + appid + '&secret=' + secret + '&js_code=' + js_code +'&code=' + js_code + '&grant_type=authorization_code'

#base_url = 'https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code'

print(base_url)
rep = requests.get(base_url)

print(rep)
print(rep.text)




#https://api.weixin.qq.com/sns/jscode2session?appid=wx99ba17c0da954a2e&secret=65de82af8ed4e280e619ea62bc79640c&js_code=061nh0rR0ihYK827HXtR0iJ9rR0nh0rT&code=061nh0rR0ihYK827HXtR0iJ9rR0nh0rT&grant_type=authorization_code
#<Response [200]>
#{"session_key":"qRNbM8mjHxXjpjJIS98p1g==","openid":"oGKmW5EYq3eRiY0APacfWxukTP2s"}