"""
Weather & Risk Fusion Module with Full Multilingual Explainable AI (XAI) Support
Fuses Image AI detection + Weather (Temp/Humidity) + Crop Growth Stage + IoT Pest Trap counts
to calculate a unified Farm Risk Score with localized XAI signal breakdowns in Hindi, Telugu, Punjabi, and English.
"""

from typing import Dict, Any
from backend.app.ai.labels import DISEASE_KNOWLEDGE_BASE
from backend.app.config import HIGH_RISK_THRESHOLD, MEDIUM_RISK_THRESHOLD

class RiskFusionEngine:

    @staticmethod
    def calculate_risk(
        disease_id: str,
        ai_confidence: float,
        temperature_c: float = 28.5,
        humidity_pct: float = 85.0,
        growth_stage: str = "vegetative",
        iot_trap_count: int = 42,
        lang: str = "hi"
    ) -> Dict[str, Any]:

        lang = lang.lower() if lang.lower() in ["hi", "te", "pa", "en"] else "hi"
        disease_info = DISEASE_KNOWLEDGE_BASE.get(disease_id, DISEASE_KNOWLEDGE_BASE["healthy"])
        base_severity = disease_info.get("base_severity", 0.1)
        disease_name = disease_info.get(f"name_{lang}", disease_info["name_en"])

        # 1. AI Image Risk Signal (0.0 to 1.0)
        ai_risk_signal = base_severity * ai_confidence

        # 2. Weather Favorability Signal & Multilingual Signal Text
        if humidity_pct > 80:
            weather_risk = 0.85
            weather_reasons = {
                "hi": f"अत्यधिक नमी ({humidity_pct}%) कवक बीजाणुओं के अंकुरण को तेजी से बढ़ाती है।",
                "te": f"అధిక తేమ ({humidity_pct}%) శిలీంధ్ర బీజాల వృద్ధిని వేగవంతం చేస్తుంది.",
                "pa": f"ਜ਼ਿਆਦਾ ਸਿੱਲ੍ਹ ({humidity_pct}%) ਉੱਲੀ ਦੇ ਬੀਜਾਣੂਆਂ ਨੂੰ ਤੇਜ਼ੀ ਨਾਲ ਵਧਾਉਂਦੀ ਹੈ।",
                "en": f"High humidity ({humidity_pct}%) promotes rapid fungal spore germination."
            }
        elif humidity_pct > 65:
            weather_risk = 0.55
            weather_reasons = {
                "hi": f"मध्यम नमी ({humidity_pct}%) रोग फैलने के लिए अनुकूल है।",
                "te": f"సాధారణ తేమ ({humidity_pct}%) తెగులు వ్యాప్తికి అనుకూలం.",
                "pa": f"ਦਰਮਿਆਨੀ ਸਿੱਲ੍ਹ ({humidity_pct}%) ਬੀਮਾਰੀ ਫੈਲਣ ਲਈ ਅਨੁਕੂਲ ਹੈ।",
                "en": f"Moderate humidity ({humidity_pct}%) maintains favorable disease spread."
            }
        else:
            weather_risk = 0.20
            weather_reasons = {
                "hi": f"कम नमी ({humidity_pct}%) कवक प्रजनन को दबाती है।",
                "te": f"తక్కువ తేమ ({humidity_pct}%) తెగులు వ్యాప్తిని నిరోధిస్తుంది.",
                "pa": f"ਘੱਟ ਸਿੱਲ੍ਹ ({humidity_pct}%) ਬੀਮਾਰੀ ਨੂੰ ਰੋਕਦੀ ਹੈ।",
                "en": f"Low humidity ({humidity_pct}%) suppresses active fungal reproduction."
            }

        weather_reason = weather_reasons.get(lang, weather_reasons["en"])

        if 20.0 <= temperature_c <= 32.0:
            weather_risk = min(1.0, weather_risk + 0.10)

        # 3. Crop Growth Stage Vulnerability & Multilingual Text
        stage_reasons_map = {
            "seedling": {
                "hi": "अंकुरण चरण में पौधे के छोटे ऊतक संक्रमण के प्रति बहुत संवेदनशील होते हैं।",
                "te": "మొలక దశలో పసి మొక్కలు తెగుళ్ళకు త్వరగా గురవుతాయి.",
                "pa": "ਅੰਕੁਰਨ ਪੜਾਅ ਵਿੱਚ ਛੋਟੇ ਪੌਦੇ ਬੀਮਾਰੀਆਂ ਲਈ ਬਹੁਤ ਸੰਵੇਦਨਸ਼ੀਲ ਹੁੰਦੇ ਹਨ।",
                "en": "Seedlings have fragile tissue vulnerable to systemic infection."
            },
            "vegetative": {
                "hi": "वानस्पतिक चरण में सघन पत्तियां कीटों और झुलसा रोग के लिए अनुकूल वातावरण बनाती हैं।",
                "te": "శాఖీయ దశలో దట్టమైన ఆకులు కీటకాలు మరియు బ్లైట్ వ్యాప్తికి అనుకూలం.",
                "pa": "ਵਨਸਪਤੀ ਪੜਾਅ ਵਿੱਚ ਸੰਘਣੇ ਪੱਤੇ ਕੀੜਿਆਂ ਅਤੇ ਝੁਲਸ ਰੋਗ ਲਈ ਅਨੁਕੂਲ ਮੌਸਮ ਬਣਾਉਂਦੇ ਹਨ।",
                "en": "Vegetative canopy density creates humid micro-climate for pests/blight."
            },
            "flowering": {
                "hi": "फूल आने का चरण अत्यंत महत्वपूर्ण है; संक्रमण से सीधा उपज का नुकसान होता है।",
                "te": "పూత దశ అత్యంత సున్నితమైనది; తెగులు సోకితే నేరుగా దిగుబడి తగ్గుతుంది.",
                "pa": "ਫੁੱਲ ਆਉਣ ਦਾ ਪੜਾਅ ਬਹੁਤ ਮਹੱਤਵਪੂਰਨ ਹੈ; ਬੀਮਾਰੀ ਨਾਲ ਸਿੱਧਾ ਝਾੜ ਘਟਦਾ ਹੈ।",
                "en": "Flowering stage is critical; infections cause direct yield loss."
            },
            "fruiting": {
                "hi": "फल/दाना बनने के चरण में फल सड़न और बीजाणु क्षति का जोखिम रहता है।",
                "te": "కాయ దశలో కాయ కుళ్ళు మరియు స్పోర్ డ్యామేజ్ రిస్క్ ఉంటుంది.",
                "pa": "ਫਲ/ਦਾਣਾ ਬਣਨ ਦੇ ਪੜਾਅ ਵਿੱਚ ਫਲ ਸੜਨ ਦਾ ਖਤਰਾ ਰਹਿੰਦਾ ਹੈ।",
                "en": "Fruiting stage vulnerable to fruit rot and late-stage spore damage."
            }
        }
        
        stage_key = growth_stage.lower() if growth_stage.lower() in stage_reasons_map else "vegetative"
        stage_risk = 0.85 if stage_key == "vegetative" else (0.90 if stage_key == "flowering" else 0.75)
        stage_reason = stage_reasons_map[stage_key].get(lang, stage_reasons_map[stage_key]["en"])

        # 4. Simulated IoT Pest Trap Count Signal & Multilingual Text
        if iot_trap_count > 50:
            iot_risk = 0.90
            iot_reasons = {
                "hi": f"उच्च आईओटी कीट ट्रैप संख्या ({iot_trap_count} कीट/दिन) सक्रिय कीट प्रकोप का संकेत देती है।",
                "te": f"అధిక IoT కీటకాల సంఖ్య ({iot_trap_count} కీటకాలు/రోజు) తీవ్రమైన కీటకాల ఉధృతిని సూచిస్తుంది.",
                "pa": f"ਉੱਚ IoT ਕੀੜੇ ਟਰੈਪ ਗਿਣਤੀ ({iot_trap_count} ਕੀੜੇ/ਦਿਨ) ਕੀੜਿਆਂ ਦੇ ਫੈਲਾਅ ਦਾ ਸੰਕੇਤ ਦਿੰਦੀ ਹੈ।",
                "en": f"High IoT pest trap count ({iot_trap_count} pests/trap/day) signals active pest surge."
            }
        elif iot_trap_count > 25:
            iot_risk = 0.55
            iot_reasons = {
                "hi": f"बढ़ी हुई कीट संख्या ({iot_trap_count} कीट/दिन) शुरुआती कीट संचय को दर्शाती है।",
                "te": f"పెరిగిన కీటకాల సంఖ్య ({iot_trap_count} కీటకాలు/రోజు) ప్రారంభ కీటకాల చేరికను సూచిస్తుంది.",
                "pa": f"ਵਧੀ ਹੋਈ ਕੀੜਿਆਂ ਦੀ ਗਿਣਤੀ ({iot_trap_count} ਕੀੜੇ/ਦਿਨ) ਸ਼ੁਰੂਆਤੀ ਵਾਧੇ ਨੂੰ ਦਰਸਾਉਂਦੀ ਹੈ।",
                "en": f"Elevated IoT trap count ({iot_trap_count} pests/trap/day) indicates early pest buildup."
            }
        else:
            iot_risk = 0.20
            iot_reasons = {
                "hi": f"सामान्य कीट संख्या ({iot_trap_count} कीट/दिन) कम कीट दबाव दर्शाती है।",
                "te": f"సాధారణ కీటకాల సంఖ్య ({iot_trap_count} కీటకాలు/రోజు) తక్కువ కీటకాల ఒత్తిడిని సూచిస్తుంది.",
                "pa": f"ਸਧਾਰਨ ਕੀੜਿਆਂ ਦੀ ਗਿਣਤੀ ({iot_trap_count} ਕੀੜੇ/ਦਿਨ) ਘੱਟ ਖਤਰੇ ਨੂੰ ਦਰਸਾਉਂਦੀ ਹੈ।",
                "en": f"Normal IoT trap count ({iot_trap_count} pests/trap/day) shows low pest pressure."
            }

        iot_reason = iot_reasons.get(lang, iot_reasons["en"])

        # Weighted Fusion Calculation
        w_ai, w_weather, w_stage, w_iot = 0.45, 0.25, 0.15, 0.15

        if disease_id == "healthy":
            fusion_score = (ai_risk_signal * 0.5) + (weather_risk * 0.15) + (iot_risk * 0.15)
        else:
            fusion_score = (w_ai * ai_risk_signal) + (w_weather * weather_risk) + (w_stage * stage_risk) + (w_iot * iot_risk)

        fusion_score = round(float(min(1.0, max(0.0, fusion_score))), 2)

        # Risk Classification Level
        if fusion_score >= HIGH_RISK_THRESHOLD:
            risk_level = "High"
            risk_color = "#DC2626"
        elif fusion_score >= MEDIUM_RISK_THRESHOLD:
            risk_level = "Medium"
            risk_color = "#D97706"
        else:
            risk_level = "Low"
            risk_color = "#16A34A"

        # Localized Factor Titles
        factor_titles = {
            "ai": {
                "hi": "एआई लक्षण पहचान",
                "te": "AI లక్షణాల గుర్తింపు",
                "pa": "AI ਲੱਛਣ ਪਛਾਣ",
                "en": "Image AI Symptom Detection"
            },
            "weather": {
                "hi": "सूक्ष्म-जलवायु मौसम",
                "te": "సూక్ష్మ-వాతావరణం",
                "pa": "ਸੂਖਮ-ਜਲਵਾਯੂ ਮੌਸਮ",
                "en": "Micro-Climate Weather"
            },
            "stage": {
                "hi": "फसल चरण संवेदनशीलता",
                "te": "పంట దశ సున్నితత్వం",
                "pa": "ਫਸਲ ਪੜਾਅ ਸੰਵੇਦਨਸ਼ੀਲਤਾ",
                "en": "Crop Stage Sensitivity"
            },
            "iot": {
                "hi": "आईओटी कीट ट्रैप सेंसर",
                "te": "IoT కీటకాల ట్రాప్ సెన్సార్",
                "pa": "IoT ਕੀੜੇ ਟਰੈਪ ਸੈਂਸਰ",
                "en": "IoT Pest Trap Sensor"
            }
        }

        ai_signal_text = {
            "hi": f"{disease_name} का {int(ai_confidence*100)}% सटीकता के साथ पता चला।",
            "te": f"{disease_name} తెగులు {int(ai_confidence*100)}% ఖచ్చితత్వంతో గుర్తించబడింది.",
            "pa": f"{disease_name} ਦੀ {int(ai_confidence*100)}% ਸਟੀਕਤਾ ਨਾਲ ਪਛਾਣ ਹੋਈ।",
            "en": f"{disease_name} detected with {int(ai_confidence*100)}% confidence."
        }

        # Localized XAI Breakdown
        xai_breakdown = [
            {
                "factor": factor_titles["ai"].get(lang, factor_titles["ai"]["en"]),
                "weight": "45%",
                "signal": ai_signal_text.get(lang, ai_signal_text["en"]),
                "score": round(ai_risk_signal, 2)
            },
            {
                "factor": factor_titles["weather"].get(lang, factor_titles["weather"]["en"]),
                "weight": "25%",
                "signal": weather_reason,
                "score": round(weather_risk, 2)
            },
            {
                "factor": factor_titles["stage"].get(lang, factor_titles["stage"]["en"]),
                "weight": "15%",
                "signal": stage_reason,
                "score": round(stage_risk, 2)
            },
            {
                "factor": factor_titles["iot"].get(lang, factor_titles["iot"]["en"]),
                "weight": "15%",
                "signal": iot_reason,
                "score": round(iot_risk, 2)
            }
        ]

        summary_reason = (
            f"Overall {risk_level} risk score of {int(fusion_score*100)}%. "
            f"Primary risk driver: {disease_name}. {weather_reason}"
        )

        return {
            "farm_risk_score": fusion_score,
            "risk_level": risk_level,
            "risk_color": risk_color,
            "summary_explanation": summary_reason,
            "xai_breakdown": xai_breakdown,
            "inputs": {
                "disease_id": disease_id,
                "temperature_c": temperature_c,
                "humidity_pct": humidity_pct,
                "growth_stage": growth_stage,
                "iot_trap_count": iot_trap_count
            }
        }
