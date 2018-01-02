from fastcluster import linkage
from scipy.cluster.hierarchy import dendrogram
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import time
from pyltp import Segmentor

raw_data = []
for file_name in os.listdir("../output"):
    with open("../output/" + file_name, "r") as file:
        for row in file:
            try:
                raw_data.append(json.loads(row))
            except Exception:
                print("json decoder error")

seg = Segmentor()
seg.load("/home/houcong/ltp_svr/ltp_data/cws.model")

questions = [" ".join(seg.segment(row["uq"])) for row in raw_data]

# questions = questions[:1000]

tfidf = TfidfVectorizer(tokenizer=lambda x: x.split(" "))
data = tfidf.fit_transform(questions)

print("tf-idf vector length: %d" % data.shape[1])

start_time = time.time()
# data_link = linkage(data.toarray(), method="ward")  #计算
data_link = np.load("data_link.npy")  # 从本地加载
np.save("data_link", data_link)
print("clustering time: %f" % (time.time() - start_time))

# fig1 = plt.figure(figsize=(15, 10))
# dendrogram(data_link)
# fig1.savefig("./dendrogram.jpg")
# fig2 = plt.figure(figsize=(15, 10))
# plt.plot(data_link[:, 2])
# fig2.savefig("./loss.jpg")

stop_point = 2000
cluster_process = data_link[:stop_point, :2]
original_len = data.shape[0]

result = {}
for i in range(original_len):
    result[i] = [i]

for i in range(cluster_process.shape[0]):
    n0 = int(cluster_process[i][0])
    n1 = int(cluster_process[i][1])

    result[original_len + i] = result[n0] + result[n1]

    result.pop(n0)
    result.pop(n1)

final_result = []
for index in result.values():
    final_result.append(raw_data[index[0]])

with open("data_final_version.json", "w") as file:
    file.write("\n".join([json.dumps(row) for row in final_result]))
