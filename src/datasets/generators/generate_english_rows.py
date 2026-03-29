import csv
import random
import re
from pathlib import Path
from faker import Faker

fake = Faker()
Faker.seed(42)  # reproducibility
random.seed(42)

# ------------------------------------------------------------------
# 1. Load existing texts (to avoid duplicates)
# ------------------------------------------------------------------
existing_texts = set()

# Replace 'your_existing_file.csv' with the actual path to your current dataset
DATASET_PATH = Path(__file__).resolve().parents[1] / "english.csv"
try:
    with open(DATASET_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:  # first column is 'text'
                existing_texts.add(row[0].strip())
    print(f"Loaded {len(existing_texts)} existing sentences.")
except FileNotFoundError:
    print("No existing file found. Starting fresh.")
    existing_texts = set()

# ------------------------------------------------------------------
# 2. Helper functions to generate realistic, sometimes long, vulgar text
# ------------------------------------------------------------------
def random_long_sentence(label, target_group=None, is_sarcastic=False, is_implicit=False):
    """
    Generate a unique, often longer sentence (15-40 words) that matches the label.
    Includes vulgar slang for 'offensive' and 'hate', neutral for others.
    """
    # Templates for each label
    if label == 'hate':
        groups = {
            'gender': ['women', 'men', 'transgender people', 'feminists', 'masculinists'],
            'religion': ['Muslims', 'Christians', 'Hindus', 'Jews', 'Sikhs', 'Buddhists'],
            'caste': ['Dalits', 'Brahmins', 'lower castes', 'upper castes', 'untouchables'],
            'nationality': ['immigrants', 'foreigners', 'refugees', 'Americans', 'Chinese', 'Pakistanis'],
            'race': ['Black people', 'White people', 'Asian people', 'Latinos'],
            'political': ['liberals', 'conservatives', 'socialists', 'nationalists', 'communists'],
            'individual': ['that person', 'this idiot', 'the offender']
        }
        group = target_group if target_group and target_group != 'none' else random.choice(list(groups.keys()))
        group_name = random.choice(groups.get(group, groups['nationality']))
        
        verbs = ['are destroying', 'pollute', 'should be removed', 'bring crime', 'spread disease', 'are vermin', 'must be eliminated']
        if is_implicit:
            verbs = ['are not like us', "don't belong here", 'have different values', 'threaten our way of life']
        
        # Longer sentence with clauses
        templates = [
            f"It is an undeniable fact that {group_name} {random.choice(verbs)} our society from within.",
            f"Every single day, those {group_name} {random.choice(verbs)} and there's nothing we can do about it?",
            f"I've had enough – these {group_name} {random.choice(verbs)} and they should be dealt with immediately.",
            f"History will judge us if we let {group_name} continue to {random.choice(verbs)} without any consequences."
        ]
        sentence = random.choice(templates)
    
    elif label == 'offensive':
        vulgar_terms = ['fucking', 'bloody', 'shitty', 'goddamn', 'pissed', 'crap', 'hell', 'damn']
        intensifiers = ['absolutely', 'totally', 'completely', 'seriously', 'fucking']
        insults = ['idiot', 'moron', 'jerk', 'asshole', 'dipshit', 'motherfucker', 'dumbass']
        templates = [
            f"You are such a {random.choice(vulgar_terms)} {random.choice(insults)}, {random.choice(intensifiers)} clueless!",
            f"What the {random.choice(vulgar_terms)} is wrong with you? Can't you do anything right?",
            f"This {random.choice(vulgar_terms)} mess is your fault, you {random.choice(insults)}.",
            f"I'm so {random.choice(vulgar_terms)} tired of your {random.choice(vulgar_terms)} nonsense, {random.choice(insults)}."
        ]
        sentence = random.choice(templates)
    
    elif label == 'health_issue':
        symptoms = ['sharp pain', 'chronic fatigue', 'dizziness', 'numbness', 'chest tightness', 'swollen joints']
        body = ['back', 'chest', 'head', 'stomach', 'legs', 'neck']
        templates = [
            f"For the past week, I've been experiencing {random.choice(symptoms)} in my {random.choice(body)} that won't go away.",
            f"Every morning I wake up with {random.choice(symptoms)} and it's really starting to worry me.",
            f"After seeing the doctor, they said the {random.choice(symptoms)} in my {random.choice(body)} might be something serious.",
            f"No matter what I do, the {random.choice(symptoms)} persists and I'm losing sleep over it."
        ]
        sentence = random.choice(templates)
    
    else:  # non_hate
        templates = [
            fake.sentence(nb_words=random.randint(12, 25)),
            f"Yesterday, {fake.name()} told me an interesting story about {fake.city()} that lasted almost an hour.",
            f"I've been thinking about {fake.word()} lately and how it affects {random.choice(['people', 'society', 'the environment'])}.",
            f"After a long discussion with {fake.first_name()}, we finally agreed that {fake.sentence(nb_words=8)[:-1]} is the best approach."
        ]
        sentence = random.choice(templates)
    
    # Make sure sentence ends with punctuation and is unique
    sentence = sentence.strip()
    if not sentence.endswith(('.', '!', '?')):
        sentence += '.'
    return sentence

# ------------------------------------------------------------------
# 3. Column value generation respecting dependencies
# ------------------------------------------------------------------
def random_label():
    # Balanced distribution: hate (25%), offensive (25%), health_issue (20%), non_hate (30%)
    return random.choices(
        ['hate', 'offensive', 'health_issue', 'non_hate'],
        weights=[0.25, 0.25, 0.20, 0.30]
    )[0]

def random_severity(label):
    if label == 'non_hate':
        return 'none'
    elif label == 'health_issue':
        return 'none'  # health issues have severity none (per schema)
    else:  # hate or offensive
        return random.choice(['mild', 'moderate', 'severe'])

def random_target_group(label):
    if label == 'hate':
        return random.choice(['gender', 'religion', 'caste', 'nationality', 'race', 'political', 'individual'])
    elif label == 'offensive':
        # offensive often targets individuals, but can be general
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
    if label == 'non_hate' or label == 'health_issue':
        return 'none'
    if is_implicit:
        return 'indirect'
    if target_group == 'none':
        return random.choice(['direct', 'indirect', 'systemic'])
    return random.choice(['direct', 'indirect', 'systemic'])

def random_call_to_action(label, target_group):
    if label != 'hate':
        return False
    # hate speech: ~30% have call to action
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
        if tone == 'joy':
            return 'joy'
        return random.choice(['none', 'joy', 'sadness'])
    # hate/offensive
    if tone == 'sarcastic':
        return 'disgust'
    return random.choice(['anger', 'disgust', 'fear'])

def random_profanity_count(text, label):
    # count common profanities in the generated text
    profane_words = ['fuck', 'shit', 'damn', 'hell', 'crap', 'bloody', 'goddamn', 'bitch', 'asshole', 'motherfucker']
    count = sum(1 for word in re.findall(r'\b\w+\b', text.lower()) if word in profane_words)
    # if label is offensive or hate and count==0, give at least 1
    if label in ('offensive', 'hate') and count == 0:
        count = 1
    return min(count, 5)  # cap at 5

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
    return random.choice(['india', 'global', 'rural_india', 'urban_india'])

def random_confidence():
    return round(random.uniform(0.80, 0.99), 2)

def random_annotator_id():
    # 20% synthetic, 80% human-like (A1..A20)
    if random.random() < 0.2:
        return 'synthetic'
    else:
        return f"A{random.randint(1, 20)}"

# ------------------------------------------------------------------
# 4. Generate 8800 unique rows
# ------------------------------------------------------------------
new_rows = []
target_count = 8800
attempts = 0
max_attempts = 20000

while len(new_rows) < target_count and attempts < max_attempts:
    attempts += 1
    label = random_label()
    is_implicit = False
    is_sarcasm = False
    if label == 'hate':
        is_implicit = random.random() < 0.2   # 20% implicit hate
        is_sarcasm = random.random() < 0.15   # 15% sarcastic hate
    elif label == 'offensive':
        is_sarcasm = random.random() < 0.1
    else:
        is_implicit = False
        is_sarcasm = False

    target_group = random_target_group(label)
    target_type = random_target_type(target_group)
    directness = random_directness(label, is_implicit, target_group)
    call_to_action = random_call_to_action(label, target_group)
    
    # Generate text based on all these attributes
    text = random_long_sentence(label, target_group, is_sarcasm, is_implicit)
    
    # Ensure text is unique and not in existing set
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

print(f"Generated {len(new_rows)} new unique rows after {attempts} attempts.")

# ------------------------------------------------------------------
# 5. Save to CSV
# ------------------------------------------------------------------
output_file = 'extra_8800_rows.csv'
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(new_rows)

print(f"Saved to {output_file}. Now you can append this to your existing dataset.")
