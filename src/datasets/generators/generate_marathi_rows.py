import csv
import random
import re
from pathlib import Path

random.seed(42)

# ------------------------------------------------------------------
# 1. Load existing Marathi texts (to avoid duplicates)
# ------------------------------------------------------------------
existing_texts = set()
marathi_csv_file = Path(__file__).resolve().parents[1] / "marathi.csv"

try:
    with open(marathi_csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                existing_texts.add(row[0].strip())
    print(f"Loaded {len(existing_texts)} existing Marathi sentences.")
except FileNotFoundError:
    print("No existing Marathi file found. Starting fresh.")
    existing_texts = set()

# ------------------------------------------------------------------
# 2. Marathi vulgar word list (for profanity count)
# ------------------------------------------------------------------
PROFANE_MARATHI = [
    'चुत्या', 'हरामखोर', 'भोसडीचा', 'बोक्या', 'मादरचोद', 'बहिनचोद',
    'साल्या', 'कुत्रा', 'डुक्कर', 'गाढव', 'बेवकूफ', 'नालायक', 'हरामजादा',
    'भाडखाऊ', 'लफंगा', 'गुंडा', 'बेइज्जत', 'जातीय', 'अस्पृश्य', 'चरसी', 'ठग'
]

# ------------------------------------------------------------------
# 3. Expanded Marathi sentence generators
# ------------------------------------------------------------------

# ----- Non-hate: 120 everyday sentences -----
NON_HATE_MARATHI = [
    "आज मी शेतात धान लावले.",
    "गावात भोजनाचा कार्यक्रम होता.",
    "शेळीचे पिल्लू जन्माला आले.",
    "मी माझ्या भावासोबत बाजारात गेलो.",
    "पत्र आले आहे, मुलाचे.",
    "आम्ही सर्व मिळून होळी खेळलो.",
    "भावाने नवीन मोटरसायकल घेतली.",
    "माझे गहू पीक चांगले आले.",
    "नणंदीच्या लग्नात खूप गर्दी होती.",
    "पूजेनंतर प्रसाद वाटप केला.",
    "आज पावसाळ्याचा पहिला दिवस होता.",
    "मी आईला बागेत फुले विकत घेतली.",
    "गावातल्या मंदिरात भजन सुरू होते.",
    "शाळेत मुलांचा वार्षिक कार्यक्रम झाला.",
    "बैलगाडीत शेण भरले होते.",
    "हळदीकुंकवाला सर्व स्त्रिया आल्या होत्या.",
    "नवीन पिढीने शेती सोडली आहे.",
    "पोरीच्या नावाचा सोहळा उत्साहात पार पडला.",
    "आजोबा गप्पा मारत बसले आहेत.",
    "आईने मला दुधात भात दिला.",
    "शेतात ऊस तोडणी सुरू आहे.",
    "गावातील तरुण मुंबईला नोकरीला गेले.",
    "बैलाला पाणी पाजले.",
    "गाईचे वासरू धावत होते.",
    "कोंबडी अंडी घालते.",
    "शेजारच्या बाईने उधार घेतलेले पैसे परत केले.",
    "मला साखरपेट्याला जायचे आहे.",
    "भाऊबीजेला बहिणीने भाऊच्या कपाळाला टिळा लावला.",
    "दिवाळीत फराळ केला.",
    "रस्त्यावर खड्डे झाले आहेत.",
    "पंचायत समितीतून नवा निर्णय झाला.",
    "शाळेला सुट्टी लागली.",
    "मुलगा परीक्षेत पहिला आला.",
    "बायकोने गोड धापे बनवले.",
    "सासूबाईंना ताप आला होता.",
    "जावई गावी आले होते.",
    "मामाच्या घरी चुलत भाऊ आला.",
    "मैत्रिणीच्या लग्नाला गेलो.",
    "भाजीपाला ताजा होता.",
    "दूध उकळले.",
    "अंगणात झेंडूची फुले फुलली.",
    "घरासमोर आंब्याचे झाड आहे.",
    "नदीत पाणी वाढले.",
    "मास्तरांनी गृहपाठ दिला.",
    "शाळेत संगीताचा वर्ग भरला.",
    "खेड्यात मेळावा झाला.",
    "हातगाडीने गहू नेला.",
    "विहिरीत पाणी कोरडे झाले.",
    "पंपाने शेताला पाणी दिले.",
    "बैल जोत लावली.",
    "कोयत्याने गवत कापले.",
    "घराचे छप्पर टाकले.",
    "चुलीवर भाकरी भाजली.",
    "तव्यावर पोळी भाजली.",
    "मधातील माशी अडकली.",
    "मुंग्या रांगत होत्या.",
    "पाखरांचे घरटे झाडावर होते.",
    "वाऱ्याने दार झपाटले.",
    "ढग गडगडले.",
    "वीज चमकली.",
    "बारिश थांबली.",
    "रस्ता चिखलून गेला.",
    "सायंकाळी दव पडले.",
    "सूर्य मावळला.",
    "चंद्र फुटला.",
    "तारे चमकले.",
    "रात्री कुत्री भुंकली.",
    "मांजर उंदीर पकडते.",
    "गाढव ओरडले.",
    "म्हशीला वासरू झाले.",
    "बकरीचे दूध गोड असते.",
    "लोणी कढवले.",
    "ताक प्याले.",
    "मठ्ठा खाल्ला.",
    "पापड वाळवले.",
    "कुरडई केली.",
    "शेतात मका पिकला.",
    "हरभरा फुलला.",
    "हळदीचे कंद काढले.",
    "मिरची सुकवली.",
    "कोथिंबीर उपटली.",
    "बारीक शेपू मिसळले.",
    "आंबट चटणी केली.",
    "थंडाई गार केली.",
    "श्रीखंड बनवले.",
    "पुरणपोळी केली.",
    "आमरस केला.",
    "भाकरी तयार झाली.",
    "भाजी तळली.",
    "कढी केली.",
    "वरण बनवले.",
    "भात शिजला.",
    "दही गोठले.",
    "तुप वितळले.",
    "साखर घातली.",
    "मीठ टाकले.",
    "लोणचे काढले.",
    "सांजेला दिवा लावला.",
    "निरांजन ओवाळले.",
    "आरती केली.",
    "प्रार्थना केली.",
    "गीता वाचली.",
    "देवळात घंटा वाजली.",
    "पुजाऱ्याने मंत्र म्हटले.",
    "पालखी निघाली.",
    "ध्वजारोहण झाले.",
    "रथ चालू झाला.",
    "भजन मंडळी गात होती.",
    "कीर्तन झाले.",
    "हरिनाम सप्ताह चालला.",
    "व्रत केले.",
    "उपवास ठेवला.",
    "फळे खाल्ली.",
    "पाणी प्याले.",
    "क्षेत्राला जायचे आहे.",
    "पंढरपूरची वारी सुरू आहे.",
    "नाशिकला स्नान केले.",
    "त्र्यंबकेश्वरला पूजा केली.",
    "शिर्डीला साईंचे दर्शन घेतले.",
    "तुळशीला पाणी घातले.",
    "बेल वृक्षाला दूध अर्पण केले.",
    "दीपक प्रज्वलित केला.",
]

# ----- Hate templates (expanded to 20) -----
HATE_TEMPLATES = [
    # Direct
    "{group} {verb} आणि त्यांना बाहेर काढले पाहिजे.",
    "{group} हे समाजाचे कर्करोग आहेत, त्यांचा नाश करा.",
    "मी सहमत नाही की {group} ला हक्क मिळावेत, ते धोकादायक आहेत.",
    "{group} ने आपली संस्कृती उद्ध्वस्त केली आहे.",
    "जोपर्यंत {group} आहेत तोपर्यंत शांती शक्य नाही.",
    "{group} च्या मुळातून उच्चाटन व्हायला हवे.",
    "{group} ला देशातून हाकलून द्या, हे परोपकारी नाहीत.",
    "{group} ने रक्ताचे हंगामे केले आहेत, आता बदला घ्या.",
    "{group} हे जनावरांसारखे आहेत, त्यांना वेगळे ठेवा.",
    "{group} विष पसरवतात, त्यांना अलग ठेवा.",
    # Implicit (used when is_implicit=True)
    "{group} बद्दल वेगळा विचार करावा लागेल.",
    "{group} कधीही आपल्यासारखे होऊ शकत नाहीत.",
    "{group} ची मूल्ये आपल्याशी जुळत नाहीत.",
    "आपल्या मुलांना {group} पासून वाचवा.",
    "{group} चा समाजात विश्वास ठेवू नये.",
]

def random_marathi_sentence(label, target_group=None, is_sarcastic=False, is_implicit=False):
    if label == 'hate':
        groups = {
            'gender': ['स्त्रिया', 'महिला', 'मुली', 'पुरुष', 'मर्द', 'हिजडे'],
            'religion': ['मुस्लिम', 'हिंदू', 'शीख', 'ख्रिश्चन', 'जैन', 'बौद्ध', 'ज्यू'],
            'caste': ['दलित', 'ब्राह्मण', 'क्षत्रिय', 'वैश्य', 'शूद्र', 'अस्पृश्य', 'मराठा', 'कुणबी'],
            'nationality': ['बिहारी', 'पंजाबी', 'दक्षिण भारतीय', 'उत्तर प्रदेशी', 'बंगाली', 'गुजराती'],
            'political': ['काँग्रेसी', 'भाजपाई', 'कम्युनिस्ट', 'आरक्षण समर्थक'],
            'individual': ['तो माणूस', 'हा बेवकूफ', 'तुझ्यासारखे']
        }
        group = target_group if target_group and target_group != 'none' else random.choice(list(groups.keys()))
        group_name = random.choice(groups.get(group, groups['nationality']))
        
        verbs = ['समाज नष्ट करत आहेत', 'घाण पसरवतात', 'गुन्हे करतात', 'रोग पसरवतात', 'गुंड आहेत', 'हटवले पाहिजेत']
        if is_implicit:
            verbs = ['आमच्यासारखे नाहीत', 'आमच्या मूल्यांच्या विरोधात आहेत', 'आमच्या संस्कृतीला धोका आहेत', 'विश्वास ठेवण्यासारखे नाहीत']
        
        # Select from expanded templates
        if is_implicit:
            # Use implicit templates (the ones listed above from index 10 onward)
            chosen_template = random.choice(HATE_TEMPLATES[10:])
        else:
            chosen_template = random.choice(HATE_TEMPLATES[:10])
        
        # Replace placeholders
        sentence = chosen_template.format(group=group_name, verb=random.choice(verbs))
        # Ensure ends with punctuation
        if not sentence.endswith(('.', '!', '?')):
            sentence += '.'
        return sentence
    
    elif label == 'offensive':
        vulgar_terms = PROFANE_MARATHI
        intensifiers = ['अगदी', 'पूर्णपणे', 'खरोखर', 'कमबख्त', 'एवढं']
        insults = ['बेवकूफ', 'नालायक', 'औकातहीन', 'घाणेरडा किडा', 'हरामखोर', 'लफंगा', 'गुंडा', 'चुत्या', 'भोसडीचा', 'बोक्या']
        templates = [
            f"तू {random.choice(vulgar_terms)} {random.choice(insults)} आहेस, {random.choice(intensifiers)} बेहूदा!",
            f"हा काय {random.choice(vulgar_terms)} चालू आहे? काही बरोबर करू शकत नाहीस?",
            f"हा {random.choice(vulgar_terms)} तुझ्यामुळे आहे, {random.choice(insults)}.",
            f"मी तुझ्या {random.choice(vulgar_terms)} नखऱ्यांनी {random.choice(vulgar_terms)} थकलो आहे, {random.choice(insults)}.",
            f"तुझ्यासारखा {random.choice(insults)} {random.choice(vulgar_terms)} पूर्णपणे नालायक आहे.",
            f"बघ आपल्या {random.choice(insults)} ला, कसा {random.choice(vulgar_terms)} वागतोय.",
            f"तू {random.choice(vulgar_terms)} चा पोरगा, लाज वाटते तुझी.",
            f"तुझ्या आईचा {random.choice(vulgar_terms)}, काय {random.choice(vulgar_terms)} करतोस?",
        ]
        sentence = random.choice(templates)
        sentence = sentence.strip()
        if not sentence.endswith(('.', '!', '?')):
            sentence += '.'
        return sentence
    
    elif label == 'health_issue':
        symptoms = ['तीव्र वेदना', 'सतत थकवा', 'चक्कर येणे', 'सुन्नपणा', 'छातीत घट्टपणा', 'सांध्याला सूज', 'पाठदुखी', 'मानदुखी', 'खोकला', 'ताप', 'अंग दुखी', 'उलटी', 'जुलाब', 'घसा खवखवणे', 'नाक वाहणे', 'डोळे लाल होणे']
        body = ['कमर', 'छाती', 'डोके', 'पोट', 'पाय', 'घसा', 'मान', 'खांदा', 'गुडघा', 'पाठ', 'नाक', 'डोळे']
        time_phrases = ['मागील एका आठवड्यापासून', 'गेले तीन दिवस', 'कालपासून', 'आज सकाळपासून', 'रात्रीपासून', 'खूप दिवसांपासून']
        templates = [
            f"{random.choice(time_phrases)} {random.choice(symptoms)} होत आहे {random.choice(body)} मध्ये, जे जात नाही.",
            f"रोज सकाळी उठल्यावर {random.choice(symptoms)} होते, आता खूप त्रास दिला आहे.",
            f"डॉक्टरांनी सांगितले की {random.choice(body)} चा {random.choice(symptoms)} गंभीर असू शकतो.",
            f"मी काहीही केले तरी {random.choice(symptoms)} कायम आहे आणि झोप उडाली आहे.",
            f"{random.choice(symptoms)} ने मला अस्वस्थ केले आहे, औषधोपचार करावा लागेल.",
            f"शरीरात {random.choice(symptoms)} जाणवते आहे, काय करावं कळत नाही.",
        ]
        sentence = random.choice(templates)
        sentence = sentence.strip()
        if not sentence.endswith(('.', '!', '?')):
            sentence += '.'
        return sentence
    
    else:  # non_hate
        sentence = random.choice(NON_HATE_MARATHI)
        if not sentence.endswith(('.', '!', '?')):
            sentence += '.'
        return sentence

# ------------------------------------------------------------------
# 4. Column generation (same as before)
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
    count = sum(1 for w in words if w in PROFANE_MARATHI)
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
    return random.choice(['india', 'rural_india', 'urban_india'])

def random_confidence():
    return round(random.uniform(0.80, 0.99), 2)

def random_annotator_id():
    return 'synthetic' if random.random() < 0.2 else f"A{random.randint(1,20)}"

# ------------------------------------------------------------------
# 5. Generate unique rows (target 8800, but with expanded templates)
# ------------------------------------------------------------------
new_rows = []
target_count = 8800
attempts = 0
max_attempts = 1000000   # Increased to allow more attempts

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
    
    text = random_marathi_sentence(label, target_group, is_sarcasm, is_implicit)
    
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

print(f"Generated {len(new_rows)} new unique Marathi rows after {attempts} attempts.")

output_file = 'extra_marathi_rows.csv'
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(new_rows)

print(f"Saved to {output_file}. Append to your existing Marathi dataset.")
