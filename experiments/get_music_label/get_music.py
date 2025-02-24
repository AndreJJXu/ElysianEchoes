import json
import matplotlib.pyplot as plt
import numpy
import seaborn as sns
from collections import Counter
import os

music_label_dist = {
    "instrument": {
        "image_title": "Instruments Distribution",
        "image_name": "Instruments Distribution.png",
        "image_xlabel": "Instrument Types",
        "categories": {
            "String Instruments": ["violin", "cello", "guitar", "harp", "bass", "viola", "ukulele", "banjo", "double bass", "fiddle"],
            "Keyboard Instruments": ["piano", "keyboard", "organ", "electric piano", "harpsichord", "clavichord"],
            "Wind Instruments": ["flute", "clarinet", "oboe", "trumpet", "trombone", "saxophone", "horn", "harmonica", "recorder", "bagpipes", "bassoon"],
            "Percussion Instruments": ["drums", "timpani", "tambourine", "triangle", "xylophone", "vibraphone", "marimba", "cymbals", "bell", "bongo", "shakers", "cowbell", "conga", "djembe"],
            "Hybrid Instruments": ["electric guitar", "e-guitar", "electric bass", "keytar", "accordion"],
            "Electronic Instruments": ["synthesizer", "synth", "drum machine", "electronic drums", "theremin", "sampler"]
        },
        "classified_instruments": {
            "String Instruments": set(),
            "Keyboard Instruments": set(),
            "Wind Instruments": set(),
            "Percussion Instruments": set(),
            "Hybrid Instruments": set(),
            "Electronic Instruments": set(),
        }
    },
    "melody": {
        "image_title": "Melody & Rhythm Distribution",
        "image_name": "Melody & Rhythm Distribution.png",
        "image_xlabel": "Melody & Rhythm Types",
        "categories": {
            "Simple": ["Simple Arpeggiated Acoustic Guitar Melody", "Simple Rhythm", "Simple Melody", "Soft Arpeggio", "Simple Bells Melody", "Steady Rhythm", "Easygoing and Relaxing", "Steady Bass Line", "Few Notes", "Minimalist", "Simple Plucked Strings Melody", "Soft Xylophone Melody", "Steady Drumming", "Simple Tune", "Minimal", "Easy Tempo", "Simple Arpegg", "Simple Bass", "Arpeggiated Melody", "Simple High Pitched", "Arpeggiated Cell", "Arpeggiated Harp"],
            "Soft": ["Soft Mellow Sentimental", "Mellow, Soft, Pensive", "Mellow Tune", "Soft, Mellow, Sentimental, Romantic", "Mellow Soft Haunting", "Mellow Synth Pad", "Soft Mellow", "Soft, Mellow, Relaxing", "Soft, Mellow, Ethereal", "Mellow High Hat", "Mellow Bells", "Mellow Tone", "Soft, Relaxing Melody", "Mellow Melody", "Mellow Mood", "Soft Synth", "Soft Melodic", "Soft Piano", "Mellow Chords", "Soft and Emotional", "Soft Release Time", "Soft and Soothing", "Soft Accompaniment", "Soft Melancholic"],
            "Dynamic": ["Melodious Melody", "Uplifting, Background Music", "Melancholic Melody", "Melodic Sounds", "Mellow, Soothing", "Intense Monotone Sound", "Emotional and Passionate", "Soft Mellow Droning", "Fast Tempo", "Melancholic Harmony", "Passionate, Easygoing", "Melancholic Chord Progression", "Melodic Keyboard Harmony", "Intense Harmony", "Melodic Organ Accompaniment", "Repetitive Melody", "Electronic Dance Music", "Synthesiser Arrangements", "Major Chord Progression", "Melancholic Romantic"],
            "Atmospheric": ["Mystical", "Nature Atmosphere", "Calming, Meditative", "Ethereal Sound", "Ambient Nature Sounds", "Oceanic Atmosphere", "Dream-like Atmosphere", "Bizarre and Creepy Atmosphere", "Synth Pad", "Haunting Atmosphere", "Shimmering Melody", "Dreamy Melody", "Background Sound: Rain", "Nature Sounds (Bird Chirping)", "Nature-Inspired", "Soft Mellow Ethereal", "Meditation Music", "Soothing Feel", "Atmospheric Synthesiser", "Crystal Glass Harmony", "Background Bass", "Synthesised Organ Harmony", "Ambient Sound"]
        },
        "classified_instruments": {
            "Simple": set(),
            "Soft": set(),
            "Dynamic": set(),
            "Atmospheric": set(),
        }
    },
    "mood": {
        "image_title": "Mood & Usage Distribution",
        "image_name": "Mood & Usage Distribution.png",
        "image_xlabel": "Mood & Usage Types",
        "categories": {
            "Relaxing": ["Soothing and Uplifting", "Peaceful", "Relaxing, Calming, Easy", "Mellow, Soft, Emotional", "Soothing", "Soft, Melodic", "Spiritual", "Soft Background", "Synthesiser Softness", "Soft, Mellow, Soothing", "Ethereal, Relaxing", "Nature-Inspired", "Relaxing, Calming, Passionate", "Relaxing, Calming, Easygoing", "Soft, Soothing, Relaxing", "Background Sounds", "Soft, Relaxing Melody", "Relaxing, Soothing Mood", "Meditation", "Calming, Meditative", "Meditation Music", "Study Music, Sleeping Music", "Gentle and Uplifting", "Dreamy Atmosphere", "Water Sound Effect", "Rain Sound Effect", "Nature Sounds", "Soft Mellow Sentimental", "Nature Sounds (Bird Chirping)", "Ocean Waves"],
            "Sad": ["Melancholic Harmony", "Melancholic Chord Progression", "Melancholic Mood", "Sad, Emotional, Passionate", "Melancholic Romantic", "Melancholic Melody", "Soft, Mellow, Sentimental, Romantic", "Mellow, Soft, Sentimental, Nostalgic", "Melancholic, Pensive", "Soft Mellow Ethereal", "Soft Piano Chords", "Sad Mood", "Minor Chord Progression", "Melancholic Tone", "Melancholic Piano Melody"],
            "Mysterious": ["Ambiguous Mood", "Bizarre, Creepy Atmosphere", "Otherworldly", "Eerie", "Mystical", "Bizarre", "Mystical, Soft, Mellow, Relaxing", "Haunting Atmosphere", "Spooky, Suspenseful", "Bizarre, Creepy", "Creepy Mood", "Thrilling", "Sinister", "Cold Atmosphere", "Spooky", "Mystical, Calming, Hypnotic"],
            "Uplifting": ["Energetic", "Uplifting, Background Music", "Fast Tempo", "Lively", "Happy and Relaxing", "Gentle and Happy Atmosphere", "Calming, Uplifting", "Uplifting", "Easygoing and Relaxing", "Energetic, Unusual", "Punchy"],
            "Ambient": ["Background Sound", "Layered Sounds", "Study Music", "Ambient Sound", "Fading Sound", "Background Music", "Ambient Nature Sounds", "Atmosphere", "Nature Atmosphere", "Nature Sound", "Background Noise", "Ambient Sounds", "Supporting Role", "Natural Sound Effects", "Ambient Tone"],
            "Emotional": ["Emotional Mood", "Mellow, Sentimental", "Emotional and Passionate", "Sad, Emotional", "Passionate, Easygoing", "Soft, Mellow, Emotional", "Soft, Mellow, Passionate", "Sad, Passionate, Emotional", "Mellow Soft Sentimental"]
        },
        "classified_instruments": {
            "Relaxing": set(),
            "Sad": set(),
            "Mysterious": set(),
            "Uplifting": set(),
            "Ambient": set(),
            "Emotional": set(),
        }
    },
    "style": {
        "image_title": "Music Style Distribution",
        "image_name": "Music Style Distribution.png",
        "image_xlabel": "Music Style Types",
        "categories": {
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
        },
        "classified_instruments": {
            "Electronic": set(),
            "Pop": set(),
            "Classical": set(),
            "Fantasy": set(),
            "Soundtrack": set(),
            "Relaxation Music": set(),
        }
    },
    "timbre": {
        "image_title": "Sound Effects Distribution",
        "image_name": "Sound Effects Distribution.png",
        "image_xlabel": "Sound Effects Types",
        "categories": {
            "Natural": ["Birds Chirping, Ambient Noise", "Water Flowing Sound Effects", "Birds Chirping, Natural Sound Effects", "Nature Sounds (Birds Chirping, River Running)", "Rainfall", "Sea Waves Sound", "Seagull Sound", "Wind Sound", "Splash Effect", "Sounds of nature (birds chirping, river)", "Bird Sound", "Water Flowing", "Birds Chirping, Water Running", "Sound of sea waves", "Birds Singing", "Bird Chirping, Wind Sound", "Birds Chirping, Open Microphone", "Seagulls Chirping", "Water Sound", "Sounds like a music box", "Sounds Relaxing, Calming", "Soft Birds Chirping", "Seagull Chorus", "Wind Chime", "Water Leaking Sound", "Bird Sounds, Natural Sounds", "Cold Water Sound", "Birds Chirping, River Running", "Seabirds Chirping", "Water-drip Sound Effect"],
            "Synthesized": ["Synth pad", "Wide Sustained Synth Pad Tone", "High-Pitched Synth", "Synthesizer Pads", "Atmospheric Synth", "Shimmering Widely Spread Bell", "Ethereal Sound Effects", "Digital Tone", "Synth Arpeggio", "Atmospheric Synthesiser", "Wide Synth Pad Chords", "Synth Bass", "Shimmering Bell", "Synthesizer Pad Sounds", "Long Notes from Harp", "Sustained Synth Bass", "Wide Sustained Synth Pad Chord", "Atmospheric Synth Lead", "Soft Synth Sound", "Reverb, Delay", "Soft Synth Pad Chords", "Tremulous Tone"],
            "Harmony": ["Soft Piano Sound", "Simple Chord Progression", "Intense Harmony", "Reverb, Stereo Imaging", "Tremolo Effect", "Soft Mellow Sentimental Harmony", "Mellow, Soft, Calming", "Wide Sustained Strings", "Intense Droning Harmony", "Sustained Note", "Vigorous Harmony", "Gentle Harmony", "Sine Wave Harmony", "Soft Sub Bass", "Soft Chords", "Soft Harmony", "Wide Chord, Plucked Arpeggiated", "Organ Harmony", "Chord Progression: Major Key", "Melancholic Chord Progression", "High-Pitched Harmony", "Minimalist Melody", "Melodic Harmony", "Shimmering Sound Effects", "Wide Natural Sound Effects"],
            "Melody and Rhythm": ["Sustained High Pitched Melody", "Simple Arpeggio", "Main Melody Sung By Female Voice", "Melody", "High Pitched Lead", "Descending Melody", "Drone Melody", "High-Pitched Melody", "Simple Plucked Strings Melody", "Simple Bass", "Simple Arpeggiated Melody", "Fast Tempo", "Main Tune played by Wind Instrument", "Sustained Melody", "Repetitive Melody", "Lilting Melody", "Melody with High Key", "Main Melody Played by Virtual Harp", "Minimalist Melody", "Melody, Lower Register", "Lower Pitched Melody", "Plucked Melody"],
            "Stereo Field": ["Noisy Recording", "Recording With Phone", "Mono", "Stereo Image", "With Reverb", "Delay", "Echo", "Poor Audio-Quality", "Low Quality Recording", "Filtered Percussion", "Sound Effects: Panning", "Panned Right", "Panned to the Right Side", "Panned Sound", "Low Fidelity"]
        },
        "classified_instruments": {
            "Natural": set(),
            "Synthesized": set(),
            "Harmony": set(),
            "Melody and Rhythm": set(),
            "Stereo Field": set(),
        }
    },
    "performance": {
        "image_title": "Performance Style Distribution",
        "image_name": "Performance Style Distribution.png",
        "image_xlabel": "Performance Style Types",
        "categories": {
            "Instrumental Focus": ["Instrumental", "NME", "Background Music", "No Singer", "No Accompaniment", "Soft Keyboard Harmony", "Wind Instrument", "Cello Accompaniment", "Plucked String Instrument", "Performed by Percussion", "Piano Accompaniment", "No Percussion", "Synthesiser Arrangements", "Organ", "Melodic Cello", "Orchestra", "Theremin", "Xylophone Melody"],
            "Atmospheric": ["Calming", "Relaxing", "Soothing", "Peaceful", "Soft", "Mellow", "Melancholic", "Sentimental", "Sad", "Romantic", "Emotional", "Ethereal", "Meditative", "Hypnotic", "Gentle Atmosphere", "Mystical", "Haunting", "Tragic", "Sombre Mood", "Nostalgic Melancholic Romantic"],
            "Energy": ["Uplifting", "Energetic", "Easygoing", "Soft Mellow Droning", "Higher Register", "Medium Tempo", "Low Pitched", "Slow Tempo", "Simple Melody", "Vibrant", "Upbeat", "Fun", "Groovy"],
            "Ambient": ["Nature Sounds", "Nature-Inspired", "Water Flowing", "Rain", "Birds Chirping", "Breeze Sounds", "Ambient", "Atmospheric", "Natural Environment", "Background Sound", "Chimes", "Rainfall and Water Flowing"]
        },
        "classified_instruments": {
            "Instrumental Focus": set(),
            "Emotional": set(),
            "Energy": set(),
            "Ambient": set(),
        }
    }
}

# 读取JSON文件

# 初始化类别计数
instruments_counter = Counter()

ANS = 'mood'

# 统计每个类别的分布
root_dir = '/mnt/ssd/BeautifulXJJ/AIGC/s2s/ElysianEchoes/datasets'
for foldername in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, foldername)
    
    json_file = os.path.join(folder_path, 'music_label.json')
    with open(json_file, 'r') as file:
        data = json.load(file)
    for key, value in data.items():
        instruments_counter.update([data[key]["Music Labels"]['Instruments Used']])

instruments = instruments_counter
print("\n" * 10, instruments)
print(len(instruments))

categories={music_label_dist[ANS]['categories']}
classified_instruments={music_label_dist[ANS]['classified_instruments']}

# # 定义各类乐器的关键词
# categories = {
#     "String Instruments": ["violin", "cello", "guitar", "harp", "bass", "viola", "ukulele", "banjo", "double bass", "fiddle"],
#     "Keyboard Instruments": ["piano", "keyboard", "organ", "electric piano", "harpsichord", "clavichord"],
#     "Wind Instruments": ["flute", "clarinet", "oboe", "trumpet", "trombone", "saxophone", "horn", "harmonica", "recorder", "bagpipes", "bassoon"],
#     "Percussion Instruments": ["drums", "timpani", "tambourine", "triangle", "xylophone", "vibraphone", "marimba", "cymbals", "bell", "bongo", "shakers", "cowbell", "conga", "djembe"],
#     "Hybrid Instruments": ["electric guitar", "e-guitar", "electric bass", "keytar", "accordion"],
#     "Electronic Instruments": ["synthesizer", "synth", "drum machine", "electronic drums", "theremin", "sampler"]
# }

# # 初始化一个字典来存储分类结果
# classified_instruments = {
#     "String Instruments": set(),
#     "Keyboard Instruments": set(),
#     "Wind Instruments": set(),
#     "Percussion Instruments": set(),
#     "Hybrid Instruments": set(),
#     "Electronic Instruments": set(),
# }


not_instruments = set()
# 分类函数
def classify_instruments(instruments):
    for instrument in instruments:
        flag = 0
        # 将乐器名称转换为小写进行关键词匹配
        instrument_lower = instrument.lower()

        # 遍历每个类别及其关键词
        for category, keywords in categories.items():
            # 如果该乐器包含该类别的关键词，则将其加入该类别中
            if any(keyword in instrument_lower for keyword in keywords):
                classified_instruments[category].add(instrument)
                flag = -1
        if flag == 0:
            not_instruments.add(instrument)
print("\n no used", not_instruments)
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

def plot_and_save_distribution_instrument(labels, values, title, filename):
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

plot_and_save_distribution_instrument(labels=labels, values=values, title=music_label_dist[ANS]['image_title'], filename=music_label_dist[ANS]['image_name'])

