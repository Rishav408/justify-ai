import csv
import random
import re
from pathlib import Path

random.seed(42)

# ------------------------------------------------------------------
# 1. Load existing Bhojpuri texts
# ------------------------------------------------------------------
existing_texts = set()
bhojpuri_csv_file = Path(__file__).resolve().parents[1] / "bhojpuri.csv"

try:
    with open(bhojpuri_csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                existing_texts.add(row[0].strip())
    print(f"Loaded {len(existing_texts)} existing Bhojpuri sentences.")
except FileNotFoundError:
    print("No existing Bhojpuri file found. Starting fresh.")
    existing_texts = set()

# ------------------------------------------------------------------
# 2. Bhojpuri vulgar word list
# ------------------------------------------------------------------
PROFANE_BHOJPURI = [
    'चूतिया', 'हरामी', 'भोसड़ी', 'भोसड़ीके', 'मादरचोद', 'बहनचोद', 'साला',
    'कुत्ता', 'सुअर', 'गधा', 'लफंगा', 'गुंडा', 'नालायक', 'बेइज्जत',
    'हरामजादा', 'चरसी', 'भंगी', 'ड़रैया', 'ठग', 'बोक्या', 'भाडखाऊ'
]

# ------------------------------------------------------------------
# 3. Expanded Bhojpuri sentence generators
# ------------------------------------------------------------------

# ----- Non-hate: 120 everyday Bhojpuri sentences -----
NON_HATE_BHOJPURI = [
    "आज हम खेत गईनी धान रोपे।",
    "हमनी के गाँव में भोज चलत रहे।",
    "बकरी के बच्चा पैदा भइल बा।",
    "हम अपना भाई संग बाजार गईनी।",
    "चिट्ठी आ गइल बा, बेटा के।",
    "हम सब मिल के होली खेलनी।",
    "भइया ने नया मोटरसाइकिल लेले बाड़े।",
    "हमरा गेहूँ के फसल अच्छा भइल बा।",
    "ननद के ब्याह में बहुत भीड़ रहे।",
    "पूजा के बाद प्रसाद बाँटल गईल।",
    "आज पहिला बरखा भइल।",
    "माई के बगइचा में फुल लागल बा।",
    "गाँव के मंदिर में भजन होत रहे।",
    "स्कूल में बच्चन के सालाना समारोह भइल।",
    "बैलगाड़ी में गोबर भरल रहे।",
    "हल्दीकुमकुम में सब महिला आइली रहली।",
    "नई पीढ़ी खेती छोड़ दिहले बा।",
    "लड़की के नामकरण धूमधाम से भइल।",
    "दादा गप सुनावत बाड़े।",
    "माई दूधभात खिलवले।",
    "खेत में गन्ना कटाई चलत बा।",
    "गाँव के लड़का मुंबई नोकरी करे गइल बा।",
    "बैल के पानी पियावल गइल।",
    "गइया के बछरू धावत रहे।",
    "मुर्गी अंडा देले बा।",
    "पड़ोसिन के पैसा वापस मिल गइल।",
    "हमरा साखरपेटा जाए के बा।",
    "भाई दूज पर बहिन भाई के टीका लगवले।",
    "दिवाली में फराल बनल।",
    "सड़क पर गड्ढा हो गइल बा।",
    "पंचायत में नया फैसला भइल।",
    "स्कूल में छुट्टी लाग गइल।",
    "लड़का परीक्षा में पहिला आइल।",
    "घरवाली मीठा दही बनवले।",
    "सासूजी के बोखार आइल रहे।",
    "जवाई गाँव आइल बाड़े।",
    "मामा के घरे मामेर आइल।",
    "सहेली के बियाह में गईनी।",
    "साग ताजा रहे।",
    "दूध गरम कइल गइल।",
    "आँगन में गेंदा फुलल बा।",
    "घर के सामने आम के पेड़ बा।",
    "नदी में पानी बढ़ गइल बा।",
    "गुरुजी पढ़ाई दिहले।",
    "स्कूल में संगीत के क्लास भइल।",
    "गाँव में मेला लागल रहे।",
    "हाथगाड़ी से गेहूँ ढोलल गइल।",
    "कुआँ सूख गइल बा।",
    "पंप से खेत में पानी दिहल गइल।",
    "बैल जोत लिहल गइल।",
    "हँसिया से घास काटल गइल।",
    "घर के छप्पर डालल गइल।",
    "चूल्हा पर रोटी सेकल गइल।",
    "तवा पर पूड़ी बनल।",
    "मधु में मक्खी फँसल।",
    "चींटी रेंगत रहे।",
    "पंछी के घोसला पेड़ पर बा।",
    "हवा से दरवाजा खुल गइल।",
    "बादल गरजल।",
    "बिजली चमकल।",
    "बरखा थम गइल।",
    "सड़क कीचड़ हो गइल।",
    "साँझ में ओस पड़ल।",
    "सूरज डूब गइल।",
    "चाँद निकलल।",
    "तारा चमकल।",
    "रात में कुक्कुर भोंकल।",
    "बिल्ली चूहा पकड़ले।",
    "गधा चिल्लाइल।",
    "भैसा के बछरू भइल।",
    "बकरी के दूध मीठ होला।",
    "घी गरम कइल गइल।",
    "छाछ पीयल गइल।",
    "मट्ठा खाइल गइल।",
    "पापड़ सुखावल गइल।",
    "कुरड़ी बनल।",
    "खेत में मक्का पकल।",
    "चना फुलल।",
    "हलदी के गाँठ काढ़ल गइल।",
    "मिर्च सुखावल गइल।",
    "धनिया उपटल गइल।",
    "बारीक मसाला मिलावल गइल।",
    "खट्टी चटनी बनल।",
    "ठंडाई ठंढा कइल गइल।",
    "श्रीखंड बनल।",
    "पुरनपोली बनल।",
    "आमरस बनल।",
    "भाकरी तइयार भइल।",
    "तरकारी भुनल गइल।",
    "कढ़ी बनल।",
    "वरण बनल।",
    "चावल पकल।",
    "दही जमल।",
    "घी पिघलल।",
    "चीनी मिलावल गइल।",
    "नमक डालल गइल।",
    "अचार निकालल गइल।",
    "साँझे दिया बारल गइल।",
    "नीरांजन ओवारल गइल।",
    "आरती कइल गइल।",
    "प्रार्थना कइल गइल।",
    "गीता पढ़ल गइल।",
    "मंदिर में घंटा बजल।",
    "पुजारी मंत्र पढ़ले।",
    "पालकी निकलल।",
    "झंडा चढ़ावल गइल।",
    "रथ चलल।",
    "भजन मंडली गावत रहे।",
    "कीर्तन भइल।",
    "हरिनाम सप्ताह चलत रहे।",
    "बरत रहल।",
    "उपवास रहल।",
    "फल खाइल गइल।",
    "पानी पियल गइल।",
    "तीरथ जाए के बा।",
    "पंढरपुर के वारी चलत बा।",
    "नाशिक में स्नान कइल गइल।",
    "त्र्यंबकेश्वर में पूजा कइल गइल।",
    "शिर्डी में साईं के दरसन कइल गइल।",
    "तुलसी में पानी डालल गइल।",
    "बेल के पेड़ पे दूध चढ़ावल गइल।",
    "दीपक जरावल गइल।",
]

# ----- Hate templates (expanded) -----
HATE_TEMPLATES_BHOJPURI = [
    # Direct
    "{group} {verb} आ हटावल जरूरी बा।",
    "{group} समाज के कर्करोग बाड़े, इनका नाश करीं।",
    "हम सहमत नइखी कि {group} के हक मिले, ई खतरनाक बाड़े।",
    "{group} हमार संस्कृति बरबाद क देले बाड़े।",
    "जबले {group} बाड़े तबले सुख नइखी।",
    "{group} के जड़ से खतम करे के चाहीं।",
    "{group} के देश से निकाल दीं, ई निकम्मा बाड़े।",
    "{group} खून के खेल कइले बाड़े, अब बदला लीं।",
    "{group} जानवर जइसन बाड़े, अलग राखल जाय।",
    "{group} जहर फैलावत बाड़े, इनका अलग राखीं।",
    # Implicit
    "{group} के बारे में अलग सोचे के जरूरत बा।",
    "{group} कबो हमनी जइसन ना हो सकेला।",
    "{group} के मूल्य हमनी से ना मिलेला।",
    "हमार लरिकन के {group} से बचाईं।",
    "{group} पर भरोसा ना करीं।",
]

def random_bhojpuri_sentence(label, target_group=None, is_sarcastic=False, is_implicit=False):
    if label == 'hate':
        groups = {
            'gender': ['औरत', 'महिला', 'लड़की', 'मरद', 'लइका', 'ट्रांसजेंडर'],
            'religion': ['मुसलमान', 'हिंदू', 'सिख', 'ईसाई', 'जैन', 'बौद्ध', 'यहूदी'],
            'caste': ['दलित', 'ब्राह्मण', 'क्षत्रिय', 'वैश्य', 'शूद्र', 'अछूत', 'यादव', 'कुर्मी'],
            'nationality': ['बिहारी', 'पंजाबी', 'दक्खिनी', 'उत्तर प्रदेशी', 'बंगाली', 'गुजराती'],
            'political': ['कांग्रेसी', 'भाजपाई', 'कम्युनिस्ट', 'आरक्षण वाला'],
            'individual': ['ऊ आदमी', 'ई बेवकूफ', 'तोहरा जइसन']
        }
        group = target_group if target_group and target_group != 'none' else random.choice(list(groups.keys()))
        group_name = random.choice(groups.get(group, groups['nationality']))
        
        verbs = ['समाज के बिगाड़ करत बाड़े', 'गंदगी फैलावत बाड़े', 'अपराध करत बाड़े', 'बीमारी फैलावत बाड़े', 'बदमाश बाड़े', 'हटावे के चाहीं']
        if is_implicit:
            verbs = ['हमनी जइसन नइखे', 'हमनी के रीति के खिलाफ बाड़े', 'हमनी के संस्कृति खतरा बा', 'भरोसा के लायक नइखे']
        
        if is_implicit:
            chosen_template = random.choice(HATE_TEMPLATES_BHOJPURI[10:])
        else:
            chosen_template = random.choice(HATE_TEMPLATES_BHOJPURI[:10])
        
        sentence = chosen_template.format(group=group_name, verb=random.choice(verbs))
        if not sentence.endswith(('.', '!', '?')):
            sentence += '.'
        return sentence
    
    elif label == 'offensive':
        vulgar_terms = PROFANE_BHOJPURI
        intensifiers = ['बिल्कुल', 'पूरी तरह', 'सचमुच', 'कमबख्त', 'इतना']
        insults = ['बेवकूफ', 'नालायक', 'औकातहीन', 'गंदा कीड़ा', 'हरामजादा', 'लफंगा', 'गुंडा', 'चूतिया', 'भोसड़ीका', 'मादरचोद']
        templates = [
            f"तू {random.choice(vulgar_terms)} {random.choice(insults)} बाड़ऽ, {random.choice(intensifiers)} बेहूदा!",
            f"ई का {random.choice(vulgar_terms)} चल रहल बा? कछु सही ना कर सकत बाड़ऽ?",
            f"ई {random.choice(vulgar_terms)} तोहरे कारण से बा, {random.choice(insults)}।",
            f"हम तोहरा {random.choice(vulgar_terms)} नखरे से {random.choice(vulgar_terms)} थक गईनी, {random.choice(insults)}।",
            f"तोहरा जइसन {random.choice(insults)} {random.choice(vulgar_terms)} पूरी तरह बेकार बा।",
            f"देख तोहरा {random.choice(insults)} के, कइसे {random.choice(vulgar_terms)} हरकत करत बा।",
            f"तू {random.choice(vulgar_terms)} के चपरासी, लाज आवेला तोहरे प।",
            f"तोहरे माई के {random.choice(vulgar_terms)}, का {random.choice(vulgar_terms)} क रहल बाड़ऽ?",
        ]
        sentence = random.choice(templates)
        if not sentence.endswith(('.', '!', '?')):
            sentence += '.'
        return sentence
    
    elif label == 'health_issue':
        symptoms = ['तेज दर्द', 'लगातार थकान', 'चक्कर', 'सुन्नपन', 'सीने में जकड़न', 'जोड़ में सूजन', 'पीठ दर्द', 'गर्दन दर्द', 'बोखार', 'खाँसी', 'तासीर', 'जी मिचलावे', 'दस्त', 'गला बैठल', 'नाक बहे', 'आँख लाल']
        body = ['कमर', 'सीना', 'सिर', 'पेट', 'गोड़', 'गला', 'गर्दन', 'कन्धा', 'गोड़', 'पीठ', 'नाक', 'आँख']
        time_phrases = ['पछिला हफ्ता से', 'तीन दिन से', 'काल से', 'आज सुबह से', 'रात से', 'बहुत दिन से']
        templates = [
            f"{random.choice(time_phrases)} {random.choice(symptoms)} होत बा {random.choice(body)} में, जे ना जात बा।",
            f"रोज सुबह उठतिये {random.choice(symptoms)} हो जाला, अब बहुत तंग कर दिहले बा।",
            f"डाक्टर कइले कि {random.choice(body)} के {random.choice(symptoms)} गंभीर हो सकता।",
            f"हम जउन करीं, {random.choice(symptoms)} बा रहेला आ नींद उड़ गइल बा।",
            f"{random.choice(symptoms)} से हम बेहाल बानी, दवा करावे के पड़ी।",
            f"शरीर में {random.choice(symptoms)} महसूस होत बा, का करीं समझ ना आवेला।",
        ]
        sentence = random.choice(templates)
        if not sentence.endswith(('.', '!', '?')):
            sentence += '.'
        return sentence
    
    else:  # non_hate
        sentence = random.choice(NON_HATE_BHOJPURI)
        if not sentence.endswith(('.', '!', '?')):
            sentence += '.'
        return sentence

# ------------------------------------------------------------------
# 4. Column generation (same as Marathi, reuse functions)
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
    count = sum(1 for w in words if w in PROFANE_BHOJPURI)
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
    return random.choice(['rural_india', 'india', 'urban_india'])

def random_confidence():
    return round(random.uniform(0.80, 0.99), 2)

def random_annotator_id():
    return 'synthetic' if random.random() < 0.2 else f"A{random.randint(1,20)}"

# ------------------------------------------------------------------
# 5. Generate unique rows
# ------------------------------------------------------------------
new_rows = []
target_count = 8800
attempts = 0
max_attempts = 100000

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
    
    text = random_bhojpuri_sentence(label, target_group, is_sarcasm, is_implicit)
    
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

print(f"Generated {len(new_rows)} new unique Bhojpuri rows after {attempts} attempts.")

output_file = 'extra_bhojpuri_rows.csv'
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(new_rows)

print(f"Saved to {output_file}. Append to your existing Bhojpuri dataset.")
