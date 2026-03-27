import csv
from pathlib import Path


COLUMNS = [
    "text",
    "label",
    "severity",
    "is_implicit",
    "is_sarcasm",
    "target_group",
    "target_type",
    "directness",
    "call_to_action",
    "tone",
    "emotion",
    "profanity_count",
    "platform",
    "domain",
    "region",
    "confidence",
    "annotator_id",
]


def row(
    text,
    label,
    severity,
    is_implicit,
    is_sarcasm,
    target_group,
    target_type,
    directness,
    call_to_action,
    tone,
    emotion,
    profanity_count,
    platform,
    domain,
    region,
    confidence,
    annotator_id,
):
    return {
        "text": text,
        "label": label,
        "severity": severity,
        "is_implicit": str(is_implicit).lower(),
        "is_sarcasm": str(is_sarcasm).lower(),
        "target_group": target_group,
        "target_type": target_type,
        "directness": directness,
        "call_to_action": str(call_to_action).lower(),
        "tone": tone,
        "emotion": emotion,
        "profanity_count": profanity_count,
        "platform": platform,
        "domain": domain,
        "region": region,
        "confidence": f"{confidence:.2f}",
        "annotator_id": annotator_id,
    }


def build_rows(spec):
    rows = []
    for i in range(spec["counts"]["non_hate"]):
        text = (
            f"{spec['nh_prefix'][i % len(spec['nh_prefix'])]} "
            f"{spec['nh_topic'][i % len(spec['nh_topic'])]}"
            f"{spec['nh_suffix'][i % len(spec['nh_suffix'])]}"
        )
        rows.append(
            row(
                text,
                "non_hate",
                "none",
                False,
                False,
                "none",
                "none",
                "none",
                False,
                "neutral",
                "joy" if i % 3 == 0 else "none",
                0,
                ["general", "chat", "social_media", "news"][i % 4],
                ["general", "education", "sports", "health"][i % 4],
                spec["region_non_hate"][i % len(spec["region_non_hate"])],
                min(1.0, 0.95 + (i % 5) * 0.01),
                spec["annotator_non_hate"][i % len(spec["annotator_non_hate"])],
            )
        )

    groups = ["gender", "religion", "caste", "nationality", "political", "individual"]
    direct_total = spec["counts"]["hate"] - spec["implicit_count"] - spec["sarcasm_count"]
    for i in range(direct_total):
        group = groups[i % len(groups)]
        base, severity, call_to_action, profanity_count, platform, domain, target_type = spec["direct"][group][
            (i // len(groups)) % len(spec["direct"][group])
        ]
        context = spec["hate_context"][i % len(spec["hate_context"])]
        text = f"{context} {base}".strip()
        rows.append(
            row(
                text,
                "hate",
                severity,
                False,
                False,
                group,
                target_type,
                "direct",
                call_to_action,
                "aggressive" if call_to_action or severity == "severe" else "dismissive",
                "anger" if call_to_action or severity in {"moderate", "severe"} else "disgust",
                profanity_count,
                platform,
                domain,
                spec["region_hate"][i % len(spec["region_hate"])],
                0.82 + (i % 9) * 0.02,
                spec["annotator_hate"][i % len(spec["annotator_hate"])],
            )
        )

    for i in range(spec["implicit_count"]):
        group = groups[i % len(groups)]
        text, profanity_count, platform, domain, target_type = spec["implicit"][group][
            i % len(spec["implicit"][group])
        ]
        rows.append(
            row(
                text,
                "hate",
                "mild",
                True,
                False,
                group,
                target_type,
                "indirect",
                False,
                "dismissive",
                "disgust" if i % 2 == 0 else "fear",
                profanity_count,
                platform,
                domain,
                spec["region_hate"][i % len(spec["region_hate"])],
                0.76 + (i % 7) * 0.02,
                spec["annotator_hate"][i % len(spec["annotator_hate"])],
            )
        )

    sarcasm_groups = ["gender", "religion", "nationality", "political", "caste", "individual"]
    for i in range(spec["sarcasm_count"]):
        group = sarcasm_groups[i % len(sarcasm_groups)]
        text, profanity_count, platform, domain, target_type = spec["sarcasm"][group][
            i % len(spec["sarcasm"][group])
        ]
        rows.append(
            row(
                text,
                "hate",
                "mild",
                False,
                True,
                group,
                target_type,
                "indirect",
                False,
                "sarcastic",
                "disgust",
                profanity_count,
                platform,
                domain,
                spec["region_hate"][i % len(spec["region_hate"])],
                0.80 + (i % 6) * 0.02,
                spec["annotator_hate"][i % len(spec["annotator_hate"])],
            )
        )

    for i in range(spec["counts"]["offensive"]):
        text, profanity_count = spec["offensive"][i % len(spec["offensive"])]
        rows.append(
            row(
                text,
                "offensive",
                "mild" if i % 2 == 0 else "moderate",
                False,
                i % 7 == 0,
                "individual",
                "individual",
                "direct",
                False,
                "aggressive" if i % 2 == 0 else "dismissive",
                "anger" if i % 2 == 0 else "disgust",
                profanity_count,
                ["chat", "social_media", "general"][i % 3],
                "general",
                spec["region_other"][i % len(spec["region_other"])],
                0.83 + (i % 8) * 0.02,
                spec["annotator_other"][i % len(spec["annotator_other"])],
            )
        )

    for i in range(spec["counts"]["health_issue"]):
        text = spec["health"][i % len(spec["health"])]
        rows.append(
            row(
                text,
                "health_issue",
                "none",
                False,
                False,
                "none",
                "none",
                "none",
                False,
                "fearful" if i % 2 == 0 else "neutral",
                "fear" if i % 2 == 0 else "sadness",
                0,
                ["chat", "general", "social_media"][i % 3],
                "health",
                spec["region_other"][i % len(spec["region_other"])],
                0.86 + (i % 7) * 0.02,
                spec["annotator_other"][i % len(spec["annotator_other"])],
            )
        )

    return rows


ENGLISH = {
    "counts": {"hate": 80, "non_hate": 90, "offensive": 15, "health_issue": 15},
    "implicit_count": 12,
    "sarcasm_count": 10,
    "region_non_hate": ["global", "global", "global", "global", "global", "urban_india"],
    "region_other": ["global", "global", "india"],
    "region_hate": ["global", "global", "global", "global", "india"],
    "annotator_non_hate": ["A1"],
    "annotator_other": ["A1"],
    "annotator_hate": ["A1"],
    "nh_prefix": [
        "I enjoyed",
        "We talked about",
        "The class discussed",
        "My family cooked",
        "The neighborhood celebrated",
        "I read about",
        "We watched",
        "The coach praised",
        "My doctor suggested",
        "The office planned",
    ],
    "nh_topic": [
        "the spring flowers in the park",
        "a warm cup of tea after work",
        "the rain and cool evening breeze",
        "our local football match",
        "a new movie at the theater",
        "study plans for the exam",
        "a community cleanup event",
        "healthy meals for the week",
        "a birthday dinner with cousins",
        "the sunrise over the lake",
    ],
    "nh_suffix": [
        " this morning.",
        " after dinner.",
        " with my friends.",
        " before class started.",
        " and it felt peaceful.",
        " during the weekend.",
    ],
    "offensive": [
        ("You clueless idiot, learn to read before you post.", 1),
        ("Stop acting like a jerk and do your job.", 1),
        ("That was a trash take, dude.", 1),
        ("He is an arrogant fool with zero sense.", 1),
        ("Quit being a nasty clown in the group chat.", 1),
    ],
    "health": [
        "My chest has been hurting since yesterday evening.",
        "I have had a fever and body ache for two days.",
        "My throat feels swollen and it is hard to swallow.",
        "I keep coughing at night and cannot sleep well.",
        "There is a sharp pain in my lower back today.",
        "I feel dizzy whenever I stand up too quickly.",
    ],
    "hate_context": ["", "Online,", "In the thread,", "At the rally,", "People there said", "On that page,"],
    "direct": {
        "gender": [
            ("Women like that should be pushed out of every leadership role.", "moderate", False, 0, "social_media", "general", "community"),
            ("Lesbians like her ruin every decent space they enter.", "moderate", False, 0, "chat", "general", "community"),
        ],
        "religion": [
            ("Kick those filthy fanatics out of our neighborhood.", "severe", True, 1, "political_speech", "religious", "community"),
            ("People of that religion are parasites on this country.", "moderate", False, 0, "social_media", "religious", "community"),
        ],
        "caste": [
            ("People from that caste should stay in their lane forever.", "moderate", False, 0, "chat", "general", "community"),
            ("Those caste people are scum and should never be trusted.", "moderate", False, 1, "chat", "general", "community"),
        ],
        "nationality": [
            ("Send those foreigners back and shut the border on them.", "severe", True, 0, "news", "political", "community"),
            ("Immigrants like them are dirty thieves, throw them out.", "severe", True, 1, "social_media", "political", "community"),
        ],
        "political": [
            ("That party's supporters are vermin and should be crushed.", "severe", True, 0, "political_speech", "political", "ideology"),
            ("Anyone backing that ideology deserves to be beaten off the streets.", "severe", True, 0, "political_speech", "political", "ideology"),
        ],
        "individual": [
            ("You are a worthless rat and I hope someone ends you.", "severe", True, 1, "social_media", "general", "individual"),
            ("That man is pure garbage and needs to disappear.", "moderate", True, 0, "chat", "general", "individual"),
        ],
    },
    "implicit": {
        "gender": [("You can always tell when women get emotional and ruin the serious work.", 0, "news", "general", "community")],
        "religion": [("Everyone knows what that community does once they become the majority.", 0, "chat", "religious", "community")],
        "caste": [("Families from that background never really fit into decent neighborhoods.", 0, "chat", "general", "community")],
        "nationality": [("Those newcomers somehow make every block feel less safe.", 0, "news", "political", "community")],
        "political": [("You know the kind of people who clap for that party, right?", 0, "social_media", "political", "ideology")],
        "individual": [("Some people carry such a rotten vibe that they poison every room.", 0, "chat", "general", "individual")],
    },
    "sarcasm": {
        "gender": [("Oh sure, women are obviously too logical to mess anything up, right?", 0, "social_media", "general", "community")],
        "religion": [("Yeah, that religion is totally famous for respecting everyone equally.", 0, "social_media", "religious", "community")],
        "caste": [("Of course those caste elites are always the first to think about fairness.", 0, "chat", "political", "community")],
        "nationality": [("Immigrants are just amazing for jobs, aren't they?", 0, "social_media", "political", "community")],
        "political": [("What a noble movement, spreading hate and calling it patriotism.", 0, "news", "political", "ideology")],
        "individual": [("Wow, he is such a delightful human, always making life miserable for everyone.", 0, "chat", "general", "individual")],
    },
}

HINDI = {
    "counts": {"hate": 60, "non_hate": 65, "offensive": 13, "health_issue": 12},
    "implicit_count": 10,
    "sarcasm_count": 10,
    "region_non_hate": ["india", "india", "rural_india"],
    "region_other": ["india", "rural_india"],
    "region_hate": ["india", "india", "india", "rural_india"],
    "annotator_non_hate": ["A1"],
    "annotator_other": ["A1"],
    "annotator_hate": ["A1"],
    "nh_prefix": ["आज", "हमने", "स्कूल में", "घर पर", "मोहल्ले में", "डॉक्टर ने", "ऑफिस में", "शाम को"],
    "nh_topic": [
        "सुबह की ठंडी हवा का आनंद लिया",
        "गरम चाय के साथ नाश्ता किया",
        "क्रिकेट मैच पर चर्चा की",
        "बच्चों की पढ़ाई में मदद की",
        "बरसात के बाद की खुशबू महसूस की",
        "परिवार के साथ खाना बनाया",
        "स्वास्थ्य जांच की रिपोर्ट देखी",
        "पड़ोसियों के साथ सफाई अभियान किया",
    ],
    "nh_suffix": ["।", " और अच्छा लगा।", " फिर सब मुस्कुराए।", " जिससे मन शांत हुआ।"],
    "offensive": [
        ("तू बिल्कुल बेवकूफ है, ढंग से बात कर।", 1),
        ("क्या घटिया हरकत है, शर्म कर।", 1),
        ("यह आदमी पूरा निकम्मा और बदतमीज है।", 1),
        ("तुम्हारी सोच बहुत सड़ी हुई है, यार।", 1),
        ("फालतू बकवास बंद करो।", 1),
    ],
    "health": [
        "मेरे सीने में दो दिन से दर्द हो रहा है।",
        "मुझे रात से तेज बुखार और ठंड लग रही है।",
        "गले में सूजन है और निगलने में दर्द हो रहा है।",
        "बार बार चक्कर आ रहा है और कमजोरी लग रही है।",
        "पीठ में तेज दर्द है और चलना मुश्किल लग रहा है।",
    ],
    "hate_context": ["", "ऑनलाइन,", "रैली में,", "पोस्ट में,"],
    "direct": {
        "gender": [
            ("औरतों को बड़े फैसलों से दूर ही रखना चाहिए।", "moderate", False, 0, "social_media", "general", "community"),
            ("इन औरतों को बस रसोई तक ही सीमित रहना चाहिए।", "moderate", False, 0, "chat", "general", "community"),
        ],
        "religion": [
            ("इन कट्टर लोगों को मोहल्ले से बाहर निकालो।", "severe", True, 0, "political_speech", "religious", "community"),
            ("उस मजहब के लोग गंदगी फैलाते हैं।", "moderate", False, 0, "social_media", "religious", "community"),
        ],
        "caste": [
            ("उस जाति के लोगों को गांव की पंचायत में मत घुसने दो।", "moderate", True, 0, "chat", "political", "community"),
            ("वो नीच जात वाले हमेशा झगड़ा ही फैलाते हैं।", "moderate", False, 1, "chat", "general", "community"),
        ],
        "nationality": [
            ("विदेशियों को यहां से भगाओ, ये देश खराब कर रहे हैं।", "severe", True, 0, "news", "political", "community"),
            ("बाहरी लोगों को शहर से निकाल फेंको।", "moderate", True, 0, "political_speech", "political", "community"),
        ],
        "political": [
            ("उस पार्टी के चमचे देश के दुश्मन हैं, इन्हें कुचल दो।", "severe", True, 0, "political_speech", "political", "ideology"),
            ("उस विचारधारा के समर्थक कीड़े हैं।", "moderate", False, 0, "social_media", "political", "ideology"),
        ],
        "individual": [
            ("तू हरामी आदमी है, तुझे खत्म कर देना चाहिए।", "severe", True, 1, "social_media", "general", "individual"),
            ("वो कमीना आदमी पूरे गांव का जहर है।", "moderate", False, 1, "chat", "general", "individual"),
        ],
    },
    "implicit": {
        "gender": [("जब भी महिलाओं को जिम्मेदारी दो, दफ्तर का हाल पता ही है।", 0, "news", "general", "community")],
        "religion": [("सब जानते हैं कि वह समुदाय मौका मिलते ही रंग दिखाता है।", 0, "chat", "religious", "community")],
        "caste": [("कुछ घरों की परवरिश ही ऐसी होती है, पहचानना मुश्किल नहीं।", 0, "chat", "general", "community")],
        "nationality": [("ये बाहरी लोग आते ही इलाके का माहौल बदल देते हैं।", 0, "news", "political", "community")],
        "political": [("उस पार्टी को पसंद करने वालों से दूरी रखना ही बेहतर है।", 0, "social_media", "political", "ideology")],
        "individual": [("उस आदमी के आते ही माहौल गंदा सा हो जाता है।", 0, "chat", "general", "individual")],
    },
    "sarcasm": {
        "gender": [("हाँ हाँ, औरतें तो बिल्कुल ही भावनाओं में नहीं बहतीं, है ना?", 0, "social_media", "general", "community")],
        "religion": [("वाह, उस समुदाय की सहनशीलता तो दुनिया में मशहूर है।", 0, "social_media", "religious", "community")],
        "caste": [("बिलकुल, जाति देखकर भेदभाव तो सिर्फ कहानी है।", 0, "chat", "political", "community")],
        "nationality": [("हाँ, बाहरी लोग आते हैं और सबके लिए काम ही काम छोड़ जाते हैं।", 0, "social_media", "political", "community")],
        "political": [("क्या शानदार विचारधारा है, बस नफरत ही नफरत बांटती है।", 0, "news", "political", "ideology")],
        "individual": [("वाह, वो आदमी कितना नेक है, हर किसी की जिंदगी खराब करता है।", 0, "chat", "general", "individual")],
    },
}

MARATHI = {
    "counts": {"hate": 60, "non_hate": 65, "offensive": 13, "health_issue": 12},
    "implicit_count": 10,
    "sarcasm_count": 10,
    "region_non_hate": ["urban_india", "india"],
    "region_other": ["urban_india", "india"],
    "region_hate": ["urban_india", "urban_india", "india"],
    "annotator_non_hate": ["A1"],
    "annotator_other": ["A1"],
    "annotator_hate": ["A1"],
    "nh_prefix": ["आज", "आम्ही", "शाळेत", "घरी", "पुण्यात", "मुंबईत", "डॉक्टरांनी", "ऑफिसमध्ये"],
    "nh_topic": [
        "थंड वाऱ्यात फेरफटका मारला",
        "गरम चहासोबत नाश्ता केला",
        "क्रिकेट सामन्यावर गप्पा मारल्या",
        "मुलांच्या अभ्यासाला मदत केली",
        "पावसानंतरचा सुगंध अनुभवला",
        "कुटुंबासोबत जेवण बनवले",
        "आरोग्य तपासणीचा अहवाल पाहिला",
        "मोहल्ल्यात स्वच्छता मोहीम केली",
    ],
    "nh_suffix": ["।", " आणि छान वाटले।", " म्हणून मन शांत झाले।", " सगळे आनंदी झाले।"],
    "offensive": [
        ("तू अगदी बावळट आहेस, नीट विचार कर.", 1),
        ("काय भंगार बोलतोयस तू.", 1),
        ("हा माणूस फारच उर्मट आणि निकम्मा आहे.", 1),
        ("तुझं उत्तर फारच ढिसाळ आहे.", 1),
        ("फालतू बडबड बंद कर.", 1),
    ],
    "health": [
        "माझ्या छातीत कालपासून दुखत आहे.",
        "मला ताप आला आहे आणि अंग दुखत आहे.",
        "घशात सूज आहे आणि गिळताना त्रास होतो.",
        "उभे राहिल्यावर चक्कर येते.",
        "पाठीमध्ये खूप वेदना आहेत.",
    ],
    "hate_context": ["", "ऑनलाइन,", "सभेत,", "पोस्टमध्ये,"],
    "direct": {
        "gender": [
            ("अशा बायकांना कोणत्याही मोठ्या पदावर बसवू नका.", "moderate", True, 0, "social_media", "general", "community"),
            ("या स्त्रिया फक्त घरात बसण्यासाठीच योग्य आहेत.", "moderate", False, 0, "chat", "general", "community"),
        ],
        "religion": [
            ("त्या धर्माच्या लोकांना आपल्या भागातून हाकलून द्या.", "severe", True, 0, "political_speech", "religious", "community"),
            ("त्या पंथाचे लोक नेहमी गोंधळच घालतात.", "moderate", False, 0, "social_media", "religious", "community"),
        ],
        "caste": [
            ("त्या जातीच्या लोकांना गावच्या बैठकीत जागा देऊ नका.", "moderate", True, 0, "chat", "political", "community"),
            ("तो नीच जातीतला माणूस कुणावरही विश्वास ठेवू देत नाही.", "moderate", False, 1, "chat", "general", "community"),
        ],
        "nationality": [
            ("बाहेरून आलेल्यांना शहराबाहेर फेका.", "severe", True, 0, "news", "political", "community"),
            ("परराज्यातून आलेले लोक इथलं वातावरण बिघडवतात.", "moderate", False, 0, "news", "political", "community"),
        ],
        "political": [
            ("त्या पक्षाचे समर्थक किडे आहेत, त्यांना चिरडून टाका.", "severe", True, 0, "political_speech", "political", "ideology"),
            ("त्या विचारसरणीचे लोक समाजावरचा डाग आहेत.", "moderate", False, 0, "social_media", "political", "ideology"),
        ],
        "individual": [
            ("तो हरामखोर माणूस संपवून टाकायला हवा.", "severe", True, 1, "social_media", "general", "individual"),
            ("तो माणूस पूर्ण गावासाठी अपशकून आहे.", "moderate", False, 0, "chat", "general", "individual"),
        ],
    },
    "implicit": {
        "gender": [("महिलांना जबाबदारी दिली की शेवटी गोंधळ होणारच.", 0, "news", "general", "community")],
        "religion": [("तो समुदाय वाढला की परिसराचा रंग बदलतोच.", 0, "chat", "religious", "community")],
        "caste": [("काही घरांची ओळख त्यांच्या वागण्यातून लगेच कळते.", 0, "chat", "general", "community")],
        "nationality": [("बाहेरचे लोक आले की मुंबईत सुरक्षित वाटत नाही.", 0, "news", "political", "community")],
        "political": [("त्या पक्षाच्या लोकांपासून थोडं लांब राहिलेलंच बरं.", 0, "social_media", "political", "ideology")],
        "individual": [("तो आला की खोलीतलं वातावरणच खराब होतं.", 0, "chat", "general", "individual")],
    },
    "sarcasm": {
        "gender": [("हो हो, बायका तर भावना बाजूला ठेवूनच निर्णय घेतात, नाही का?", 0, "social_media", "general", "community")],
        "religion": [("वा, त्या समुदायाची सहिष्णुता तर फार प्रसिद्ध आहे.", 0, "social_media", "religious", "community")],
        "caste": [("अर्थातच, जात पाहून भेदभाव महाराष्ट्रात अजिबात होत नाही.", 0, "chat", "political", "community")],
        "nationality": [("हो, बाहेरचे लोक आले की पुण्याची संस्कृतीच फुलते म्हणे.", 0, "social_media", "political", "community")],
        "political": [("काय सुंदर विचारसरणी आहे, फक्त द्वेष पसरवते.", 0, "news", "political", "ideology")],
        "individual": [("वा, तो माणूस किती छान, सगळ्यांचं आयुष्य बिघडवतो.", 0, "chat", "general", "individual")],
    },
}

BHOJPURI = {
    "counts": {"hate": 40, "non_hate": 45, "offensive": 7, "health_issue": 8},
    "implicit_count": 8,
    "sarcasm_count": 10,
    "region_non_hate": ["rural_india"],
    "region_other": ["rural_india"],
    "region_hate": ["rural_india"],
    "annotator_non_hate": ["synthetic", "synthetic", "synthetic", "A1"],
    "annotator_other": ["synthetic", "synthetic", "A1"],
    "annotator_hate": ["synthetic", "synthetic", "synthetic", "A1"],
    "nh_prefix": ["आज", "हमनी", "घरे", "खेत पर", "गांव में", "डॉक्टर कहले", "स्कूल में"],
    "nh_topic": [
        "सबेरे के ठंढा हवा में घूमनी",
        "गरम चाय संग नाश्ता कईनी",
        "क्रिकेट खेल पर बतकही भइल",
        "लइकन के पढ़ाई में मदद कईनी",
        "बरखा बाद माटी के खुशबू अइल",
        "घर वाला संगे रोटी बनवनी",
        "स्वास्थ्य जांच के कागज देखनी",
    ],
    "nh_suffix": ["।", " त मन खुश भइल।", " सब हंस पड़ल।", " दिन बढ़िया निकलल।"],
    "offensive": [
        ("तू बड़ा बेवकूफ बाड़ऽ, चुप हो जा।", 1),
        ("ई का घटिया बकवास बा।", 1),
        ("ओकर दिमाग घास चरहे गइल बा।", 1),
        ("फालतू रउआ हल्ला मत मचावऽ।", 1),
    ],
    "health": [
        "हमार छाती में काल्हु से दरद बा।",
        "दू दिन से बुखार आ बदन टूटत बा।",
        "गरदन सुजल बा आ निगले में दिक्कत बा।",
        "बार बार चक्कर आवत बा।",
        "पीठ में तेज पीरा बा।",
    ],
    "hate_context": ["", "ऑनलाइन,", "सभा में,"],
    "direct": {
        "gender": [
            ("एह औरतन के फैसला से दूर राखल जाव।", "moderate", True, 0, "social_media", "general", "community"),
            ("एह मेहरारू लोग बस रसोई खातिर ठीक बा।", "moderate", False, 0, "chat", "general", "community"),
        ],
        "religion": [
            ("ओह मजहब वाला लोगन के टोला से भगा दऽ।", "severe", True, 0, "political_speech", "religious", "community"),
            ("ओह धरम वाला लोग हमेशा गड़बड़ करे ला।", "moderate", False, 0, "social_media", "religious", "community"),
        ],
        "caste": [
            ("ओह जात के लोग पंचायत में ना घुसे।", "moderate", True, 0, "chat", "political", "community"),
            ("नीच जात वाला पर भरोसा मत करा।", "moderate", False, 1, "chat", "general", "community"),
        ],
        "nationality": [
            ("बाहिर से आइल लोगन के गांव से निकाल दऽ।", "severe", True, 0, "news", "political", "community"),
            ("परदेसी लोग इहाँ के माहौल बिगाड़ देला।", "moderate", False, 0, "news", "political", "community"),
        ],
        "political": [
            ("ओह पार्टी के चमचा सभ के कुचल दऽ।", "severe", True, 0, "political_speech", "political", "ideology"),
            ("ओह सोच वाला लोग समाज पर कलंक बा।", "moderate", False, 0, "social_media", "political", "ideology"),
        ],
        "individual": [
            ("तू हरामी आदमी बाड़ऽ, तोहरा के मेटा देवे के चाहीं।", "severe", True, 1, "social_media", "general", "individual"),
            ("ओ आदमी पूरा गांव खातिर जहर बा।", "moderate", False, 0, "chat", "general", "individual"),
        ],
    },
    "implicit": {
        "gender": [("मेहरारू लोग जिम्मेदारी पावत ही गड़बड़ करे लागेला।", 0, "news", "general", "community")],
        "religion": [("ओह समुदाय के लोग मौका पावत ही असली रंग देखावेला।", 0, "chat", "religious", "community")],
        "caste": [("कुछ घर के पहचान बोलचाल से तुरंते हो जाला।", 0, "chat", "general", "community")],
        "nationality": [("परदेसी लोग अइलें कि टोला कम सुरक्षित लागे लागेला।", 0, "news", "political", "community")],
        "political": [("ओह दल वाला लोग से दूरी बनवले ठीक बा।", 0, "social_media", "political", "ideology")],
        "individual": [("ओके देखते माहौलिये खराब हो जाला।", 0, "chat", "general", "individual")],
    },
    "sarcasm": {
        "gender": [("हाँ हाँ, मेहरारू लोग त बड़ा ठंढा दिमाग से फैसला लेले, ना?", 0, "social_media", "general", "community")],
        "religion": [("वाह, ओह समुदाय के सहनशीलता त बड़ा नामी बा।", 0, "social_media", "religious", "community")],
        "caste": [("बिलकुल, जाति देख के भेदभाव त कहीं होला ही ना।", 0, "chat", "political", "community")],
        "nationality": [("हाँ, परदेसी लोग आके सबके रोजी बढ़ा देला, है ना?", 0, "social_media", "political", "community")],
        "political": [("का बढ़िया विचार बा, बस नफरतिए फइलावे ला।", 0, "news", "political", "ideology")],
        "individual": [("वाह, उ आदमी त बड़ा नेक बा, सभे के जीवन खराब करेला।", 0, "chat", "general", "individual")],
    },
}

MARWARI = {
    "counts": {"hate": 40, "non_hate": 45, "offensive": 7, "health_issue": 8},
    "implicit_count": 8,
    "sarcasm_count": 10,
    "region_non_hate": ["rural_india"],
    "region_other": ["rural_india"],
    "region_hate": ["rural_india"],
    "annotator_non_hate": ["synthetic", "synthetic", "synthetic", "A1"],
    "annotator_other": ["synthetic", "synthetic", "A1"],
    "annotator_hate": ["synthetic", "synthetic", "synthetic", "A1"],
    "nh_prefix": ["आज", "म्हे", "घरे", "खेत में", "गांव में", "डॉक्टर साहब कह्या", "स्कूल में"],
    "nh_topic": [
        "सुबेरो ठंडो पवन में घूम्या",
        "गरम चाय सूं नाश्तो कर्यो",
        "क्रिकेट री बात करां",
        "बालकां नै पढ़ाई में मदद करी",
        "मेह बरसां पाछो माटी री खुशबू आई",
        "कुटुंब सूं भोजन बनायो",
        "सेहत जांच रो कागद देख्यो",
    ],
    "nh_suffix": ["।", " मन ने घणो सुख मिल्यो।", " सब हंस पड़्या।", " दिन बढ़ियो गयो।"],
    "offensive": [
        ("थूं घणो बेवकूफ है, चुप रह।", 1),
        ("ई घणी घटिया बकवास है।", 1),
        ("ओ रो दिमाग खातर गईलो लागे है।", 1),
        ("फालतू रो शोर मत मचा।", 1),
    ],
    "health": [
        "म्हारी छाती में काल सूं दुखाव है।",
        "दू दिन सूं ताप अणे बदन दुखे है।",
        "गळो सूज गयो है अणे निगलता पीर होवे है।",
        "बार बार चक्कर आवे है।",
        "पीठ में तेज पीर है।",
    ],
    "hate_context": ["", "ऑनलाइन,", "सभा में,"],
    "direct": {
        "gender": [
            ("ई औरतां नै बड़ा फैसला सूं दूर राखो।", "moderate", True, 0, "social_media", "general", "community"),
            ("ई लुगायां बस रसोई खातर ठीक है।", "moderate", False, 0, "chat", "general", "community"),
        ],
        "religion": [
            ("ओ धरम वालां नै मोहल्ला सूं बाहर काढ़ द्यो।", "severe", True, 0, "political_speech", "religious", "community"),
            ("ओ पंथ वालां सूं सगळी गड़बड़ होवे है।", "moderate", False, 0, "social_media", "religious", "community"),
        ],
        "caste": [
            ("ओ जात वालां नै पंचायत में मत घुसण द्यो।", "moderate", True, 0, "chat", "political", "community"),
            ("नीच जात वालां पर भरोसो मत करो।", "moderate", False, 1, "chat", "general", "community"),
        ],
        "nationality": [
            ("बाहरा वालां नै गांव सूं निकाल द्यो।", "severe", True, 0, "news", "political", "community"),
            ("परदेसिया आके गांव रो माहौल बिगाड़े है।", "moderate", False, 0, "news", "political", "community"),
        ],
        "political": [
            ("ओ पार्टी रा चमचा नै कुचल द्यो।", "severe", True, 0, "political_speech", "political", "ideology"),
            ("ओ सोच वालां समाज पर धब्बो है।", "moderate", False, 0, "social_media", "political", "ideology"),
        ],
        "individual": [
            ("थूं हरामी मानस है, थाने मेट द्यां।", "severe", True, 1, "social_media", "general", "individual"),
            ("ओ मानस सगळा गांव खातर जहर है।", "moderate", False, 0, "chat", "general", "individual"),
        ],
    },
    "implicit": {
        "gender": [("लुगायां नै जिम्मेदारी मिलते ही गड़बड़ चालू हो जावे है।", 0, "news", "general", "community")],
        "religion": [("ओ समुदाय रो रंग मौका मिलते ही दिख जावे है।", 0, "chat", "religious", "community")],
        "caste": [("कुच्छ घराणी री पहचान बात सूं ही लाग जावे है।", 0, "chat", "general", "community")],
        "nationality": [("परदेसिया आवे तो गांव कम सुरक्षित लागे है।", 0, "news", "political", "community")],
        "political": [("ओ दल वालां सूं दूरी राखणी चोखी है।", 0, "social_media", "political", "ideology")],
        "individual": [("ओ आवे तो सगळो माहौल खराब हो जावे है।", 0, "chat", "general", "individual")],
    },
    "sarcasm": {
        "gender": [("हाँ हाँ, लुगायां त घणा ठंडा दिमाग सूं फैसला लेवे है, है ना?", 0, "social_media", "general", "community")],
        "religion": [("वाह, ओ समुदाय री सहनशीलता तो घणी मशहूर है।", 0, "social_media", "religious", "community")],
        "caste": [("बिलकुल, जात देख के भेदभाव तो कदे होवे ही ना।", 0, "chat", "political", "community")],
        "nationality": [("हाँ, परदेसिया आवे अणे सबने रोजी दे जावे, है ना?", 0, "social_media", "political", "community")],
        "political": [("कितनी सुंदर सोच है, बस नफरत फैलावे है।", 0, "news", "political", "ideology")],
        "individual": [("वाह, ओ मानस तो घणो नेक है, सबरो जीवन खराब करे है।", 0, "chat", "general", "individual")],
    },
}


def main():
    base = Path(__file__).resolve().parents[1] / "src" / "datasets"
    datasets = {
        "english.csv": ENGLISH,
        "hindi.csv": HINDI,
        "marathi.csv": MARATHI,
        "bhojpuri.csv": BHOJPURI,
        "marwari.csv": MARWARI,
    }
    for name, spec in datasets.items():
        with (base / name).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(build_rows(spec))
        print(f"Wrote {name}")


if __name__ == "__main__":
    main()
