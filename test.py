from src.pipelines.hindi_pipeline import run_hindi_pipeline
import json

text = "लोकसभा चुनाव 2019 के दौरान रामपुर में एक सभा को संबोधित करते हुए आजम खान ने जिलाधिकारियों (DM) को लेकर विवादास्पद बयान दिया था:"
result = run_hindi_pipeline(text)
print(json.dumps(result, indent=2, ensure_ascii=False))
