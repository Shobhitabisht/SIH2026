"""
Unit tests for AI Image Classification and Advisory Knowledge Base
"""

import pytest
from backend.app.ai.classifier import classifier
from backend.app.ai.labels import DISEASE_KNOWLEDGE_BASE

def test_knowledge_base_classes():
    assert "rice_blast" in DISEASE_KNOWLEDGE_BASE
    assert "wheat_yellow_rust" in DISEASE_KNOWLEDGE_BASE
    assert "tomato_late_blight" in DISEASE_KNOWLEDGE_BASE
    assert "healthy" in DISEASE_KNOWLEDGE_BASE

def test_classifier_predict_fallback():
    # Test with dummy image bytes
    dummy_bytes = b"fake_image_data"
    result = classifier.predict(dummy_bytes, crop_hint="rice")
    assert "disease_id" in result
    assert "confidence" in result
    assert result["confidence"] > 0.0
