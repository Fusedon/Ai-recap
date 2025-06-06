#!/usr/bin/env python3
"""
Configuration Test Script
Validates your config.json file and API connections
"""

import json
import os
import sys

def test_config(config_path="config.json"):
    """Test configuration file and API connections"""
    
    print("Testing Movie Recap Generator Configuration...")
    print("=" * 50)
    
    # Test 1: Config file exists
    if not os.path.exists(config_path):
        print(f"❌ Config file not found: {config_path}")
        print(f"   Create one by copying config_template.json")
        return False
    
    print(f"✅ Config file found: {config_path}")
    
    # Test 2: Load and parse config
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        print("✅ Config file is valid JSON")
    except json.JSONDecodeError as e:
        print(f"❌ Config file has invalid JSON: {e}")
        return False
    
    # Test 3: Required fields
    required_fields = ['openai_api_key', 'elevenlabs_api_key', 'movie_path']
    missing_fields = []
    
    for field in required_fields:
        if field not in config or not config[field] or config[field] in ['YOUR_OPENAI_API_KEY_HERE', 'YOUR_ELEVENLABS_API_KEY_HERE']:
            missing_fields.append(field)
    
    if missing_fields:
        print(f"❌ Missing or invalid required fields: {', '.join(missing_fields)}")
        return False
    
    print("✅ All required fields present")
    
    # Test 4: Movie file exists
    movie_path = config['movie_path']
    if not os.path.exists(movie_path):
        print(f"❌ Movie file not found: {movie_path}")
        return False
    
    print(f"✅ Movie file found: {movie_path}")
    
    # Test 5: Script or SRT file exists
    script_path = config.get('script_path')
    srt_path = config.get('srt_path')
    
    has_script = script_path and os.path.exists(script_path)
    has_srt = srt_path and os.path.exists(srt_path)
    
    if not has_script and not has_srt:
        print("❌ Neither script file nor SRT file found")
        print("   You need at least one of these for the tool to work")
        return False
    
    if has_script:
        print(f"✅ Script file found: {script_path}")
    if has_srt:
        print(f"✅ SRT file found: {srt_path}")
    
    # Test 6: Background music directory (optional)
    music_dir = config.get('background_music_dir')
    if music_dir:
        if os.path.exists(music_dir):
            music_files = [f for f in os.listdir(music_dir) 
                          if f.lower().endswith(('.mp3', '.wav', '.m4a'))]
            if music_files:
                print(f"✅ Background music directory found with {len(music_files)} files")
            else:
                print(f"⚠️  Background music directory exists but no audio files found")
        else:
            print(f"⚠️  Background music directory not found: {music_dir}")
    else:
        print("ℹ️  No background music directory specified (optional)")
    
    # Test 7: API Key format validation
    openai_key = config['openai_api_key']
    if not openai_key.startswith('sk-'):
        print("⚠️  OpenAI API key doesn't start with 'sk-' - this might be incorrect")
    else:
        print("✅ OpenAI API key format looks correct")
    
    elevenlabs_key = config['elevenlabs_api_key']
    if len(elevenlabs_key) < 20:
        print("⚠️  ElevenLabs API key seems too short - this might be incorrect")
    else:
        print("✅ ElevenLabs API key format looks correct")
    
    # Test 8: Output directory writable
    output_path = config.get('output_path', 'output_recap.mp4')
    output_dir = os.path.dirname(output_path) or '.'
    
    if os.access(output_dir, os.W_OK):
        print(f"✅ Output directory is writable: {output_dir}")
    else:
        print(f"❌ Output directory is not writable: {output_dir}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Configuration test passed!")
    print("You can now run: python movie_recap.py")
    
    return True

def test_api_connections(config_path="config.json"):
    """Test actual API connections (optional, requires API calls)"""
    
    print("\nTesting API Connections (this will make actual API calls)...")
    print("=" * 50)
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except:
        print("❌ Cannot load config file")
        return False
    
    # Test AI services using utility functions
    try:
        from ai_utils import test_ai_connections
        
        if not test_ai_connections(config['openai_api_key'], config['elevenlabs_api_key']):
            return False
            
    except ImportError:
        print("⚠️  AI utilities not available (check ai_utils.py)")
        return False
    except Exception as e:
        print(f"❌ AI service connection test failed: {e}")
        return False
    
    print("🎉 All API connections successful!")
    return True

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Test Movie Recap Generator configuration')
    parser.add_argument('--config', default='config.json', help='Path to configuration file')
    parser.add_argument('--test-apis', action='store_true', help='Test actual API connections (makes API calls)')
    
    args = parser.parse_args()
    
    # Test configuration
    if not test_config(args.config):
        print("\n❌ Configuration test failed. Please fix the issues above.")
        return 1
    
    # Test APIs if requested
    if args.test_apis:
        if not test_api_connections(args.config):
            print("\n❌ API connection test failed.")
            return 1
    
    return 0

if __name__ == "__main__":
    exit(main())