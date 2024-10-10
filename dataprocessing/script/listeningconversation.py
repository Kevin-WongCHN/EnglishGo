def tts(texts):
    import ChatTTS
    chat = ChatTTS.Chat()
    chat.load(compile=False)  # Set to True for better performance
    rand_spk = chat.sample_random_speaker()
    params_infer_code = ChatTTS.Chat.InferCodeParams(
        spk_emb=rand_spk,  # add sampled speaker
        temperature=.3,   # using custom temperature
        top_P=0.6,        # top P decode
        top_K=23,         # top K decode
        manual_seed=7,
        prompt="[speed_3]"
    )
    params_refine_text = ChatTTS.Chat.RefineTextParams(
        temperature=0.3,
        top_P=0.6,
        top_K=23,
        manual_seed=70,
        prompt="[break_1][oral_0][laugh_0]"
    )
    texts = list(map(lambda str: str.strip()+"[uv_break]", texts))
    wavs = chat.infer(
        texts,
        params_refine_text=params_refine_text,
        params_infer_code=params_infer_code,
    )
    return wavs

import json
import sys
prefix="data/listeningconversation"
filename=sys.argv[1]
import os
file=os.path.join(prefix,filename)
data=json.load(open(file,"r",encoding="utf-8"))
odd=data["material"][0::2]
even=data["material"][1::2]

odd_wavs=tts(odd)
even_wavs=tts(even)

wavs=[item for pair in zip(odd_wavs,even_wavs) for item in pair]
if len(odd_wavs)!=len(even_wavs):
    wavs.append(odd_wavs[-1])

import numpy as np
wavs=np.concatenate(wavs, axis=-1)
import torch
import torchaudio
try:
    torchaudio.save(f"output/listeningconversation/{filename}.wav", torch.from_numpy(wavs).unsqueeze(0), 24000)
except:
    torchaudio.save(f"output/listeningconversation/{filename}.wav", torch.from_numpy(wavs), 24000)
    

import sqlite3
num=3
if(len(sys.argv)>2):
    random=int(sys.argv[2])
else:
    random=np.random.randint(num)
db=sqlite3.connect(f"db/listening/listening{random}.db")
cursor=db.cursor()
cursor.execute(
    """
    create table if not exists listeningconversation(
    id INTEGER PRIMARY KEY,
    material TEXT,
    questions TEXT,
    options TEXT,
    answers TEXT,
    explanations TEXT,
    audio BLOB
    )
    """
)
cursor.execute(
    """
    insert into listeningconversation(material,questions,options,answers,explanations,audio) values(?,?,?,?,?,?)
    """,
    (json.dumps(data["material"]),
     json.dumps(data["questions"]),
     json.dumps(data["options"]),
     json.dumps(data["answers"]),
     json.dumps(data["explanations"]),
     open(f"output/listeningconversation/{filename}.wav", 'rb').read()
     )
)
db.commit()
with open(os.path.join(prefix,"readme.txt"),"w",encoding="utf-8") as f:
        f.write(filename)