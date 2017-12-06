import urllib3
import json

if __name__ == "__main__":
    http = urllib3.PoolManager()

    # get data
    rGET = http.request("GET", "http://localhost:8101/getques")
    retData = json.loads(rGET.data.decode("utf8"))

    # labeling
    if retData["state"] == 0:
        print("reading success")
        data = retData["data"]
        labeledData = []
        for row in data:
            temp = row
            temp["answer"] = row["zhidaoData"][0]["answer"]
            temp["simques"] = [row["zhidaoData"][0]["simques"], row["zhidaoData"][1]["simques"]]
            temp["diffques"] = [row["zhidaoData"][2]["simques"], row["zhidaoData"][3]["simques"]]
            temp["author"] = "Test"
            labeledData.append(temp)

    # write data
        rPOST = http.request("POST", "http://localhost:8101/writeques", body=json.dumps(labeledData))
        print(rPOST.data.decode("utf8"))

    else:
        print(retData["desc"])
        print("reading failed")
