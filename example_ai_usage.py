#!/usr/bin/env python3
"""
Example usage of AI utilities independently

This demonstrates how to use the OpenAI and ElevenLabs utilities
separately from the main movie recap functionality.
"""

import os
import json
from ai_utils import create_ai_clients, OpenAITextGenerator, ElevenLabsAudioGenerator


def example_text_generation():
    """Example of using OpenAI text generation"""
    print("🤖 OpenAI Text Generation Example")
    print("=" * 40)
    
    # Load config
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    # Create text generator
    text_gen = OpenAITextGenerator(config['openai_api_key'])
    
    # Generate some text
    prompt = "Write a brief movie review for The Matrix in 2 sentences."
    response = text_gen.generate_text(
        prompt=prompt,
        system_message="You are a professional movie critic.",
        temperature=0.7
    )
    
    print(f"Prompt: {prompt}")
    print(f"Response: {response}")
    print()


def example_audio_generation():
    """Example of using ElevenLabs audio generation"""
    print("🎵 ElevenLabs Audio Generation Example")
    print("=" * 40)
    
    # Load config
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    # Create audio generator
    audio_gen = ElevenLabsAudioGenerator(config['elevenlabs_api_key'])
    
    # Generate audio
    text = "This is a test of the ElevenLabs text-to-speech system."
    output_path = "test_audio.mp3"
    
    try:
        result_path = audio_gen.generate_audio(
            text=text,
            voice="Liam",
            output_path=output_path
        )
        
        print(f"Text: {text}")
        print(f"Audio saved to: {result_path}")
        print(f"File size: {os.path.getsize(result_path)} bytes")
        
        # Clean up
        os.remove(result_path)
        print("Test file cleaned up.")
        
    except Exception as e:
        print(f"Error generating audio: {e}")
    
    print()


def example_combined_usage():
    """Example of using both services together"""
    print("🔄 Combined AI Services Example")
    print("=" * 40)
    
    # Load config
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    # Create both clients
    text_gen, audio_gen = create_ai_clients(
        config['openai_api_key'],
        config['elevenlabs_api_key']
    )
    
    # Generate a movie quote
    prompt = "Generate a famous movie quote about artificial intelligence."
    quote = text_gen.generate_text(
        prompt=prompt,
        system_message="You are a movie database expert.",
        temperature=0.8
    )
    
    print(f"Generated quote: {quote}")
    
    # Convert to audio
    try:
        audio_path = audio_gen.generate_audio(
            text=quote,
            voice="Liam",
            output_path="movie_quote.mp3"
        )
        
        print(f"Quote converted to audio: {audio_path}")
        print(f"Audio file size: {os.path.getsize(audio_path)} bytes")
        
        # Clean up
        os.remove(audio_path)
        print("Audio file cleaned up.")
        
    except Exception as e:
        print(f"Error generating audio: {e}")


def main():
    """Run all examples"""
    print("🧪 AI Utilities Examples")
    print("=" * 50)
    print()
    
    # Check if config exists
    if not os.path.exists('config.json'):
        print("❌ config.json not found!")
        print("Please create a config.json file with your API keys.")
        print("Use config_template.json as a reference.")
        return
    
    try:
        # Run examples
        example_text_generation()
        example_audio_generation()
        example_combined_usage()
        
        print("✅ All examples completed successfully!")
        
    except Exception as e:
        print(f"❌ Example failed: {e}")
        print("\nTroubleshooting:")
        print("- Check your API keys in config.json")
        print("- Ensure you have internet connectivity")
        print("- Run: python test_config.py to validate setup")


if __name__ == "__main__":
    main()