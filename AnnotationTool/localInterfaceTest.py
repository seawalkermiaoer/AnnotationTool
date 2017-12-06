from mongoDb import mongoDbOperation

if __name__ == "__main__":
    mdo = mongoDbOperation()
    retData = mdo.getData()
    print(retData["issuccess"])
    labeledData = []
    for row in retData["data"]:
        temp = row
        temp["answer"] = "test answer"
        temp["simques"] = ["simques 1", "simques 2"]
        labeledData.append(temp)
    writeRes = mdo.saveLabeledData(labeledData)
    print(writeRes)