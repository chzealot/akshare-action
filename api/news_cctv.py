import tornado
import akshare as ak


class NewsCctvHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def get(self):
        date = self.get_argument('date')
        news_cctv_df = ak.news_cctv(date)
        return self.write(news_cctv_df.to_json(orient='records'))
