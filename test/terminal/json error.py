import json

file = open('./test-json_error.json', 'r')
content: dict = json.loads(file.read())
file.close()
