"""
Crop Disease Knowledge Base & Multilingual Advisory Rules
Supports Rice, Wheat, Cotton, Tomato, Potato, Maize, Sugarcane & Healthy crops.
Languages: English (en), Hindi (hi), Telugu (te), Punjabi (pa).
"""

DISEASE_KNOWLEDGE_BASE = {
    "rice_blast": {
        "id": "rice_blast",
        "crop": "rice",
        "name_en": "Rice Blast (Magnaporthe oryzae)",
        "name_hi": "धान का झुलसा रोग (राइस ब्लास्ट)",
        "name_te": "వరి అగ్గి తెగులు (రైస్ బ్లాస్ట్)",
        "name_pa": "ਝੋਨੇ ਦਾ ਬਲਾਸਟ ਰੋਗ",
        "base_severity": 0.85,
        "symptoms": "Spindle-shaped lesions on leaves with gray/white centers and reddish-brown borders.",
        "dos": [
            {"en": "Apply recommended fungicide (Tricyclazole 75% WP @ 0.6g/L) at initial symptom onset.",
             "hi": "शुरुआती लक्षण दिखने पर अनुशंसित कवकनाशी (ट्राइसाइक्लाज़ोल 75% WP @ 0.6 ग्राम/लीटर) का छिड़काव करें।",
             "te": "తొలి దశలో సిఫార్సు చేసిన శిలీంధ్ర నాశిని (ట్రైసైక్లాజోల్ 75% WP @ 0.6 గ్రా/లీ) పిచికారీ చేయండి.",
             "pa": "ਸ਼ੁਰੂਆਤੀ ਲੱਛਣ ਦਿਸਣ 'ਤੇ ਸਿਫਾਰਿਸ਼ ਕੀਤੀ ਫੰਗਸਨਾਸ਼ਕ (ਟ੍ਰਾਈਸਾਈਕਲਾਜ਼ੋਲ 75% WP @ 0.6 ਗ੍ਰਾਮ/ਲੀਟਰ) ਦਾ ਛਿੜਕਾਅ ਕਰੋ।"},
            {"en": "Maintain balanced nitrogen application in split doses.",
             "hi": "नाइट्रोजन उर्वरक का संतुलित उपयोग किस्तों में करें।",
             "te": "నత్రజని ఎరువులను విడతలవారీగా సమతుల్యంగా వాడండి.",
             "pa": "ਨਾਇਟ੍ਰੋਜਨ ਦੀ ਸੰਤੁਲਿਤ ਖਾਦ ਕਿਸ਼ਤਾਂ ਵਿੱਚ ਪਾਓ।"}
        ],
        "donts": [
            {"en": "Do not flood fields continuously; practice alternate wetting and drying.",
             "hi": "खेत में लगातार पानी भरा न रखें; बारी-बारी से सिंचाई करें।",
             "te": "పొలంలో నిరంతరం నీరు ఉంచవద్దు; మార్చి మార్చి తడి ఆరబెట్టే పద్ధతి పాటించండి.",
             "pa": "ਖੇਤ ਵਿੱਚ ਲਗਾਤਾਰ ਪਾਣੀ ਖੜ੍ਹਾ ਨਾ ਰੱਖੋ।"},
            {"en": "Do not apply excessive nitrogen fertilizer during humid weather.",
             "hi": "नमी वाले मौसम में अत्यधिक नाइट्रोजन न डालें।",
             "te": "తేమతో కూడిన వాతావరణంలో అధిక నత్రజని వాడవద్దు.",
             "pa": "ਸਿੱਲ੍ਹੇ ਮੌਸਮ ਵਿੱਚ ਬਹੁਤ ਜ਼ਿਆਦਾ ਨਾਇਟ੍ਰੋਜਨ ਨਾ ਪਾਓ।"}
        ],
        "chemical_treatment": {
            "pesticide": "Tricyclazole 75% WP / Isoprothiolane 40% EC",
            "dosage": "0.6 g per Liter of water (or 120 g per acre in 200L water)",
            "safety_period": "Wait 21 days before harvest after final spray",
            "protective_gear": "Wear gloves, safety mask, and protective eye gear during mixing and spraying."
        },
        "organic_treatment": "Spray Neem oil (10,000 ppm) @ 3 ml/L or Pseudomonas fluorescens @ 10 g/L."
    },
    "wheat_yellow_rust": {
        "id": "wheat_yellow_rust",
        "crop": "wheat",
        "name_en": "Wheat Yellow Rust (Puccinia striiformis)",
        "name_hi": "गेहूं का पीला रतुआ (येलो रस्ट)",
        "name_te": "గోధుమ పసుపు రంగు తెగులు",
        "name_pa": "ਕਣਕ ਦਾ ਪੀਲਾ ਰਤੂਆ",
        "base_severity": 0.88,
        "symptoms": "Yellow stripes of pustules arranged parallel along leaf veins.",
        "dos": [
            {"en": "Spray Propiconazole 25% EC @ 1 ml/L at first sign of yellow stripes.",
             "hi": "पीली धारियां दिखने पर प्रोपिकोनाज़ोल 25% EC @ 1 मिली/लीटर का तुरंत छिड़काव करें।",
             "te": "పసుపు గీతలు కనిపించిన వెంటనే ప్రొపికోనాజోల్ 25% EC @ 1 మి.లీ/లీ పిచికారీ చేయండి.",
             "pa": "ਪੀਲੀਆਂ ਧਾਰੀਆਂ ਦਿਸਣ 'ਤੇ ਪ੍ਰੋਪੀਕੋਨਾਜ਼ੋਲ 25% EC @ 1 ਮਿਲੀ/ਲੀਟਰ ਦਾ ਛਿੜਕਾਅ ਕਰੋ।"},
            {"en": "Monitor field borders daily during cold and humid winter mornings.",
             "hi": "ठंड और नमी भरे सुबह के समय खेत के किनारों की दैनिक निगरानी करें।",
             "te": "చల్లని, తేమతో కూడిన ఉదయాల్లో పొలం సరిహద్దులను ప్రతిరోజూ పరిశీలించండి.",
             "pa": "ਠੰਢ ਅਤੇ ਸਿੱਲ੍ਹੇ ਮੌਸਮ ਵਿੱਚ ਖੇਤਾਂ ਦੀ ਰੋਜ਼ਾਨਾ ਨਿਗਰਾਨੀ ਕਰੋ।"}
        ],
        "donts": [
            {"en": "Do not delay spraying once yellow rust spots appear; spores spread fast in wind.",
             "hi": "लक्षण दिखने पर छिड़काव में देरी न करें; हवा से बीजाणु तेजी से फैलते हैं।",
             "te": "లక్షణాలు కనిపించాక పిచికారీ ఆలస్యం చేయవద్దు; గాలి ద్వారా త్వరగా వ్యాపిస్తుంది.",
             "pa": "ਲੱਛਣ ਦਿਸਣ 'ਤੇ ਛਿੜਕਾਅ ਵਿੱਚ ਦੇਰੀ ਨਾ ਕਰੋ, ਇਹ ਹਵਾ ਨਾਲ ਤੇਜ਼ੀ ਨਾਲ ਫੈਲਦਾ ਹੈ।"}
        ],
        "chemical_treatment": {
            "pesticide": "Propiconazole 25% EC (Tilt)",
            "dosage": "1 ml per Liter of water (200 ml in 200L water per acre)",
            "safety_period": "Wait 30 days before harvest",
            "protective_gear": "Cover nose and mouth with mask, wear long sleeves."
        },
        "organic_treatment": "Foliar spray of Trichoderma viride @ 5g/L mixed with jaggery solution."
    },
    "tomato_late_blight": {
        "id": "tomato_late_blight",
        "crop": "tomato",
        "name_en": "Tomato Late Blight (Phytophthora infestans)",
        "name_hi": "टमाटर का पछैती झुलसा रोग",
        "name_te": "టమాటా లేట్ బ్లైట్ తెగులు",
        "name_pa": "ਟਮਾਟਰ ਦਾ ਪਛੇਤਾ ਝੁਲਸ ਰੋਗ",
        "base_severity": 0.90,
        "symptoms": "Water-soaked dark lesions on leaves and stems with white fungal mold under humid conditions.",
        "dos": [
            {"en": "Spray Mancozeb 75% WP @ 2.5 g/L as preventive measure or Cymoxanil + Mancozeb on infestation.",
             "hi": "बचाव के लिए मैनकोज़ेब 75% WP @ 2.5 ग्राम/लीटर या प्रकोप होने पर साइमोक्सानिल+मैनकोज़ेब का छिड़काव करें।",
             "te": "ముందస్తు జాగ్రత్తగా మ్యాంకోజెబ్ 2.5 గ్రా/లీ లేదా ఉధృతి ఉంటే సైమోక్సానిల్+మ్యాంకోజెబ్ చల్లండి.",
             "pa": "ਮੈਨਕੋਜ਼ੇਬ 75% WP @ 2.5 ਗ੍ਰਾਮ/ਲੀਟਰ ਦਾ ਛਿੜਕਾਅ ਕਰੋ।"}
        ],
        "donts": [
            {"en": "Do not leave infected plant debris in the field.",
             "hi": "संक्रमित पौधों के अवशेष खेत में न छोड़ें।",
             "te": "వ్యాధి సోకిన మొక్కల వ్యర్థాలను పొలంలో ఉంచవద్దు.",
             "pa": "ਬੀਮਾਰੀ ਵਾਲੇ ਪੌਦਿਆਂ ਦੇ ਰਹਿੰਦ-ਖੂੰਹਦ ਖੇਤ ਵਿੱਚ ਨਾ ਛੱਡੋ।"}
        ],
        "chemical_treatment": {
            "pesticide": "Mancozeb 75% WP / Metalaxyl + Mancozeb",
            "dosage": "2.5 g per Liter of water (500 g per acre)",
            "safety_period": "Wait 7 days before harvesting tomatoes",
            "protective_gear": "Use protective gloves, goggles, and face covering."
        },
        "organic_treatment": "Copper Oxychloride 50% WP @ 3 g/L or sour buttermilk spray (50 ml/L)."
    },
    "cotton_leaf_curl": {
        "id": "cotton_leaf_curl",
        "crop": "cotton",
        "name_en": "Cotton Leaf Curl Virus (CLCuV)",
        "name_hi": "कपास का पत्ता मरोड़ रोग (लीफ कर्ल)",
        "name_te": "ప్రత్తి ఆకు ముడుత తెగులు",
        "name_pa": "ਕਪਾਹ ਦਾ ਪੱਤਾ ਮਰੋੜ ਰੋਗ",
        "base_severity": 0.82,
        "symptoms": "Upward or downward curling of leaves with thickened veins and enations.",
        "dos": [
            {"en": "Control whitefly vector by spraying Afidopyropen 50 g/L DC @ 2 ml/L.",
             "hi": "सफेद मक्खी पर नियंत्रण के लिए एफिडोपायरोपेन @ 2 मिली/लीटर का छिड़काव करें।",
             "te": "తెల్లదోమ నివారణకు అఫిడోపైరోపెన్ @ 2 మి.లీ/లీ పిచికారీ చేయండి.",
             "pa": "ਚਿੱਟੀ ਮੱਖੀ ਦੇ ਕੰਟਰੋਲ ਲਈ ਐਫੀਡੋਪਾਇਰੋਪੇਨ ਦਾ ਛਿੜਕਾਅ ਕਰੋ।"}
        ],
        "donts": [
            {"en": "Do not allow weed hosts (like Kanghi booti) to grow near field borders.",
             "hi": "खेत के आसपास खरपतवार न उगने दें।",
             "te": "పొలం గట్లపై కలుపు మొక్కలను పెరగనివ్వవద్దు.",
             "pa": "ਖੇਤ ਦੇ ਆਲੇ-ਦੁਆਲੇ ਨਦੀਨ ਨਾ ਉੱਗਣ ਦਿਓ।"}
        ],
        "chemical_treatment": {
            "pesticide": "Diafenthiuron 50% WP / Spiromesifen 22.9% SC",
            "dosage": "1.25 g per Liter of water",
            "safety_period": "Wait 14 days before next picking",
            "protective_gear": "Full rubber gloves and protective breathing mask."
        },
        "organic_treatment": "Yellow sticky traps (15-20 per acre) and Neem seed kernel extract (5%)."
    },
    "potato_early_blight": {
        "id": "potato_early_blight",
        "crop": "potato",
        "name_en": "Potato Early Blight (Alternaria solani)",
        "name_hi": "आलू का अगेती झुलसा रोग",
        "name_te": "బంగాళాదుంప ముందస్తు బ్లైట్",
        "name_pa": "ਆਲੂ ਦਾ ਅਗੇਤਾ ਝੁਲਸ ਰੋਗ",
        "base_severity": 0.75,
        "symptoms": "Concentric rings ('target board' pattern) on lower leaves.",
        "dos": [
            {"en": "Spray Chlorothalonil 75% WP @ 2 g/L or Azoxystrobin + Difenoconazole.",
             "hi": "क्लोरोथेलोनिल 75% WP @ 2 ग्राम/लीटर का छिड़काव करें।",
             "te": "క్లోరోథలోనిల్ 75% WP @ 2 గ్రా/లీ పిచికారీ చేయండి.",
             "pa": "ਕਲੋਰੋਥੈਲੋਨਿਲ 75% WP @ 2 ਗ੍ਰਾਮ/ਲੀਟਰ ਦਾ ਛਿੜਕਾਅ ਕਰੋ।"}
        ],
        "donts": [
            {"en": "Do not overhead irrigate in late afternoon.",
             "hi": "देर शाम को ऊपर से सिंचाई न करें।",
             "te": "సాయంత్రం వేళల్లో పైనుండి నీరు పెట్టవద్దు.",
             "pa": "ਸ਼ਾਮ ਵੇਲੇ ਫੁਹਾਰਾ ਸਿੰਚਾਈ ਨਾ ਕਰੋ।"}
        ],
        "chemical_treatment": {
            "pesticide": "Chlorothalonil 75% WP",
            "dosage": "2.0 g per Liter of water",
            "safety_period": "Wait 14 days before harvest",
            "protective_gear": "Safety glasses, mask, gloves."
        },
        "organic_treatment": "Bordeaux mixture (1%) or Bacillus subtilis bio-fungicide @ 5 g/L."
    },
    "healthy": {
        "id": "healthy",
        "crop": "general",
        "name_en": "Healthy Crop (No Disease Detected)",
        "name_hi": "स्वास्थ्य फसल (कोई रोग नहीं मिला)",
        "name_te": "ఆరోగ్యకరమైన పంట (ఎలాంటి తెగులు లేదు)",
        "name_pa": "ਸਿਹਤਮੰਦ ਫਸਲ (ਕੋਈ ਬੀਮਾਰੀ ਨਹੀਂ)",
        "base_severity": 0.05,
        "symptoms": "Vibrant green leaves, uniform growth, no dark spots, rust, or wilting.",
        "dos": [
            {"en": "Continue regular nutrient management and soil moisture maintenance.",
             "hi": "नियमित पोषण प्रबंधन और मृदा नमी बनाए रखें।",
             "te": "క్రమబద్ధమైన పోషకాల యాజమాన్యం మరియు తేమ నిర్వహణ కొనసాగించండి.",
             "pa": "ਸੰਤੁਲਿਤ ਖਾਦਾਂ ਅਤੇ ਪਾਣੀ ਦੀ ਸੰਭਾਲ ਜਾਰੀ ਰੱਖੋ।"}
        ],
        "donts": [
            {"en": "Do not apply unnecessary chemical pesticides.",
             "hi": "अनावश्यक रासायनिक कीटनाशकों का प्रयोग न करें।",
             "te": "అవసరం లేని రసాయన పురుగుమందులను వాడవద్దు.",
             "pa": "ਬਿਨਾਂ ਲੋੜ ਤੋਂ ਰਸਾਇਣਕ ਕੀਟਨਾਸ਼ਕਾਂ ਦੀ ਵਰਤੋਂ ਨਾ ਕਰੋ।"}
        ],
        "chemical_treatment": {
            "pesticide": "None required",
            "dosage": "N/A",
            "safety_period": "N/A",
            "protective_gear": "N/A"
        },
        "organic_treatment": "Routine bio-fertilizer spray (Panchagavya or Vermicompost wash)."
    }
}
