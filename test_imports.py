#!/usr/bin/env python3
"""
Test script to verify all package imports work correctly with the latest versions
"""

def test_moviepy_import():
    """Test MoviePy v2.0+ imports"""
    try:
        from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip, concatenate_audioclips
        from moviepy import SpeedEffect, AudioClip
        print("✅ MoviePy v2.0+ imports successful")
        return True
    except ImportError as e:
        print(f"❌ MoviePy import failed: {e}")
        return False

def test_openai_import():
    """Test OpenAI v1.0+ imports"""
    try:
        from openai import OpenAI
        print("✅ OpenAI v1.0+ imports successful")
        return True
    except ImportError as e:
        print(f"❌ OpenAI import failed: {e}")
        return False

def test_elevenlabs_import():
    """Test ElevenLabs v1.0+ imports"""
    try:
        from elevenlabs import ElevenLabs
        print("✅ ElevenLabs v1.0+ imports successful")
        return True
    except ImportError as e:
        print(f"❌ ElevenLabs import failed: {e}")
        return False

def test_ai_utils_import():
    """Test AI utilities import"""
    try:
        from ai_utils import create_ai_clients, OpenAITextGenerator, ElevenLabsAudioGenerator, test_ai_connections
        print("✅ AI utilities imports successful")
        return True
    except ImportError as e:
        print(f"❌ AI utilities import failed: {e}")
        return False

def test_other_imports():
    """Test other required imports"""
    try:
        import requests
        import json
        import os
        import argparse
        print("✅ Standard library imports successful")
        return True
    except ImportError as e:
        print(f"❌ Standard library import failed: {e}")
        return False

def main():
    """Run all import tests"""
    print("🧪 Testing package imports for updated APIs...\n")
    
    tests = [
        test_moviepy_import,
        test_openai_import,
        test_elevenlabs_import,
        test_ai_utils_import,
        test_other_imports
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print(f"\n📊 Results: {sum(results)}/{len(results)} tests passed")
    
    if all(results):
        print("🎉 All imports successful! Ready to use the updated movie recap tool.")
        return True
    else:
        print("⚠️  Some imports failed. Please install missing packages:")
        print("   pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    main()