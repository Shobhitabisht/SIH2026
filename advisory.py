"""
Multilingual Advisory Generation Module
Delivers structured Do/Do-Not guidelines, chemical/organic treatment dosages,
and audio voice synthesis payloads in Hindi, Telugu, Punjabi, and English.
"""

from typing import Dict, Any, List
from backend.app.ai.labels import DISEASE_KNOWLEDGE_BASE

class AdvisoryEngine:

    @staticmethod
    def generate_advisory(disease_id: str, lang: str = "hi") -> Dict[str, Any]:
        disease = DISEASE_KNOWLEDGE_BASE.get(disease_id, DISEASE_KNOWLEDGE_BASE["healthy"])
        lang = lang.lower() if lang.lower() in ["hi", "te", "pa", "en"] else "hi"

        # Disease name in target language
        disease_name = disease.get(f"name_{lang}", disease["name_en"])

        # Extract localized Do's & Don'ts
        dos = [item.get(lang, item["en"]) for item in disease.get("dos", [])]
        donts = [item.get(lang, item["en"]) for item in disease.get("donts", [])]

        chem = disease.get("chemical_treatment", {})
        organic = disease.get("organic_treatment", "")

        # Generate voice speech script tailored to language
        if lang == "hi":
            voice_script = (
                f"किसान भाई, आपकी फसल में {disease_name} के लक्षण पाए गए हैं। "
                f"तुरंत उपचार के लिए: {dos[0] if dos else 'उचित कवकनाशी का प्रयोग करें।'} "
                f"सावधानी: {donts[0] if donts else 'खेत में पानी जमा न होने दें।'}"
            )
        elif lang == "te":
            voice_script = (
                f"రైతు సోదరా, మీ పంటలో {disease_name} లక్షణాలు గుర్తించబడ్డాయి. "
                f"తక్షణ నివారణ చర్య: {dos[0] if dos else 'సిఫార్సు చేసిన మందులను పిచికారీ చేయండి.'} "
                f"జాగ్రత్త: {donts[0] if donts else 'పొలంలో నీరు ఎక్కువగా ఉంచవద్దు.'}"
            )
        elif lang == "pa":
            voice_script = (
                f"ਕਿਸਾਨ ਵੀਰੋ, ਤੁਹਾਡੀ ਫਸਲ ਵਿੱਚ {disease_name} ਦੇ ਲੱਛਣ ਮਿਲੇ ਹਨ। "
                f"ਤੁਰੰਤ ਇਲਾਜ: {dos[0] if dos else 'ਢੁਕਵੀਂ ਦਵਾਈ ਦਾ ਛਿੜਕਾਅ ਕਰੋ।'} "
                f"ਸਾਵਧਾਨੀ: {donts[0] if donts else 'ਖੇਤ ਵਿੱਚ ਵਾਧੂ ਪਾਣੀ ਨਾ ਖੜ੍ਹਾ ਕਰੋ।'}"
            )
        else: # English
            voice_script = (
                f"Attention Farmer: Symptoms of {disease_name} detected in your crop. "
                f"Recommended Action: {dos[0] if dos else 'Apply prescribed treatment immediately.'} "
                f"Precaution: {donts[0] if donts else 'Avoid excess waterlogging.'}"
            )

        return {
            "disease_id": disease_id,
            "language": lang,
            "disease_name": disease_name,
            "symptoms": disease.get("symptoms", ""),
            "dos": dos,
            "donts": donts,
            "treatment": {
                "chemical": chem,
                "organic": organic
            },
            "voice_advisory": {
                "lang": lang,
                "text": voice_script
            }
        }
