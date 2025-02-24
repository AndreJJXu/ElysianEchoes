import json
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import os
# 读取JSON文件


# 初始化类别计数
instruments_counter = Counter()
music_style_counter = Counter()
melody_rhythm_counter = Counter()
sound_effects_counter = Counter()
mood_usage_counter = Counter()
performance_style_counter = Counter()

# 统计每个类别的分布
root_dir = '/mnt/ssd/BeautifulXJJ/AIGC/s2s/ElysianEchoes/datasets'
for foldername in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, foldername)
    
    json_file = os.path.join(folder_path, 'music_label.json')
    with open(json_file, 'r') as file:
        data = json.load(file)
    for key, value in data.items():
        instruments_counter.update([data[key]["Music Labels"]['Instruments Used']])
        # print(data[key]["Music Labels"]['Instruments Used'])
        # break
        music_style_counter.update([data[key]["Music Labels"]['Music Style']])
        melody_rhythm_counter.update([data[key]["Music Labels"]['Melody and Rhythm']])
        sound_effects_counter.update([data[key]["Music Labels"]['Sound Effects and Timbre']])
        mood_usage_counter.update([data[key]["Music Labels"]['Mood and Usage']])
        performance_style_counter.update([data[key]["Music Labels"]['Performance Style']])

instrument = set()

def plot_and_save_distribution(counter, title, filename):
    labels, values = zip(*counter.items())
    # print(labels)
    global instrument
    instrument = instrument | set(labels)
    plt.figure(figsize=(10, 5))
    sns.barplot(x=list(labels), y=list(values))
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(filename)  # 保存图像
    plt.show()

# 绘制并保存六个类别的分布图 
# plot_and_save_distribution(instruments_counter, 'Instruments Distribution', 'instruments_distribution.png')
plot_and_save_distribution(music_style_counter, 'Music Style Distribution', 'music_style_distribution.png')
# plot_and_save_distribution(melody_rhythm_counter, 'Melody & Rhythm Distribution', 'melody_rhythm_distribution.png')
# plot_and_save_distribution(sound_effects_counter, 'Sound Effects Distribution', 'sound_effects_distribution.png')
# plot_and_save_distribution(mood_usage_counter, 'Mood & Usage Distribution', 'mood_usage_distribution.png')
# plot_and_save_distribution(performance_style_counter, 'Performance Style Distribution', 'performance_style_distribution.png')

print("\n" * 10, instrument)
print(len(instrument))
