import os
import librosa
import torch
import torch.nn.functional as F
from models.bart_captioning import BartCaptionModel
import json

checkpoint_path = "/mnt/ssd/BeautifulXJJ/AIGC/s2s/ElysianEchoes/music_caption/best_model/1.6.pt"
cp = torch.load(checkpoint_path)
config = cp["config"]
model = BartCaptionModel(config)
model.load_state_dict(cp["model"])
device = torch.device(config["device"])
model.to(device)

# 定义主目录路径
root_dir = '/mnt/ssd/BeautifulXJJ/AIGC/s2s/ElysianEchoes/datasets'

# 遍历datasets目录下的所有文件夹
for foldername in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, foldername)
    audio_base_path = os.path.join(folder_path, 'audios')
    audio_folder = [
        os.path.join(audio_base_path, audio_path)
        for audio_path in os.listdir(audio_base_path)
    ]
    

    caption_dict = {}
    for i in range(len(audio_folder)):
        audio_path = audio_folder[i]
        waveform, sr = librosa.load(audio_path, sr=16000, mono=True)
        waveform = torch.tensor(waveform)

        if config["audio_encoder_args"]["model_arch"] == "transformer":
            max_length = 16000 * 10
            if len(waveform) > max_length:
                waveform = waveform[:max_length]
            else:
                waveform = F.pad(waveform, [0, max_length - len(waveform)], "constant", 0.0)

        else:
            print("wrong"*10)
            max_length = 32000 * 30
            if len(waveform) > max_length:
                waveform = waveform[:max_length]

        waveform = waveform.unsqueeze(0)

        model.eval()
        with torch.no_grad():
            waveform = waveform.to(device)
            caption = model.generate(samples=waveform, num_beams=3)

        print(caption, " to ", folder_path)
        caption_dict[os.path.basename(audio_path)] = caption

    caption_file = os.path.join(folder_path, 'musiccaps.json')
    with open(caption_file, 'w') as f:
        json.dump(caption_dict, f, indent=4)