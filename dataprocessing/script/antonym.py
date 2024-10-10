import os
import json
import sys
import sqlite3
prefix="data/antonym"
filename=sys.argv[1]
path=os.path.join(prefix,filename)
data=json.load(open(path,"r",encoding="utf-8"))
db_num=3
import numpy as np
if(len(sys.argv)>2):
    select_db=int(sys.argv[2])
else:
    select_db=np.random.randint(0,db_num)

db=sqlite3.connect(f"db/vocab/vocab{select_db}.db")
cursor=db.cursor()
cursor.execute(
    """
    create table if not exists antonym(
    id INTEGER PRIMARY KEY,
    question TEXT,
    options TEXT,
    answer TEXT
    )
    """
)
for item in data:
    cursor.execute(
        """
        insert into antonym(question,options,answer) values(?,?,?)
        """
        ,
        (item["question"],json.dumps(item["options"]),item["answer"])
    )
db.commit()
db.close()

open(os.path.join(prefix,"readme.txt"),"w").write(filename)
