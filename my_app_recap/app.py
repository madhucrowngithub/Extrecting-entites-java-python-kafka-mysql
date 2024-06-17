from flask import Flask, render_template, request, jsonify
from flask_restx import Api, Resource, fields
from mdc import MDC
import logging
import json
import uuid
import time

import requests
from entities_extraction import getdata
from parse_web_data import extract_text_from_html
# curl -X POST -F "files=@/path/to/file1.html" -F "files=@/path/to/file2.html" http://127.0.0.1:4500/recap/htmlupload
# curl -X POST -F "files=@/Users/madhumr/dokcerpro/index.html" http://127.0.0.1:4500/recap/htmlupload
# curl -X POST -H "Content-Type: application/json" -d '{"urls": ["http://example.com", "http://example2.com"]}' http://127.0.0.1:4500/recap/htmlurl
# curl  -POST 'http://127.0.0.1:4500/recap/request' -d '{"source":"recap","text":"today i travled morethen 65 km in my city"}'




app = Flask(__name__)
api = Api(app, version='1.0', title='Entites Extraction API',
          description='Explore our wonderful user frindly API',
          doc='/recap/doc/'  # The base URL for Swagger UI documentation
          )

ns = api.namespace('API', description='All API operations in one place')

post_model = api.model('PostModel', {
    'source': fields.String(required=True, description='The first source  "recap"'),
    'text': fields.String(required=True, description='the text which you want to reconginze the entities')
})

# @ns.expect(post_model)
@ns.route('/recap/request')
class Resource1(Resource):
    @ns.doc('get_request')
    def get(self):
        """Get a simple message"""
        return {"message": "This is resource 1"}

    
    @ns.expect(post_model)
    @ns.doc('post_request')
    def post(self):
        """Post a simple message"""
        data = request.json

        external_api_url = 'http://127.0.0.1:4500/recap/request'
        try:
            response = requests.get(external_api_url)
            response.raise_for_status()  # Raise an HTTPError on bad status
            data = response.json()
            return {"message": "Success", "data": data}, 200
        except requests.exceptions.RequestException as e:
            return {"message": "Failed to retrieve data", "error": str(e)}, 500
        


@app.route('/recap/request', methods=['POST'])

def process_request():
    
    md = get_uid()
    start_at = time.time()
    resp = do_process_request()
    logging.info(f'got response as: {resp}')
    resp["request_id"] = md
    time_ms = int(1000 * (time.time() - start_at))
    resp["time_taken_ms"] = time_ms
    resp = jsonify(resp)
    resp.headers.add("Access-Control-Allow-Origin", "*")
        
    return resp

@app.route('/recap/htmlupload', methods=['POST'])
def upload_files():
    md = get_uid()
    start_at = time.time()

    files = request.files.getlist('files')
    text_data = ''

    for file in files:
        if file and file.filename.endswith('.html'):
            file_content = file.read()
            text = extract_text_from_html(file_content.decode('utf-8'))
            text_data += text +" "

    resp = do_process_request(text_data)
    resp["request_id"] = md
    time_ms = int(1000 * (time.time() - start_at))
    resp["time_taken_ms"] = time_ms
    resp = jsonify(resp)

    return resp

@app.route('/recap/htmlurl', methods=['POST'])
def process_url():
    md = get_uid()
    start_at = time.time()
    data = request.json
    urls = data.get('urls', [])
    text_data = []
    row_text = ''

    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                text = extract_text_from_html(response.text)
                text_data.append({url: text})
            else:
                text_data.append({url: "Failed"})
        except requests.exceptions.RequestException as e:
            text_data = []
    
    for dictionary in text_data:
        for key, value in dictionary.items():
            if value != 'Failed':
                row_text+= value + " "

    resp = do_process_request(row_text)
    resp["request_id"] = md
    time_ms = int(1000 * (time.time() - start_at))
    resp["time_taken_ms"] = time_ms
    resp = jsonify(resp)

    return resp

    
def do_process_request(text=None):
    data = text
    if data is None:

        json_data = request.get_data()
        obj = json.loads(json_data)
        logging.info(f"obj:{obj}")
        print(obj)
        data = obj.get('text')
    print(f"data sending to model: {data}")
    status, entry = getdata(data)
    logging.info(f"sentence:{data}")
    if status == "SUCCESS":
            res = {'data':  entry, 'status': status, 'code': 200}
    elif status == "FAILURE":
            res = {'status': 'FAILURE', 'code': 500}

    return res


@app.route('/recap/getuid')
def get_uid():
    return(uuid.uuid4().hex)


@app.route('/recap/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=4500,debug=True)

