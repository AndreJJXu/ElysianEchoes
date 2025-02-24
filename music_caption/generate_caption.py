
import librosa
import torch
import torch.nn.functional as F
from models.bart_captioning import BartCaptionModel
import os
import json
checkpoint_path = "/mnt/ssd/BeautifulXJJ/AIGC/s2s/ElysianEchoes/music_caption/best_model/1.6.pt"
audio_base_path = "/mnt/ssd/BeautifulXJJ/AIGC/s2s/ElysianEchoes/music_caption/music_samples/music/樱花"
audio_folder = [
    os.path.join(audio_base_path, audio_path)
    for audio_path in os.listdir(audio_base_path)
]
# audio_path = "/mnt/ssd/BeautifulXJJ/AIGC/s2s/ElysianEchoes/music_caption/music_samples/music/［4K］ 樱花近景拍摄.wav"
cp = torch.load(checkpoint_path)

config = cp["config"]
model = BartCaptionModel(config)
model.load_state_dict(cp["model"])
device = torch.device(config["device"])
model.to(device)

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
        # print(waveform, waveform.shape)
        caption = model.generate(samples=waveform, num_beams=3)

    print(caption)
    caption_dict[os.path.basename(audio_path)] = caption

caption_file = "/mnt/ssd/BeautifulXJJ/AIGC/s2s/ElysianEchoes/music_caption/music_samples/music/sakura.json"
with open(caption_file, 'w') as f:
    json.dump(caption_dict, f, indent=4)