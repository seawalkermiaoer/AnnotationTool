from pymongo import MongoClient
from bson.objectid import ObjectId

class mongoDbOperation:

    def __init__(self, ip="192.168.59.4", port=27017):
        self.client = MongoClient(ip, port)
        self.db = self.client.questions
        self.tempDataConn = self.db.tempData
        self.labeledDataConn = self.db.labeledData

    def getData(self, dataNum=100):
        """
        从tempData表中取一些数据,并在tempData表中将取出的数据state字段改为1
        :param dataNum: 取数据的个数
        :return: issuccess 操作是否成功
                 data 返回数据,list of dict,每一条有q/qid/tags/cate/mongoid 5个字段
                   q: str,问题
                   qid: str,问题的百度id
                   tags: str,问题的标签,','隔开
                   cate: str,问题的分类编号
                   mongoid: str,条目在tempData表中的数据库id
        """
        try:
            queryData = self.tempDataConn.find({"state": 0}).limit(dataNum)
            retData = []
            for row in queryData:
                retData.append({
                    "q": row["q"],
                    "qid": row["qid"],
                    "tags": row["tags"],
                    "cate": row["cate"],
                    "mongoid": str(row["_id"])
                })
                updateRes = self.tempDataConn.update_one(
                    {"_id": row["_id"]},
                    {
                        "$set": {
                            "state": 1
                        }
                    }
                )
                assert updateRes.modified_count == 1
            assert len(retData) == dataNum
            return {"data": retData, "issuccess": True}
        except Exception:
            return {"data": [], "issuccess":False}

    def saveLabeledData(self, labeledData):
        """
        将已经标注好了的数据写入labeledData数据表,并将写入好的数据在tempData中的对应记录的state字段改为2
        :param labeledData: 要写入的已标注数据,list of dict,每一条有q/qid/tags/cate/mongoid/answer/simques一共8个字段
                              q: str,问题
                              qid: str,问题的百度id
                              tags: str,问题的标签,','隔开
                              cate: str,问题的分类编号
                              mongoid: str,条目在tempData表中的数据库id
                              answer: str, 问题回答
                              simques: list of str, 相似问题
                              author: str, 作者名
        :return: issuccess 操作是否成功
                 wrongcount 错误个数
        """
        wrongCount = 0
        for row in labeledData:
            try:
                self.labeledDataConn.insert_one({
                    "q": row["q"],
                    "qid": row["qid"],
                    "tags": row["tags"],
                    "cate": row["cate"],
                    "answer": row["answer"],
                    "simques": row["simques"],
                    "diffques": row["diffques"],
                    "author": row["author"]
                })
                updateRes = self.tempDataConn.update_one(
                    {"_id": ObjectId(row["mongoid"])},
                    {
                        "$set": {
                            "state": 2
                        }
                    }
                )
                assert updateRes.matched_count == 1
            except Exception:
                wrongCount += 1
        if wrongCount == 0:
            return {"issuccess": True, "wrongcount": wrongCount}
        else:
            return {"issuccess": False, "wrongcount": wrongCount}

    def resetSampleData(self):
        """
        制造一些实验数据
        """
        self.tempDataConn.remove()
        self.labeledDataConn.remove()
        tempData = []
        for row in self.db.zhidao.find().limit(1000):
            tempRow = {
                "q": row["q"],
                "qid": row["qid"],
                "tags": row["tags"],
                "cate": row["cate"],
                "state": 0
            }
            tempData.append(tempRow)
        self.tempDataConn.insert_many(tempData)

if __name__ == "__main__":
    mdo = mongoDbOperation()
    mdo.resetSampleData()
