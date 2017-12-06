from mongoDb import mongoDbOperation
from getBaiduZhidao import getQuestion
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging

logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename='server.log',
                            filemode='a')


class Handler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def getMongoData(self, num=100):
        """
        从数据库读数据操作
        :param num: 返回数据条数
        :return: 返回数据
        """
        try:
            ret = self.mongoDbOper.getData(num)
        except Exception:
            self.mongoDbOper = mongoDbOperation()
            ret = self.mongoDbOper.getData(num)
        return ret

    def writeMongoData(self, inputData):
        """
        向数据库写数据操作
        :param inputData: 要写的数据
        :return: 写入结果状态
        """
        try:
            ret = self.mongoDbOper.saveLabeledData(inputData)
        except Exception:
            self.mongoDbOper = mongoDbOperation()
            ret = self.mongoDbOper.saveLabeledData(inputData)
        return ret

    def do_GET(self):
        """
        取问题数据接口, GET, http://xxx.xxx.xxx.xxx:xxxx/getques
        只取一条
        无传入参数
        :return: "state": 0为正常, 1为错误
                 "desc": 状态描述
                 "data": 返回数据, list of dict(目前只取一条), 每一条有q/qid/tags/cate/mongoid 6个字段
                         q: str,问题
                         qid: str,问题的百度id
                         tags: str,问题的标签,','隔开
                         cate: str,问题的分类编号
                         mongoid: str,条目在tempData表中的数据库id
                         zhidaoData: list of dict, [{'simques': 相似问题, 'answer': 相似问题的答案, 'link': 相似问题的链接}, ...]
        """
        try:
            self._set_headers()
            name = self.raw_requestline.decode("utf8").split(" ")[1]
            if name == "/getques":
                # TODO: 增加控制返回数据条数的参数
                data = self.getMongoData(1)
                if data["issuccess"]:
                    question = [row['q'] for row in data["data"]][0]
                    zhidaoData = getQuestion(question)
                    if zhidaoData['issuccess']:
                        temp = data["data"]
                        temp[0]["zhidaoData"] = zhidaoData["data"]
                        response = {"data": temp, "state": 0, "desc": "normal"}
                        self.wfile.write(json.dumps(response).encode("utf8"))
                        logging.info("GET  %s  %s" %(question, response["desc"]))
                    else:
                        response = {"data": [], "state": 1, "desc": "failed in zhidao: %s" % zhidaoData["desc"]}
                        self.wfile.write(json.dumps(response).encode("utf8"))
                        logging.info("GET  %s  %s" % (question, response["desc"]))
                else:
                    response = {"data": [], "state": 1, "desc": "failed to get data in mongodb"}
                    self.wfile.write(json.dumps(response).encode("utf8"))
                    logging.info("GET  %s  %s" % ("no_question", response["desc"]))
            else:
                response = {"data": [], "state": 1, "desc": "wrong interface name"}
                self.wfile.write(json.dumps(response).encode("utf8"))
                logging.info("GET  %s  %s" % ("no_question", response["desc"]))
        except Exception:
            response = {"data": [], "state": 1, "desc": "wrong in http get"}
            self.wfile.write(json.dumps(response).encode("utf8"))
            logging.info("GET  %s  %s" % ("no_question", response["desc"]))

    def do_POST(self):
        """
        写入已标注问题数据接口, POST, http://xxx.xxx.xxx.xxx:xxxx/writeques
        传入参数为要写入的数据labeledData: 要写入的已标注数据,list of dict,
        每一条有q/qid/tags/cate/mongoid/answer/simques/author一共 8个字段
                              q: str,问题
                              qid: str,问题的百度id
                              tags: str,问题的标签,','隔开
                              cate: str,问题的分类编号
                              mongoid: str,条目在tempData表中的数据库id
                              answer: str, 问题回答
                              simques: list of str, 相似问题
                              diffques: list of str, bu相似问题
                              author: str, 作者名
        :return: "state": 0为正常(全部写入成功为正常), 1为错误
                 "desc": 状态描述
                 "wrongcount": 写入错误的个数
        """
        try:
            self._set_headers()
            length = int(self.headers["content-length"])
            post_data = json.loads(self.rfile.read(length).decode("utf8"))
            name = self.raw_requestline.decode("utf8").split(" ")[1]
            if name == "/writeques":
                data = self.writeMongoData(post_data)
                if data["issuccess"]:
                    response = {"wrongcount": data["wrongcount"], "state": 0, "desc": "normal"}
                    self.wfile.write(json.dumps(response).encode("utf8"))
                    logging.info("POST  %s  %d" % (response["desc"], response["wrongcount"]))
                else:
                    response = {"wrongcount": data["wrongcount"], "state": 1, "desc": "failed to write data in mongodb"}
                    self.wfile.write(json.dumps(response).encode("utf8"))
                    logging.info("POST  %s  %d" % (response["desc"], response["wrongcount"]))
            else:
                response = {"wrongcount": -1, "state": 1, "desc": "wrong interface name"}
                self.wfile.write(json.dumps(response).encode("utf8"))
                logging.info("POST  %s  %d" % (response["desc"], response["wrongcount"]))
        except Exception:
            response = {"wrongcount": -1, "state": 1, "desc": "wrong in http post"}
            self.wfile.write(json.dumps(response).encode("utf8"))
            logging.info("POST  %s  %d" % (response["desc"], -1))

    def do_HEAD(self):
        self._set_headers()


def run(ip, port):
    """
    运行
    :param ip: IP
    :param port: 端口
    """
    httpd = HTTPServer((ip, port), Handler)
    try:
        print("server running")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("stop server")
        httpd.server_close()

if __name__ == "__main__":
    run("0.0.0.0", 8101)
