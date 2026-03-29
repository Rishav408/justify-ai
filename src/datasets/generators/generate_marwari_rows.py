import csv
import random
import re
from pathlib import Path

random.seed(42)

# ------------------------------------------------------------------
# 1. Load existing Marwari texts (to avoid duplicates)
# ------------------------------------------------------------------
existing_texts = set()
marwari_csv_file = Path(__file__).resolve().parents[1] / "marwari.csv"

try:
    with open(marwari_csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                existing_texts.add(row[0].strip())
    print(f"Loaded {len(existing_texts)} existing Marwari sentences.")
except FileNotFoundError:
    print("No existing Marwari file found. Starting fresh.")
    existing_texts = set()

# ------------------------------------------------------------------
# 2. Marwari vulgar word list (for profanity count)
# ------------------------------------------------------------------
PROFANE_MARWARI = [
    'चुतिया', 'हरामी', 'भोसड़ी', 'भोसड़ीके', 'मादरचोद', 'बहनचोद', 'साला',
    'कुत्तो', 'सुअर', 'गधो', 'लफंगो', 'गुंडो', 'नालायक', 'बेइज्जत',
    'हरामजादो', 'चरसी', 'भंगी', 'ठग', 'बोक्या', 'भाडखाऊ', 'चोर',
    'लुच्चो', 'पाजी', 'खोटो', 'बदमाश', 'ढूंढ़ो', 'हरामखोर'
]

# ------------------------------------------------------------------
# 3. Expanded Marwari sentence generators
# ------------------------------------------------------------------

# ----- Non-hate: 120 everyday Marwari sentences -----
NON_HATE_MARWARI = [
    "आज म्हे खेत में बाजरो बोयो।",
    "गाँव मां भोजणो रो कार्यक्रम थियो।",
    "बकरी रो बच्चो जणम्यो।",
    "म्हे अपणा भाई सै बाजार गया।",
    "चिट्ठी आई है, बेटा री।",
    "म्हे सब मिलकर होली खेली।",
    "भाई नै नई मोटरसाइकिल लीधी।",
    "म्हारा गेहूँ री फसल अच्छी थी।",
    "नणंद री ब्याह मां बड़ी भीड़ थी।",
    "पूजा रे बाद प्रसाद बांटियो।",
    "आज पहली बारसात थी।",
    "माई रे बगीचे मां फूल खिल्या।",
    "गाँव रे मंदिर मां भजन थियो।",
    "स्कूल मां बच्चां रो सालाणो समारोह थियो।",
    "बैलगाड़ी मां गोबर भरियो।",
    "हळदीकुंकू मां सगळी औरतां आई।",
    "नई पीढ़ी खेती छोड़ दीधी है।",
    "बेटी रो नामकरण धूमधाम सै करयो।",
    "बाबोजी किस्से सुणावै।",
    "माई दूधभात खवायो।",
    "खेत मां गन्नो री कटाई चलै है।",
    "गाँव रो जवान मुंबई नौकरी करण गयो।",
    "बैल नै पाणी पियायो।",
    "गाय रो बछड़ो दौड़ै।",
    "मुर्गी अंडो देती है।",
    "पड़ोसण रे पैसे वापस मिलग्या।",
    "म्हारो साखरपेटो है।",
    "भाई दूज पै बहन नै टीको लगायो।",
    "दिवाली मां फराल बणायो।",
    "सड़क पै गढ्ढा होग्यो है।",
    "पंचायत मां नयो फैसलो थियो।",
    "स्कूल मां छुट्टी लागगी।",
    "लड़को पैरीक्षा मां पहिलो आयो।",
    "घरवाली नै मीठो दही बणायो।",
    "सासूजी नै बुखार आयो थो।",
    "जवाई गाँव आयो।",
    "मामा रे घर मामेरो आयो।",
    "सहेली री ब्याह मां गई।",
    "भाजी ताजी थी।",
    "दूध गरम करयो।",
    "आंगण मां गेंदा फुल्यो।",
    "घर रे सामने आम रो पेड़ है।",
    "नदी मां पाणी चढ़ग्यो।",
    "गुरुजी नै पढ़ायो।",
    "स्कूल मां संगीत रो क्लास थियो।",
    "गाँव मां मेलो लाग्यो।",
    "हाथगाड़ी सै गेहूं ढोलियो।",
    "कुओं सूखग्यो।",
    "पंप सै खेत मां पाणी दियो।",
    "बैल जोत लीधी।",
    "हँसिये सै घास काटी।",
    "घर री छाण डाली।",
    "चूल्हे पै रोटी सेकी।",
    "तवे पै पूड़ी बणी।",
    "मधु मां मक्खी फँसी।",
    "चींटी रेंगै।",
    "पंछी रो घोंसलो पेड़ पै है।",
    "हवा सै दरवाजो खुलग्यो।",
    "बादळ गरज्या।",
    "बिजळी चमकी।",
    "बारसात थमगी।",
    "सड़क कीचड़ होगी।",
    "साँझ पै ओस पड़ी।",
    "सूरज डूबग्यो।",
    "चाँद निकल्यो।",
    "तारा चमक्या।",
    "रात मां कुत्तो भोंक्यो।",
    "बिल्ली चूहो पकड़ै।",
    "गधो रेंक्यो।",
    "भैंस रो बछड़ो थियो।",
    "बकरी रो दूध मीठो होवै।",
    "घी गरम करयो।",
    "छाछ पीयो।",
    "मठ्ठो खायो।",
    "पापड़ सुखाया।",
    "कुरडी बणाई।",
    "खेत मां मक्को पक्यो।",
    "चणो फुल्यो।",
    "हल्दी री गांठ काढ़ी।",
    "मिर्च सुखाई।",
    "धणियो उखाड़यो।",
    "बारीक मसालो मिलायो।",
    "खट्टी चटणी बणाई।",
    "ठंडाई ठंडी करी।",
    "श्रीखंड बणायो।",
    "पूरनपोळी बणाई।",
    "आमरस बणायो।",
    "भाकरी तयार थी।",
    "तरकारी तळी।",
    "कढ़ी बणाई।",
    "वरण बणायो।",
    "चावळ पक्या।",
    "दही जमायो।",
    "घी पिघल्यो।",
    "शक्कर पायी।",
    "नमक पायो।",
    "अचार काढ्यो।",
    "साँझे दियो बाल्यो।",
    "नीरांजण ओळम्यो।",
    "आरती करी।",
    "प्रार्थना करी।",
    "गीता पढ़ी।",
    "मंदिर मां घंटो बज्यो।",
    "पुजारी नै मंत्र पढ़्या।",
    "पालकी निकली।",
    "झंडो चढ़ायो।",
    "रथ चल्यो।",
    "भजन मंडळी गावै।",
    "कीर्तन थियो।",
    "हरिनाम सप्ताह चलै।",
    "व्रत राख्यो।",
    "उपवास राख्यो।",
    "फळ खाया।",
    "पाणी पीयो।",
    "तीरथ जाणो है।",
    "पंढरपुर री वारी चलै है।",
    "नाशिक मां स्नान करयो।",
    "त्र्यंबकेश्वर मां पूजा करी।",
    "शिर्डी मां साईं रे दर्शन कर्या।",
    "तुलसी मां पाणी घाल्यो।",
    "बेल रे पेड़ पै दूध चढ़ायो।",
    "दीपक प्रज्वलित करयो।",
]

# ----- Hate templates (expanded) -----
# Direct hate templates (index 0-9)
HATE_TEMPLATES_DIRECT = [
    "{group} {verb} अर उनखा बाहर काढणो जरूरी है।",
    "{group} समाज रो कैंसर है, उनखो नाश करो।",
    "म्हे नई मानूं कि {group} नै हक मिलणा चाहिये, वो खतरनाक है।",
    "{group} हमारी संस्कृति बरबाद कर दी है।",
    "जबलक {group} है तबलक शांति नई हो सकती।",
    "{group} री जड़ सै उखाड़ फेकणी चाहिये।",
    "{group} नै देश सै निकाल दो, ये निकम्मा है।",
    "{group} खून रे खेल कर्या है, आब बदलो लेवो।",
    "{group} जानवर जैसा है, उनखा अलग राखो।",
    "{group} ज़हर फैलावै है, उनखा अलग करो।",
]

# Implicit hate templates (index 10-14)
HATE_TEMPLATES_IMPLICIT = [
    "{group} रे बारे मां अलग सोचणो पड़ैगा।",
    "{group} कधी हमारा जैसा नई हो सकता।",
    "{group} री कीमत हमारा सै मेल नई खाती।",
    "अपणा बच्चां नै {group} सै बचाओ।",
    "{group} पै भरोसो मत करो।",
]

def random_marwari_sentence(label, target_group=None, is_sarcastic=False, is_implicit=False):
    if label == 'hate':
        groups = {
            'gender': ['औरतें', 'महिलाएं', 'लड़कियां', 'मरद', 'लड़का', 'ट्रांसजेंडर'],
            'religion': ['मुसलमान', 'हिंदू', 'सिख', 'ईसाई', 'जैन', 'बौद्ध', 'यहूदी'],
            'caste': ['दलित', 'ब्राह्मण', 'क्षत्रिय', 'वैश्य', 'शूद्र', 'अछूत', 'यादव', 'कुर्मी', 'मारवाड़ी'],
            'nationality': ['बिहारी', 'पंजाबी', 'दक्खिनी', 'उत्तर प्रदेशी', 'बंगाली', 'गुजराती'],
            'political': ['कांग्रेसी', 'भाजपाई', 'कम्युनिस्ट', 'आरक्षण वाला'],
            'individual': ['वो आदमी', 'यो बेवकूफ', 'तोरा जैसा']
        }
        group = target_group if target_group and target_group != 'none' else random.choice(list(groups.keys()))
        group_name = random.choice(groups.get(group, groups['nationality']))
        
        verbs = ['समाज बिगाड़ै है', 'गंदगी फैलावै है', 'अपराध करै है', 'बीमारी फैलावै है', 'बदमाश है', 'हटावणो चाहिये']
        if is_implicit:
            verbs = ['हमारा जैसा नई है', 'हमारी रीति रे खिलाफ है', 'हमारी संस्कृति नै खतरो है', 'भरोसे लायक नई है']
        
        if is_implicit:
            chosen_template = random.choice(HATE_TEMPLATES_IMPLICIT)
        else:
            chosen_template = random.choice(HATE_TEMPLATES_DIRECT)
        
        sentence = chosen_template.format(group=group_name, verb=random.choice(verbs))
        if not sentence.endswith(('.', '!', '?')):
            sentence += '.'
        return sentence
    
    elif label == 'offensive':
        vulgar_terms = PROFANE_MARWARI
        intensifiers = ['बिल्कुल', 'पूरी तरह', 'सच में', 'कमबख्त', 'इतणो']
        insults = ['बेवकूफ', 'नालायक', 'औकातहीन', 'गंदो कीड़ो', 'हरामजादो', 'लफंगो', 'गुंडो', 'चुतिया', 'भोसड़ीका', 'मादरचोद']
        templates = [
            f"तू {random.choice(vulgar_terms)} {random.choice(insults)} है, {random.choice(intensifiers)} बेहूदा!",
            f"यो काय {random.choice(vulgar_terms)} चलै है? कुछ सही नई कर सकै?",
            f"यो {random.choice(vulgar_terms)} तोरा करणी है, {random.choice(insults)}।",
            f"म्हे तोरा {random.choice(vulgar_terms)} नखरा सै {random.choice(vulgar_terms)} थक गयो, {random.choice(insults)}।",
            f"तोरा जैसो {random.choice(insults)} {random.choice(vulgar_terms)} पूरी तरह बेकार है।",
            f"देख तोरा {random.choice(insults)} नै, कितणो {random.choice(vulgar_terms)} हरकत करै है।",
            f"तू {random.choice(vulgar_terms)} रो चपरासी, लाज आवै तोरा पै।",
            f"तोरी माई रो {random.choice(vulgar_terms)}, काय {random.choice(vulgar_terms)} करै है?",
        ]
        sentence = random.choice(templates)
        if not sentence.endswith(('.', '!', '?')):
            sentence += '.'
        return sentence
    
    elif label == 'health_issue':
        symptoms = ['तीव्र दर्द', 'लगातार थकान', 'चक्कर', 'सुन्नपन', 'छाती मां जकड़न', 'जोड़ मां सूजन', 'पीठ दर्द', 'गर्दन दर्द', 'बुखार', 'खांसी', 'तासीर', 'जी मिचलाणो', 'दस्त', 'गला बैठणो', 'नाक बहणो', 'आंख लाल होणो']
        body = ['कमर', 'छाती', 'सिर', 'पेट', 'पैर', 'गळो', 'गर्दन', 'कंधो', 'पीठ', 'नाक', 'आंख']
        time_phrases = ['पिछला हफ्ता सै', 'तीन दिन सै', 'काल सै', 'आज सुबह सै', 'रात सै', 'बड़ा दिन सै']
        templates = [
            f"{random.choice(time_phrases)} {random.choice(symptoms)} होवै है {random.choice(body)} मां, जो जावै नई।",
            f"रोज सुबह उठतिये {random.choice(symptoms)} हो जावै है, अब बहुत तंग कर दियो है।",
            f"डॉक्टर नै कह्यो कि {random.choice(body)} रो {random.choice(symptoms)} गंभीर हो सकै है।",
            f"म्हे कुछ भी करूं, {random.choice(symptoms)} बणो रै है अर नींद उड़गी है।",
            f"{random.choice(symptoms)} सै म्हे बेहाल होग्यो, दवा कराणी पड़ैगी।",
            f"शरीर मां {random.choice(symptoms)} महसूस होवै है, काय करूं समझ नई आवै।",
        ]
        sentence = random.choice(templates)
        if not sentence.endswith(('.', '!', '?')):
            sentence += '.'
        return sentence
    
    else:  # non_hate
        sentence = random.choice(NON_HATE_MARWARI)
        if not sentence.endswith(('.', '!', '?')):
            sentence += '.'
        return sentence

# ------------------------------------------------------------------
# 4. Column generation (same as other scripts)
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
    words = re.findall(r'[\u0900-\u097F]+', text)
    count = sum(1 for w in words if w in PROFANE_MARWARI)
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
    # Marwari is spoken in Rajasthan, mostly rural/urban India
    return random.choice(['india', 'rural_india', 'urban_india'])

def random_confidence():
    return round(random.uniform(0.80, 0.99), 2)

def random_annotator_id():
    return 'synthetic' if random.random() < 0.2 else f"A{random.randint(1,20)}"

# ------------------------------------------------------------------
# 5. Generate unique rows (target 9900 to reach 10000 total with existing 100)
# ------------------------------------------------------------------
new_rows = []
target_count = 9900   # because you already have ~100
attempts = 0
max_attempts = 12000000

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
    
    text = random_marwari_sentence(label, target_group, is_sarcasm, is_implicit)
    
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

print(f"Generated {len(new_rows)} new unique Marwari rows after {attempts} attempts.")

# ------------------------------------------------------------------
# 6. Save to CSV
# ------------------------------------------------------------------
output_file = 'extra_marwari_rows.csv'
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(new_rows)

print(f"Saved to {output_file}. Now append this to your existing Marwari dataset.")
