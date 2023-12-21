import datetime
import base64
import re
import json

import tornado
import akshare as ak


USERNAME = 'dingtalk'
PASSWORD = 'hello1234'

class NewsCctvHandler(tornado.web.RequestHandler):
    PATTERN = re.compile(r'(\d+)[^\d]+(\d+)[^\d]+(\d+)')
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def get(self):
        if not self.do_auth():
            self.set_status(401)
            self.finish()
            return
        date = self.get_argument('date')
        try:
            date = int(date)
        except:
            year = int(self.PATTERN.search(date).group(1))
            month = int(self.PATTERN.search(date).group(2))
            day = int(self.PATTERN.search(date).group(3))
            date = datetime.date(year, month, day).strftime('%Y%m%d')
        news_cctv_df = ak.news_cctv(date)
        result = json.dumps(json.loads(news_cctv_df.to_json(orient='records')), ensure_ascii=False)
        return self.write(result)

    def do_auth(self):
        api_key = self.request.headers.get('x-api-key')
        if api_key == PASSWORD:
            return True
        api_key = self.get_argument('password', '')
        if api_key == PASSWORD:
            return True
        auth_header = self.request.headers.get('Authorization')
        if not auth_header:
            return False
        auth_items = auth_header.split(' ', 1)
        if len(auth_items) != 2 or auth_items[0] not in ('Basic', 'Bearer'):
            return False
        auth_type, auth_value = auth_items[0], auth_items[1]
        if auth_type == 'Bearer' and auth_value == PASSWORD:
            return True
        auth_decoded = base64.b64decode(auth_value).decode('utf-8')
        userpass = auth_decoded.split(':', 1)
        if len(userpass) == 2 and userpass[0] == USERNAME and userpass[1] == PASSWORD:
            return True
        return False
