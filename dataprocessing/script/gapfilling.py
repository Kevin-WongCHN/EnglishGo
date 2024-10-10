import os
import json
import sys
import sqlite3
prefix="data/gapfilling"
filename=sys.argv[1]
path=os.path.join(prefix,filename)
data=json.load(open(path,"r",encoding="utf-8"))
db_num=3
import numpy as np
if(len(sys.argv)>2):
    select_db=int(sys.argv[2])
else:
    select_db=np.random.randint(0,db_num)
db=sqlite3.connect(f"db/gapfilling/gapfilling{select_db}.db")
cursor=db.cursor()
cursor.execute(
    """
    create table if not exists gapfilling(
    id INTEGER PRIMARY KEY,
    material TEXT,
    options TEXT,
    answers TEXT,
    explanations TEXT
    )
    """
)

cursor.execute(
    """
    insert into gapfilling(material,options,answers,explanations) values(?,?,?,?)
    """
    ,
    (data["material"],json.dumps(data["options"]),json.dumps(data["answers"]),json.dumps(data["explanations"]))
)
db.commit()
db.close()

open(os.path.join(prefix,"readme.txt"),"w").write(filename)
