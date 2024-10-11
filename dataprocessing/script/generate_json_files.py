prefixs=["data/antonym","data/synonym","data/completion","data/gapfilling","data/listeningconversation"
         ,"data/listeningparaphrase","data/listeningpassage","data/readinglong","data/readingshort"]
import os
from_=7
to=50
for prefix in prefixs:
    for i in range(from_,to+1):
        path=os.path.join(prefix,f"z{i}.json")
        with open(path,"w") as f:
            pass