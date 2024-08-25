import json
import pickle
import sys


fr = open('./Chess/optimal_policy_1','rb')
estimations = pickle.load(fr)

fr.close()

print(len(estimations))
print(sys.getsizeof(estimations))
# 将字典写入JSON文件
with open('data.json', 'w') as f:
    json.dump(estimations, f)
