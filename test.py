import json

import requests

# data = {
#     'dept_no': 'd009',
#     'dept_name': 'cyx'
# }
# json_data=json.dumps(data)
# url = 'http://127.0.0.1:5000/api/v1/departments'
# headers = {'Content-type': 'application/json'}
# requests.put(url, data=json_data, headers=headers)
# url = 'http://127.0.0.1:5000/api/v1/departments/d009'
# requests.delete(url)
url = 'http://127.0.0.1:5000/api/v1/employees/10001'
print(requests.get(url))
