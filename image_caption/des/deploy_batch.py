from PIL import Image
import requests
from transformers import AutoProcessor, LlavaForConditionalGeneration
import torch
from tqdm import tqdm
import os
import json
# # 更改预训练下载位置
# os.environ['TORCH_HOME'] = '/mnt/ssd/BeautifulXJJ/AIGC/s2s/LLaVA_deploy/ckpt/'
with torch.no_grad():
    model = LlavaForConditionalGeneration.from_pretrained("llava-hf/llava-1.5-7b-hf", cache_dir = "/mnt/ssd/BeautifulXJJ/AIGC/s2s/LLaVA_deploy/ckpt/", torch_dtype=torch.bfloat16).cuda()
    processor = AutoProcessor.from_pretrained("llava-hf/llava-1.5-7b-hf" , cache_dir = "/mnt/ssd/BeautifulXJJ/AIGC/s2s/LLaVA_deploy/ckpt/")

    print("load is completed!")
    # prompt = "USER: <image>\nPlease name the instance and \n the bounding boxes of them.\n Then tell details of the blackground and relation between them. ASSISTANT:"
    prompt = "USER: <image>\nPlease tell details of the main instance. ASSISTANT:"
    root_dir = '/mnt/ssd/BeautifulXJJ/AIGC/s2s/ElysianEchoes/datasets'

    # 遍历datasets目录下的所有文件夹
    cnt = 0
    for foldername in os.listdir(root_dir):
        cnt += 1
        if cnt < 3:
            continue
        folder_path = os.path.join(root_dir, foldername)
        imgs_folder_path = os.path.join(folder_path, 'images')
    # imgs_folder_path = "/mnt/ssd/BeautifulXJJ/AIGC/s2s/datasets/vgg_sound/train/select5imgs"
        all_images = os.listdir(imgs_folder_path)
        image_text_dict = {}
        json_file = os.path.join(folder_path, "des.json")
        # for i in range(len(all_images)):
        for i in tqdm(range(0, len(all_images))):
            img_path = os.path.join(imgs_folder_path, all_images[i])
            image = Image.open(img_path)
            inputs = processor(text=prompt, images=image, return_tensors="pt")
            # print("image process completed!")
            for key in inputs:
                inputs[key] = inputs[key].cuda()
            # Generate
            
            generate_ids = model.generate(**inputs, max_new_tokens=1048).cuda()
            # print("waiting for the last code!")
            ans_all = processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
            # input_string = "USER: <image>\nPlease tell details of the main instance. ASSISTANT: This is the main instance."
            prefix = "USER:    Please tell details of the main instance. ASSISTANT:"

            # Remove the prefix
            output_string = ans_all[len(prefix):].strip()
            # print(output_string, "*"*10, ans_all)
            image_text_dict[all_images[i]] = output_string
            image.close()

            # 保存字典为 JSON 文件

            with open(json_file, 'w') as fp:
                json.dump(image_text_dict, fp, indent=4)
