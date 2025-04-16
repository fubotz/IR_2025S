import json

from datasets import Dataset


def save_to_json(dataset, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)


def save_to_jsonl(dataset, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for entry in dataset:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def load_from_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_from_jsonl(path):
    data = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line))
    return data


def convert_to_hf_dataset(data):
    return Dataset.from_list(data)
