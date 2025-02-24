import json
import os
from transformers import AutoModelForCausalLM, AutoTokenizer
device = "cuda" # the device to load the model onto

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2-7B-Instruct",
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-7B-Instruct", cache_dir = "/mnt/ssd/BeautifulXJJ/AIGC/s2s/ElysianEchoes/music_caption/llama/ckpt/")

prompt_ori = """
Please analyze the following music descriptions and classify the information into the specified categories. If specific details are not directly mentioned, attempt to infer them based on the context. If inference is not possible, label the category as NME (Not Mentioned or Explicit).

Instruments Used: Identify the instruments mentioned (e.g., Piano, Guitar, Xylophone, Synth, Harp, Electric Guitar, Drums, Violin, Flute, Saxophone).
Music Style: Identify the music style or genre (e.g., Ballad, Electronic Dance Music, Lullaby, Classical, Jazz, Rock, Pop, Christmas Music, Gospel, Blues).
Melody and Rhythm: Describe the melody and rhythm features (e.g., Gentle Melody, Repetitive Melody, Lilting Melody, Solo, Medium Tempo, Fast Tempo, Minor Chord Progression, Simple Melody).
Sound Effects and Timbre: Identify any sound effects or timbre characteristics (e.g., Reverb, Delay, Monotone Sound, Distortion, Echo, Clean Tone, Warm Tone).
Mood and Usage: Describe the mood or suggested use of the music (e.g., Calming, Relaxing, Romantic, Uplifting, Energetic, Background Music, Study Music, Sleeping Music, Christmas Atmosphere, Meditative).
Performance Style: Determine if the piece is instrumental or if it mentions a singer (e.g., Instrumental, No Singer, Vocal).
If any category information is missing or cannot be inferred, please label it as NME.

Example Input:

"This song is a ballad which features a piano playing a gentle melody. The two main instruments are being played by a xylophone and..."

Example Output Format:

Piano, Xylophone; Ballad; Gentle Melody; NME; Calming; Instrumental

请严格保持输出的内容都在我的举例中！
每个大类别都以"; "分割，其余单词之间不需要！
至少5个"; "！！！！

Now process the description:
"""

Instru = ["Piano", "Guitar", "Xylophone", "Synth", "Harp", "Electric Guitar", "Drums", "Violin", "Flute", "Saxophone"]
Styl = ["Ballad", "Electronic Dance Music", "Lullaby", "Classical", "Jazz", "Rock", "Pop", "Christmas Music", "Gospel", "Blues"]
MelRhy = ['Gentle Melody', 'Repetitive Melody', 'Lilting Melody', 'Solo', 'Medium Tempo', 'Fast Tempo', 'Minor Chord Progression', 'Simple Melody']
SoTim = ['Reverb', 'Delay', 'Monotone Sound', 'Distortion', 'Echo', 'Clean Tone', 'Warm Tone']
ModUsg = ['Calming', 'Relaxing', 'Romantic', 'Uplifting', 'Energetic', 'Background Music', 'Study Music', 'Sleeping Music', 'Christmas Atmosphere', 'Meditative']
PerStyl = ['Instrumental', 'No Singer', 'Vocal']
Label_list = [Instru, Styl, MelRhy, SoTim, ModUsg, PerStyl]

root_dir = '/mnt/ssd/BeautifulXJJ/AIGC/s2s/ElysianEchoes/datasets'

# 遍历datasets目录下的所有文件夹
for foldername in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, foldername)
    
    json_file = os.path.join(folder_path, 'musiccaps.json')


    # json_file = "/mnt/ssd/BeautifulXJJ/AIGC/s2s/ElysianEchoes/datasets/瑞士4K景色——翼装飞行视角，FPV放松电影与平静的音乐/musiccaps.json"
    with open(json_file, 'r') as f:
        data = json.load(f)  # 将 JSON 文件内容解析为字典

    # 遍历字典的键值对
    dict = {}
    
    for key, value in data.items():
        try:
            print("now is ", key , value, "*"*50, folder_path)
            now_example = value
            
            prompt = prompt_ori + "'" + now_example[0] + ".'"
            print("now example: ", prompt)
            print("{}"*100)

            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
            text = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            model_inputs = tokenizer([text], return_tensors="pt").to(device)

            generated_ids = model.generate(
                model_inputs.input_ids,
                max_new_tokens=512
            )
            generated_ids = [
                output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
            ]

            response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

            print(response)
            print("-"*50)
            output_list = response.split('; ')
            # print("LEN OF OUTPUT_LIST:", len(output_list))
            # 映射到六个类别
            lab_list = output_list
            # for k in range(6):
            #     flag = 0
            #     for m in range(6):
            #         lists_tmp = Label_list[m]
            #         if output_list[k] in lists_tmp:
            #             lab_list.append(output_list[k])
            #             flag = 1
            #             break
            #     if flag == 0:
            #         lab_list.append("NME")
            # print("LEN OF LABEL:", len(lab_list))
                
            categories = {
                "Instruments Used": lab_list[0],
                "Music Style": lab_list[1],
                "Melody and Rhythm": lab_list[2],
                "Sound Effects and Timbre": lab_list[3],
                "Mood and Usage": lab_list[4],
                "Performance Style": lab_list[5]
            }

            dict[key] = {
                "Music Caption": value[0],
                "Music Labels": categories
            }
            caption_file = os.path.join(folder_path, "music_label.json")
            with open(caption_file, 'w') as f:
                json.dump(dict, f, indent=4)
        except:
            
            continue
        
        # break
    # break
