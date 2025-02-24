import json
import matplotlib.pyplot as plt
import numpy
import seaborn as sns
from collections import Counter
import os
# 读取JSON文件

# 初始化类别计数
instruments_counter = Counter()

# 统计每个类别的分布
root_dir = '/mnt/ssd/BeautifulXJJ/AIGC/s2s/ElysianEchoes/datasets'
for foldername in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, foldername)
    
    json_file = os.path.join(folder_path, 'music_label.json')
    with open(json_file, 'r') as file:
        data = json.load(file)
    for key, value in data.items():
        instruments_counter.update([data[key]["Music Labels"]['Sound Effects and Timbre']])

instruments = instruments_counter
print("\n" * 10, instruments)
print(len(instruments))

# 定义各类乐器的关键词
categories = {
    "Natural": ["Birds Chirping, Ambient Noise", "Water Flowing Sound Effects", "Birds Chirping, Natural Sound Effects", "Nature Sounds (Birds Chirping, River Running)", "Rainfall", "Sea Waves Sound", "Seagull Sound", "Wind Sound", "Splash Effect", "Sounds of nature (birds chirping, river)", "Bird Sound", "Water Flowing", "Birds Chirping, Water Running", "Sound of sea waves", "Birds Singing", "Bird Chirping, Wind Sound", "Birds Chirping, Open Microphone", "Seagulls Chirping", "Water Sound", "Sounds like a music box", "Sounds Relaxing, Calming", "Soft Birds Chirping", "Seagull Chorus", "Wind Chime", "Water Leaking Sound", "Bird Sounds, Natural Sounds", "Cold Water Sound", "Birds Chirping, River Running", "Seabirds Chirping", "Water-drip Sound Effect"],
    "Synthesized": ["Synth pad", "Wide Sustained Synth Pad Tone", "High-Pitched Synth", "Synthesizer Pads", "Atmospheric Synth", "Shimmering Widely Spread Bell", "Ethereal Sound Effects", "Digital Tone", "Synth Arpeggio", "Atmospheric Synthesiser", "Wide Synth Pad Chords", "Synth Bass", "Shimmering Bell", "Synthesizer Pad Sounds", "Long Notes from Harp", "Sustained Synth Bass", "Wide Sustained Synth Pad Chord", "Atmospheric Synth Lead", "Soft Synth Sound", "Reverb, Delay", "Soft Synth Pad Chords", "Tremulous Tone"],
    "Harmony": ["Soft Piano Sound", "Simple Chord Progression", "Intense Harmony", "Reverb, Stereo Imaging", "Tremolo Effect", "Soft Mellow Sentimental Harmony", "Mellow, Soft, Calming", "Wide Sustained Strings", "Intense Droning Harmony", "Sustained Note", "Vigorous Harmony", "Gentle Harmony", "Sine Wave Harmony", "Soft Sub Bass", "Soft Chords", "Soft Harmony", "Wide Chord, Plucked Arpeggiated", "Organ Harmony", "Chord Progression: Major Key", "Melancholic Chord Progression", "High-Pitched Harmony", "Minimalist Melody", "Melodic Harmony", "Shimmering Sound Effects", "Wide Natural Sound Effects"],
    "Melody and Rhythm": ["Sustained High Pitched Melody", "Simple Arpeggio", "Main Melody Sung By Female Voice", "Melody", "High Pitched Lead", "Descending Melody", "Drone Melody", "High-Pitched Melody", "Simple Plucked Strings Melody", "Simple Bass", "Simple Arpeggiated Melody", "Fast Tempo", "Main Tune played by Wind Instrument", "Sustained Melody", "Repetitive Melody", "Lilting Melody", "Melody with High Key", "Main Melody Played by Virtual Harp", "Minimalist Melody", "Melody, Lower Register", "Lower Pitched Melody", "Plucked Melody"],
    "Stereo Field": ["Noisy Recording", "Recording With Phone", "Mono", "Stereo Image", "With Reverb", "Delay", "Echo", "Poor Audio-Quality", "Low Quality Recording", "Filtered Percussion", "Sound Effects: Panning", "Panned Right", "Panned to the Right Side", "Panned Sound", "Low Fidelity"]
}


# 初始化一个字典来存储分类结果
classified_instruments = {
    "Natural": set(),
    "Synthesized": set(),
    "Harmony": set(),
    "Melody and Rhythm": set(),
    "Stereo Field": set(),
}


not_instruments = set()
# 分类函数
zzhsum = 0
def classify_instruments(instruments):
    global not_instruments
    global zzhsum
    te = set()
    for instrument in instruments:
        flag = 0
        # 将乐器名称转换为小写进行关键词匹配
        instrument_lower = instrument.lower()

        # 遍历每个类别及其关键词
        for category, keywords in categories.items():
            # 如果该乐器包含该类别的关键词，则将其加入该类别中
            if any(keyword.lower() in instrument_lower for keyword in keywords) or any(instrument_lower in keyword.lower() for keyword in keywords):
                classified_instruments[category].add(instrument)
                if flag == -1:
                    zzhsum +=1
                flag = -1
        if flag == 0:
            # print('zzh', instrument)
            te.add(instrument)
    print("\n no used", te)
    
# 进行分类
classify_instruments(instruments)

labels, values = [], []

# 打印分类结果
for category, instruments in classified_instruments.items():
    sum = 0
    for instrument in instruments:
        sum += instruments_counter[instrument]
    print(f"\n{category}: {sum}")
    labels.append(category.replace(" Instruments", ""))
    values.append(sum)


def plot_and_save_distribution_instrument(title, filename):
    sorted_indices = numpy.argsort(values)[::-1]  # 获取排序索引
    sorted_labels = [labels[i] for i in sorted_indices]
    sorted_values = [values[i] for i in sorted_indices]

    colors = ['#FCE6D5', '#FADBDF', '#F5B7BF', '#ADE5FF', '#D4F4F2', '#C8E5B3']
    bar_width = 0.4

    plt.figure(figsize=(10, 6))
    print(values)
    sorted_values = [int(i) for i in sorted_values]
    # 绘制条形图
    bar_plot = sns.barplot(x=sorted_labels, y=sorted_values, palette=colors, saturation=0.85, ci=None)

    # 添加数据标签
    for p in bar_plot.patches:
        bar_plot.annotate(int(p.get_height()), 
                          (p.get_x() + p.get_width() / 2., p.get_height()), 
                          ha='center', va='bottom', 
                          fontsize=18, color='black')

    # 设置标题和标签
    plt.title(title, fontsize=25, fontweight='bold', color='#0F1423')
    # plt.xlabel('Instrument Types', fontsize=14, color='#0F1423')
    # plt.ylabel('Frequency', fontsize=14, color='#0F1423')
    
    # 美化坐标轴
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    # plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig(filename)  # 保存图像
    plt.show()
plot_and_save_distribution_instrument('Sound Effects Distribution', 'Sound Effects Distribution.png')
print(zzhsum)
