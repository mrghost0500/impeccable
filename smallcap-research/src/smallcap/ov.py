"""Merge Stage 3/4 research overrides into cache/stage3_overrides.json."""
import json, os, sys
PATH = os.path.join(os.path.dirname(__file__), "..", "..", "cache", "stage3_overrides.json")
def merge(new: dict):
    path = os.path.abspath(PATH)
    data = json.load(open(path)) if os.path.exists(path) else {}
    for k, v in new.items():
        data.setdefault(k, {}).update(v)
    json.dump(data, open(path, "w"), indent=1, ensure_ascii=False)
    return len(data)
if __name__ == "__main__":
    print(merge(json.load(sys.stdin)))
