import csv
import random
import re
from pathlib import Path
from faker import Faker

fake = Faker('hi_IN')  # Hindi locale
Faker.seed(42)
random.seed(42)

# ------------------------------------------------------------------
# 1. Load existing Hindi texts (to avoid duplicates)
# ------------------------------------------------------------------
existing_texts = set()

# Change this to your actual Hindi CSV file name
hindi_csv_file = Path(__file__).resolve().parents[1] / "hindi.csv"

try:
    with open(hindi_csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                existing_texts.add(row[0].strip())
    print(f"Loaded {len(existing_texts)} existing Hindi sentences.")
except FileNotFoundError:
    print("No existing Hindi file found. Starting fresh.")
    existing_texts = set()

# ------------------------------------------------------------------
# 2. Helper functions to generate Hindi sentences
# ------------------------------------------------------------------
def random_hindi_sentence(label, target_group=None, is_sarcastic=False, is_implicit=False):
    """Generate a unique Hindi sentence matching the label."""
    
    if label == 'hate':
        # Target groups and their Hindi names
        groups = {
            'gender': ['औरतें', 'महिलाएं', 'लड़कियां', 'पुरुष', 'मर्द', 'ट्रांसजेंडर'],
            'religion': ['मुसलमान', 'हिंदू', 'सिख', 'ईसाई', 'जैन', 'बौद्ध', 'यहूदी'],
            'caste': ['दलित', 'ब्राह्मण', 'क्षत्रिय', 'वैश्य', 'शूद्र', 'अछूत', 'ओबीसी'],
            'nationality': ['बिहारी', 'पंजाबी', 'दक्षिण भारतीय', 'उत्तर प्रदेशी', 'बंगाली', 'गुजराती', 'राजस्थानी'],
            'political': ['कांग्रेसी', 'भाजपाई', 'कम्युनिस्ट', 'आरक्षण समर्थक'],
            'individual': ['वह आदमी', 'यह बेवकूफ', 'तुम जैसे लोग']
        }
        group = target_group if target_group and target_group != 'none' else random.choice(list(groups.keys()))
        group_name = random.choice(groups.get(group, groups['nationality']))
        
        # Hate verbs/phrases
        verbs = ['समाज का नाश कर रहे हैं', 'गंदगी फैलाते हैं', 'अपराध करते हैं', 'बीमारी फैलाते हैं', 'बदमाश हैं', 'हटाए जाने चाहिए']
        if is_implicit:
            verbs = ['हमारी तरह नहीं हैं', 'हमारे मूल्यों के खिलाफ हैं', 'हमारी संस्कृति को खतरा हैं', 'भरोसे के लायक नहीं हैं']
        
        templates = [
            f"यह सच है कि {group_name} {random.choice(verbs)}।",
            f"हर रोज़ ये {group_name} {random.choice(verbs)} और कोई कुछ नहीं करता।",
            f"मैं थक गया हूँ – ये {group_name} {random.choice(verbs)}, इनका सफाया होना चाहिए।",
            f"इतिहास हमें दोषी ठहराएगा अगर हमने {group_name} को {random.choice(verbs)} दिया।"
        ]
        sentence = random.choice(templates)
    
    elif label == 'offensive':
        vulgar_terms = ['बकवास', 'चूतिया', 'हरामी', 'भोसड़ीके', 'मादरचोद', 'साला', 'कुत्ता', 'सुअर', 'गधा']
        intensifiers = ['बिल्कुल', 'पूरी तरह', 'सच में', 'कमबख्त']
        insults = ['बेवकूफ', 'नालायक', 'औकातहीन', 'गंदा कीड़ा', 'हरामजादा']
        templates = [
            f"तुम {random.choice(vulgar_terms)} {random.choice(insults)} हो, {random.choice(intensifiers)} बेहूदा!",
            f"ये क्या {random.choice(vulgar_terms)} चल रहा है? कुछ भी सही नहीं कर सकते?",
            f"यह {random.choice(vulgar_terms)} तुम्हारी वजह से है, {random.choice(insults)}।",
            f"मैं {random.choice(vulgar_terms)} थक गया हूँ तुम्हारे {random.choice(vulgar_terms)} नखरे से, {random.choice(insults)}।"
        ]
        sentence = random.choice(templates)
    
    elif label == 'health_issue':
        symptoms = ['तीखा दर्द', 'लगातार थकान', 'चक्कर', 'सुन्नपन', 'सीने में जकड़न', 'जोड़ों में सूजन', 'पीठ दर्द', 'गर्दन दर्द']
        body_parts = ['कमर', 'सीने', 'सिर', 'पेट', 'पैर', 'गले']
        templates = [
            f"पिछले एक हफ्ते से {random.choice(symptoms)} हो रहा है {random.choice(body_parts)} में, जो जा ही नहीं रहा।",
            f"हर सुबह उठते ही {random.choice(symptoms)} होता है, अब बहुत परेशान कर दिया है।",
            f"डॉक्टर ने कहा कि {random.choice(body_parts)} का {random.choice(symptoms)} गंभीर हो सकता है।",
            f"मैं कुछ भी करूँ, {random.choice(symptoms)} बना रहता है और नींद उड़ गई है।"
        ]
        sentence = random.choice(templates)
    
    else:  # non_hate – use Faker for natural Hindi sentences
        templates = [
            fake.sentence(nb_words=random.randint(10, 20)),
            f"कल, {fake.name()} ने {fake.city()} के बारे में एक दिलचस्प कहानी सुनाई जो लगभग एक घंटे तक चली।",
            f"मैं {fake.word()} के बारे में सोच रहा था और यह {random.choice(['लोगों', 'समाज', 'पर्यावरण'])} को कैसे प्रभावित करता है।",
            f"{fake.first_name()} के साथ लंबी बहस के बाद हम इस नतीजे पर पहुंचे कि {fake.sentence(nb_words=8)[:-1]} सबसे अच्छा तरीका है।"
        ]
        sentence = random.choice(templates)
    
    sentence = sentence.strip()
    if not sentence.endswith(('.', '!', '?')):
        sentence += '.'
    return sentence

# ------------------------------------------------------------------
# 3. Column value generation (same logic as English, but adapted)
# ------------------------------------------------------------------
def random_label():
    return random.choices(
        ['hate', 'offensive', 'health_issue', 'non_hate'],
        weights=[0.25, 0.25, 0.20, 0.30]
    )[0]

def random_severity(label):
    if label in ('non_hate', 'health_issue'):
        return 'none'
    return random.choice(['mild', 'moderate', 'severe'])

def random_target_group(label):
    if label == 'hate':
        return random.choice(['gender', 'religion', 'caste', 'nationality', 'political', 'individual'])
    elif label == 'offensive':
        return random.choices(['individual', 'none'], weights=[0.7, 0.3])[0]
    else:
        return 'none'

def random_target_type(target_group):
    if target_group == 'individual':
        return 'individual'
    elif target_group == 'none':
        return 'none'
    else:
        return random.choice(['community', 'ideology'])

def random_directness(label, is_implicit, target_group):
    if label in ('non_hate', 'health_issue'):
        return 'none'
    if is_implicit:
        return 'indirect'
    return random.choice(['direct', 'indirect', 'systemic'])

def random_call_to_action(label):
    if label != 'hate':
        return False
    return random.random() < 0.3

def random_tone(label, is_sarcasm):
    if is_sarcasm:
        return 'sarcastic'
    if label == 'hate':
        return random.choice(['aggressive', 'dismissive', 'fearful'])
    elif label == 'offensive':
        return random.choice(['aggressive', 'dismissive'])
    elif label == 'health_issue':
        return random.choice(['neutral', 'fearful'])
    else:
        return random.choice(['neutral', 'joy', 'sadness'])

def random_emotion(label, tone):
    if label == 'health_issue':
        return random.choice(['fear', 'sadness', 'pain', 'none'])
    if label == 'non_hate':
        return 'joy' if tone == 'joy' else random.choice(['none', 'joy', 'sadness'])
    if tone == 'sarcastic':
        return 'disgust'
    return random.choice(['anger', 'disgust', 'fear'])

def random_profanity_count(text, label):
    profane_hindi = ['चूतिया', 'हरामी', 'भोसड़ी', 'मादरचोद', 'साला', 'बकवास', 'कुत्ता', 'सुअर', 'गधा', 'हरामजादा', 'बहनचोद']
    count = sum(1 for word in re.findall(r'[\u0900-\u097F]+', text) if word in profane_hindi)
    if label in ('offensive', 'hate') and count == 0:
        count = 1
    return min(count, 5)

def random_platform():
    return random.choice(['social_media', 'news', 'chat', 'political_speech', 'general'])

def random_domain(label):
    if label == 'health_issue':
        return 'health'
    elif label == 'hate':
        return random.choices(['general', 'political', 'religious', 'sports'], weights=[0.4, 0.4, 0.15, 0.05])[0]
    else:
        return random.choice(['general', 'political', 'religious', 'sports', 'health', 'education'])

def random_region():
    # Hindi dataset primarily India-focused
    return random.choice(['india', 'rural_india', 'urban_india'])

def random_confidence():
    return round(random.uniform(0.80, 0.99), 2)

def random_annotator_id():
    return 'synthetic' if random.random() < 0.2 else f"A{random.randint(1,20)}"

# ------------------------------------------------------------------
# 4. Generate unique rows (target 8800, adjust as needed)
# ------------------------------------------------------------------
new_rows = []
target_count = 8800
attempts = 0
max_attempts = 25000

while len(new_rows) < target_count and attempts < max_attempts:
    attempts += 1
    label = random_label()
    is_implicit = False
    is_sarcasm = False
    if label == 'hate':
        is_implicit = random.random() < 0.2
        is_sarcasm = random.random() < 0.15
    elif label == 'offensive':
        is_sarcasm = random.random() < 0.1

    target_group = random_target_group(label)
    target_type = random_target_type(target_group)
    directness = random_directness(label, is_implicit, target_group)
    call_to_action = random_call_to_action(label)
    
    text = random_hindi_sentence(label, target_group, is_sarcasm, is_implicit)
    
    # Uniqueness check
    if text in existing_texts or any(row[0] == text for row in new_rows):
        continue
    
    severity = random_severity(label)
    tone = random_tone(label, is_sarcasm)
    emotion = random_emotion(label, tone)
    profanity_count = random_profanity_count(text, label)
    platform = random_platform()
    domain = random_domain(label)
    region = random_region()
    confidence = random_confidence()
    annotator_id = random_annotator_id()
    
    new_rows.append([
        text, label, severity, str(is_implicit).lower(), str(is_sarcasm).lower(),
        target_group, target_type, directness, str(call_to_action).lower(),
        tone, emotion, profanity_count, platform, domain, region, confidence, annotator_id
    ])

print(f"Generated {len(new_rows)} new unique Hindi rows after {attempts} attempts.")

# ------------------------------------------------------------------
# 5. Save to CSV
# ------------------------------------------------------------------
output_file = 'extra_hindi_rows.csv'
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(new_rows)

print(f"Saved to {output_file}. Append to your existing Hindi dataset.")
