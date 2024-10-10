# coding=utf-8
###################################
# Sample a speaker from Gaussian.
def tts(texts,filename):
    
    import ChatTTS
    import torch
    import torchaudio

    chat = ChatTTS.Chat()
    chat.load(compile=False) # Set to True for better performance

    rand_spk = chat.sample_random_speaker()

    params_infer_code = ChatTTS.Chat.InferCodeParams(
        spk_emb = rand_spk, # add sampled speaker 
        temperature = .3,   # using custom temperature
        top_P = 0.6,        # top P decode
        top_K = 23,         # top K decode
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
    
    print(texts)
    wavs = chat.infer(
        texts,
        params_refine_text=params_refine_text,
        params_infer_code=params_infer_code,
    )
    import numpy as np
    final_wavs=np.concatenate(wavs, axis=-1)
    try:
        torchaudio.save(f"output/listeningpassage/{filename}.wav", torch.from_numpy(final_wavs).unsqueeze(0), 24000)
    except:
        torchaudio.save(f"output/listeningpassage/{filename}.wav", torch.from_numpy(final_wavs), 24000)
        
if __name__ == "__main__":
    import sys
    import json
    prefix="data/listeningpassage"
    filename=sys.argv[1]
    import os
    file=os.path.join(prefix,filename)
    data=json.load(open(file,"r",encoding="utf-8"))
    texts=data["material"]
    texts=texts.split(".")  
    texts=list(map(lambda str: str.strip()+". ", texts))
    first=texts[::3]
    second=texts[1::3]
    third=texts[2::3]
    texts_=["".join(pair) for pair in zip(first,second,third)]
    if len(texts)%3==1:
        texts_.append(texts[-1])
    elif len(texts)%3==2:
        texts_.append("".join(texts[-2:]))
    tts(texts_,filename)
    
    import sqlite3
    
    num=3
    import numpy as np
    if(len(sys.argv)>2):
        random=int(sys.argv[2])
    else:
        random=np.random.randint(num)
    db=sqlite3.connect(f"db/listening/listening{random}.db")
    cursor=db.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS listeningpassage (
        id INTEGER PRIMARY KEY,
        material TEXT,
        questions TEXT,
        options TEXT,
        answers TEXT,
        audio BLOB,
        explanations TEXT
        )
        """
    )
 
    material=data["material"]
    questions=data["questions"]
    options=data["options"]
    answers=data["answers"]
    audio=open(f'output/listeningpassage/{filename}.wav', 'rb').read()
    explanations=data["explanations"]
    cursor.execute(
        """
        insert into listeningpassage(material,questions,options,answers,audio,explanations) values(?,?,?,?,?,?)
        """
        ,
        (material,json.dumps(questions),json.dumps(options),json.dumps(answers),audio,json.dumps(explanations))
    )
    open(os.path.join(prefix,"readme.txt"),"w",encoding="utf-8").write(filename)
    db.commit()