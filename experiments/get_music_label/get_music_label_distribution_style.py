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
        instruments_counter.update([data[key]["Music Labels"]['Music Style']])

instruments = instruments_counter
print("\n" * 10, instruments)
print(len(instruments))

# 定义各类乐器的关键词
categories = {
    "Electronic": [
        "Electronic", "Dance", "House", "Techno", "Trance", "Dubstep", 
        "Electro", "Ambient", "Glitch Music", "Synthwave", "Synth", 
        "Digital Synth", "Synth Keys", "Synthesised Sounds", "Synthesiser", 
        "Granular Synth", "Acid", "Glitch", "Digital Pluck", "Synth", "Ambient", "Electro"
    ],
    "Pop": [
        "Pop", "Rock", "Hip Hop", "Dance-Pop", "Synth-Pop", "R&B", 
        "Indie Pop", "Advertisement Jingle", "TV Show Theme", 
        "Comedy Music", "Spanish Music", "Mexican Style", 
        "Korean", "Russian", "Chinese Ballad", "Irish Folk Music", 
        "Somali Folk Music", "DJ", "Spanish", "Mexican Storm", "Jingle", "Ad Jingle", "TV Show Advertisement", "Comedy",
        "Spanish", "Mexican Storm", "Jingle", "Ad Jingle", "TV Show Advertisement", "Comedy"
    ],
    "Classical": [
        "Classical Orchestra", "Contemporary Classical", "Baroque", 
        "Romantic", "Chamber Music", "Opera", "Classical", 
        "Traditional Chinese Sounds", "Traditional Chinese", 
        "Traditional Chinese String Instruments", "Traditional Song", "Medieval Music", "Harmonica", "Traditional Song", "Medieval Music", "Harmonica"
    ],
    "Soundtrack": [
        "Film", "Game", "Soundtrack", "Score", "Cinematic", 
        "Trailer Music", "Documentary", "TV Series Theme", 
        "Educational", "Instructional", "Music Style NME", 
        "Narration", "Story-Telling Mood", "Instrumental Showcase", "Movie Music", "Educational", "Instructional", "Instrumental Showcase", "Movie Music", "Educational", "Instructional"
    ],
    "Fantasy": [
        "Fantasy", "New-Age", "Epic", "World Music", "Mythical", 
        "Bird Song", "Dreamy Atmosphere", "Futuristic", "Sci-Fi", 
        "Experimental", "Nature Sounds", "Natural Harmony", 
        "Natural Sound Effects", "Space Sounds", "Atmospheric", "Liquid Sound", "Dreamy", "Bali Music", "Space Sounds", "Atmospheric", "Liquid Sound", "Dreamy", "Bali Music"
    ],
    "Relaxation Music": [
        "Soft", "Soothing", "Sleeping", "Study", "Calm", 
        "Meditative", "Zen", "Relaxing", "Lullaby", "Meditation", 
        "Meditation Music", "Meditation Atmosphere", "Mellow", 
        "Ambient", "Mellow Emotional Song", "Mellow Piano", 
        "Mellow Synth Pad", "Mellow Arpeggiated Harp Melody", 
        "Mellow Instrumental", "Relaxing Music", "Emotional", "Melancholic", "Lullaby", "Slow", "Easy Listening", "Soothing", "Relaxing", "Natural Sounds"
    ]
}


# 初始化一个字典来存储分类结果
classified_instruments = {
    "Electronic": set(),
    "Pop": set(),
    "Classical": set(),
    "Fantasy": set(),
    "Soundtrack": set(),
    "Relaxation Music": set(),
}

zzhsum = 0
not_instruments = set()
# 分类函数
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
                if(flag == -1):
                    zzhsum += 1
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
plot_and_save_distribution_instrument('Music Style Distribution', 'Music Style Distribution.png')

zzh = 0
for i in instruments:
    print(i)
    # zzh += instruments_counter(i)
print(zzh)
labels, values = zip(*instruments_counter.items())
for i in values:
    zzh += i
print(zzh, zzhsum)
