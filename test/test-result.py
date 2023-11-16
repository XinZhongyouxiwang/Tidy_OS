from urllib.request import urlopen

try:
    resp = urlopen('https://github.com')
except Exception as e:
    print('Unable to link to github')
    exit()
if resp.getcode() == 200:
    print('success')