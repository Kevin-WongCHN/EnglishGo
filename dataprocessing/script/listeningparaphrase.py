import sys
def tts(texts,prefix="output/listeningparaphrase/"):
    import ChatTTS
    import torch
    import torchaudio
    chat = ChatTTS.Chat()
    chat.load(compile=False)  # Set to True for better performance
    rand_spk = chat.sample_random_speaker()
    params_infer_code = ChatTTS.Chat.InferCodeParams(
        spk_emb=rand_spk,  # add sampled speaker
        temperature=.3,   # using custom temperature
        top_P=0.6,        # top P decode
        top_K=23,         # top K decode
        manual_seed=7,
        prompt="[speed_2]"
    )
    params_refine_text = ChatTTS.Chat.RefineTextParams(
        temperature=0.3,
        top_P=0.6,
        top_K=23,
        manual_seed=70,
        prompt="[break_3][oral_0][laugh_0]"
    )
    texts = list(map(lambda str: str.strip()+"[uv_break]", texts))
    wavs = chat.infer(
        texts,
        params_refine_text=params_refine_text,
        params_infer_code=params_infer_code,
    )
    for index, wav in enumerate(wavs):
        try:
            torchaudio.save(f"{prefix}t{index}.wav", torch.from_numpy(
                wav).unsqueeze(0), 24000)
        except:
            torchaudio.save(f"{prefix}t{index}.wav", torch.from_numpy(wav), 24000)
        from pydub import AudioSegment
        sound=AudioSegment.from_file(f"{prefix}t{index}.wav")
        sound=sound.set_frame_rate(12000)
        sound.export(f"{prefix}t{index}.mp3", format="mp3", bitrate="128k")
        


def save_to_audio(filename):
    import json
    data=json.load(open(filename,"r",encoding="utf-8"))
    texts = [item["question"] for item in data]
    tts(texts)


def save_to_sqlite(num,filename):
    import sqlite3
    import numpy as np
    if(len(sys.argv)>2):
        dbnum=int(sys.argv[2])
    else:
        dbnum=np.random.randint(num)
    conn = sqlite3.connect(f'db/listening/listening{dbnum}.db')
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS listeningparaphrase (
    id INTEGER PRIMARY KEY,
    question TEXT,
    options TEXT,
    answer TEXT,
    audio BLOB
    )
    """
    )
    import json
    data=json.load(open(filename,"r",encoding="utf-8"))
    for index,item in enumerate(data):
        question=item["question"]
        options=item["options"]
        answer=item["answer"]
        audio=open('output/listeningparaphrase/'+ 't'+str(index)+'.mp3', 'rb').read()
        cursor.execute(
            """
            insert into listeningparaphrase(question,options,answer,audio) values(?,?,?,?)
            """
            ,
            (question,json.dumps(options),answer,audio)
        )
    conn.commit()
    with open(os.path.join(prefix,"readme.txt"),"w",encoding="utf-8") as f:
        f.write(filename)


if __name__ == "__main__":
    
    prefix="data/listeningparaphrase"
    filename=sys.argv[1]
    import os
    file=os.path.join(prefix,filename)
    save_to_audio(file)
    num=3
    save_to_sqlite(num,file)
    