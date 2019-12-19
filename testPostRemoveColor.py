import requests

url = 'http://localhost:5555/removeColor'
data = {
    'path': 'C:\\Users\\Administrator\\Desktop\\test\\source.pdf',
    'outpath': '',
    'zoomNum': '',
    'compressNum': '',
}
response = requests.post(url, data=data)
print(response.text)