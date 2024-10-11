# coding=utf-8
import numpy as np
import sys
import json
def tts(file,filename):
    
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
        prompt="[speed_4]"
    )

    params_refine_text = ChatTTS.Chat.RefineTextParams(
        temperature=0.3,
                top_P=0.6,
                top_K=23,
                manual_seed=70,
                prompt="[break_2][oral_0][laugh_0]"
    )
    data=json.load(open(file,"r",encoding="utf-8"))
    _texts=data["material"]
    _texts=_texts.split(".")  
    _texts=list(map(lambda str: str.strip()+". ", _texts))
    first=_texts[::3]
    second=_texts[1::3]
    third=_texts[2::3]
    texts=["".join(pair) for pair in zip(first,second,third)]
    if len(_texts)%3==1:
        texts.append(_texts[-1])
    elif len(_texts)%3==2:
        texts.append("".join(_texts[-2:]))
        
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

    from pydub import AudioSegment
    
    sound=AudioSegment.from_file(f"output/listeningpassage/{filename}.wav")
    sound=sound.set_frame_rate(12000)
    sound.export(f"output/listeningpassage/{filename}.mp3", format="mp3", bitrate="128k")    
    
def save_to_sqlite(file,filename):    
    import sqlite3
    data=json.load(open(file,"r",encoding="utf-8"))
    num=3
    
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
    audio=open(f'output/listeningpassage/{filename}.mp3', 'rb').read()
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
    
if __name__ == "__main__":
    prefix="data/listeningpassage"
    filename=sys.argv[1]
    import os
    file=os.path.join(prefix,filename)
    
    # tts(file,filename)
    save_to_sqlite(file,filename)
    
   