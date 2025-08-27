import json
import requests
import re
import time
import random

API_BASE = #API_BASE#
API_KEY = #API_KEY#

MODELS = ["gemini-2.5-pro","x-ai/grok-4-07-09","gpt-4o","gemini-2.5-flash", "claude-sonnet-4-20250514" ,"Qwen/Qwen3-235B-A22B-Instruct-2507-FP8" ,"Qwen/Qwen2.5-VL-72B-Instruct"]  # 你可以添加多个模型

def load_dataset(path):
    data = []
    sum = 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line))
            sum+=1
            if sum == 50:
                break
    return data

def query_model(question, options, model_name, max_retries=20, backoff=2):
    prompt = f"请回答下面的多选题，只输出正确选项字母（A/B/C/D），可以多选，不要其他文字：\n问题：{question}\n选项：\n" + "\n".join(options)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 1
    }

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(API_BASE, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            resp_json = response.json()
            content = resp_json["choices"][0]["message"]["content"].upper()
            letters = re.findall(r'[A-D]', content)
            return sorted(list(set(letters)))
        except requests.exceptions.RequestException as e:
            wait_time = backoff + random.random()
            print(f"[{model_name}] 请求失败（尝试 {attempt}/{max_retries}）：{e}，等待 {wait_time:.1f}s 后重试...")
            time.sleep(wait_time)
    print(f"[{model_name}] 多次请求失败，返回空结果 []")
    return []

def evaluate_multi_models(dataset, models, output_file="res.txt"):
    with open(output_file, "w", encoding="utf-8") as f:
        for model_name in models:
            print(f"\n=== Evaluating model: {model_name} ===")
            f.write(f"=== Model: {model_name} ===\n")
            correct = 0
            total = len(dataset)
            
            for i, item in enumerate(dataset, 1):
                pred = query_model(item["question"], item["options"], model_name)
                label_list = item.get("label", [])
                label = sorted(label_list)
                # 多选题判定：预测选项和真实选项完全一致才算对
                if pred == label:
                    correct += 1
                line = f"{i}/{total} | Pred: {pred} | Label: {label}\n"
                f.write(line)
                print(line.strip())
            
            accuracy = correct / total
            acc_line = f"Accuracy: {accuracy:.4f}\n\n"
            f.write(acc_line)
            print(acc_line.strip())

if __name__ == "__main__":
    dataset = load_dataset("jec-qa-kd.jsonl")
    evaluate_multi_models(dataset, MODELS)

