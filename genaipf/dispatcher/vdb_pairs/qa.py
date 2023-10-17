import pandas as pd

vdb_map = {}

qa_jsonl = [
    {"prompt": "Where is Paris?", "completion": "Paris is located in the north-central part of France. Specifically, it is situated in the Île-de-France region. Geographically, it lies along the Seine River. Paris is the capital city of France and is known worldwide for its culture, history, art, and cuisine."},
    {"prompt": "What is the weather like in London?", "completion": "London, being in the southeast of England, has a temperate maritime climate. It experiences mild winters with temperatures usually not falling below freezing and warm summers. Rain is fairly evenly distributed throughout the year, but the city can be particularly rainy in the autumn months. London weather can be unpredictable, and it is not uncommon to experience sun, cloud, and rain all in a single day."},
]

for kv in qa_jsonl:
    vdb_map[kv["prompt"]] = kv["completion"]

