# Dataset Schema

All dataset CSV files in `src/datasets/` use the following 17-column schema in this exact order:

| Field | Type | Allowed Values / Notes |
| --- | --- | --- |
| `text` | string | The raw sentence. Keep authentic to the language. |
| `label` | string | `hate`, `non_hate`, `offensive`, `health_issue` |
| `severity` | string | `none`, `mild`, `moderate`, `severe` — use `none` for non_hate rows |
| `is_implicit` | boolean | `true` if hate is coded/indirect (e.g. dog whistle, metaphor). `false` if direct. |
| `is_sarcasm` | boolean | `true` if the sentence uses sarcasm or irony. |
| `target_group` | string | `none`, `gender`, `religion`, `caste`, `nationality`, `race`, `political`, `individual` |
| `target_type` | string | `none`, `individual`, `community`, `ideology` |
| `directness` | string | `none`, `direct`, `indirect`, `systemic` |
| `call_to_action` | boolean | `true` if the text incites action against a group (e.g. "kill them", "remove them"). |
| `tone` | string | `neutral`, `aggressive`, `dismissive`, `sarcastic`, `fearful` |
| `emotion` | string | `none`, `anger`, `disgust`, `fear`, `sadness`, `joy` |
| `profanity_count` | integer | Count of profane/slur words in the sentence (0, 1, 2, etc.) |
| `platform` | string | `social_media`, `news`, `chat`, `political_speech`, `general` |
| `domain` | string | `general`, `political`, `religious`, `sports`, `health`, `education` |
| `region` | string | `india`, `global`, `rural_india`, `urban_india` |
| `confidence` | float | Annotator confidence: `0.70` to `1.00` |
| `annotator_id` | string | `A1` for human-like samples, `synthetic` for AI-generated samples |
