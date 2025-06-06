#!/usr/bin/env python3
"""
AI Utilities for Movie Recap Generator

This module contains utility functions for interacting with AI services:
- OpenAI GPT-4 for text generation
- ElevenLabs for text-to-speech conversion
"""

import os
import time
from typing import Optional, List, Dict, Any
from openai import OpenAI
from elevenlabs import ElevenLabs


class OpenAITextGenerator:
    """Handles OpenAI GPT-4 text generation"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        """
        Initialize OpenAI client
        
        Args:
            api_key: OpenAI API key
            model: Model to use (default: gpt-4o)
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def generate_text(self, 
                     prompt: str, 
                     system_message: str = "You are a helpful assistant.",
                     max_tokens: Optional[int] = None,
                     temperature: float = 0.7,
                     max_retries: int = 3) -> str:
        """
        Generate text using OpenAI GPT-4
        
        Args:
            prompt: User prompt for text generation
            system_message: System message to set context
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0-2)
            max_retries: Maximum number of retry attempts
            
        Returns:
            Generated text string
            
        Raises:
            Exception: If all retry attempts fail
        """
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                
                return response.choices[0].message.content.strip()
                
            except Exception as e:
                print(f"OpenAI API attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise Exception(f"OpenAI API failed after {max_retries} attempts: {e}")
                time.sleep(2 ** attempt)  # Exponential backoff
    
    def generate_movie_scenes(self, 
                            movie_content: str, 
                            num_clips: int = 25,
                            max_duration: int = 270) -> str:
        """
        Generate movie scene selections using GPT-4
        
        Args:
            movie_content: Movie script or subtitle content
            num_clips: Number of clips to generate
            max_duration: Maximum total duration in seconds
            
        Returns:
            Generated scene selection text
        """
        system_message = "You are a movie expert and commentator."
        
        prompt = f'''Based on this movie content, select {num_clips} key scenes that best represent the movie's plot progression. 

Movie content:
{movie_content}

For each scene, provide:
1. Time range (start-end in seconds)
2. Brief narration text (1-2 sentences) explaining what happens

Format your response as a Python list of tuples: [(start, end, "narration"), ...]

Requirements:
- Total duration should not exceed {max_duration} seconds
- Cover the main plot points chronologically
- Each clip should be 8-15 seconds long
- Include key dramatic moments and plot developments
- Narration should be engaging and informative

Make sure the whole movie's plot arc is covered, up until the final scene. Output the time ranges in numerical order. Ignore the very first time range, which starts at 0.'''

        return self.generate_text(
            prompt=prompt,
            system_message=system_message,
            temperature=0.3  # Lower temperature for more consistent formatting
        )


class ElevenLabsAudioGenerator:
    """Handles ElevenLabs text-to-speech generation"""
    
    def __init__(self, api_key: str):
        """
        Initialize ElevenLabs client
        
        Args:
            api_key: ElevenLabs API key
        """
        self.client = ElevenLabs(api_key=api_key)
    
    def generate_audio(self, 
                      text: str,
                      voice: str = "Liam",
                      model: str = "eleven_multilingual_v2",
                      output_path: Optional[str] = None,
                      max_retries: int = 3) -> Optional[str]:
        """
        Generate audio from text using ElevenLabs
        
        Args:
            text: Text to convert to speech
            voice: Voice to use (default: Liam)
            model: Model to use (default: eleven_multilingual_v2)
            output_path: Path to save audio file (optional)
            max_retries: Maximum number of retry attempts
            
        Returns:
            Path to saved audio file if output_path provided, None otherwise
            
        Raises:
            Exception: If all retry attempts fail
        """
        for attempt in range(max_retries):
            try:
                # Generate audio
                audio_generator = self.client.generate(
                    text=text,
                    voice=voice,
                    model=model
                )
                
                # Save to file if path provided
                if output_path:
                    with open(output_path, "wb") as f:
                        for chunk in audio_generator:
                            f.write(chunk)
                    return output_path
                
                return audio_generator
                
            except Exception as e:
                print(f"ElevenLabs API attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise Exception(f"ElevenLabs API failed after {max_retries} attempts: {e}")
                time.sleep(2 ** attempt)  # Exponential backoff
    
    def generate_narration_audio(self, 
                                narration_text: str,
                                output_dir: str,
                                clip_index: int,
                                voice: str = "Liam") -> str:
        """
        Generate narration audio for a specific clip
        
        Args:
            narration_text: Text to narrate
            output_dir: Directory to save audio file
            clip_index: Index of the clip (for filename)
            voice: Voice to use
            
        Returns:
            Path to saved audio file
        """
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename
        audio_filename = f"narration_{clip_index}.mp3"
        audio_path = os.path.join(output_dir, audio_filename)
        
        # Generate and save audio
        self.generate_audio(
            text=narration_text,
            voice=voice,
            output_path=audio_path
        )
        
        return audio_path


def create_ai_clients(openai_key: str, elevenlabs_key: str) -> tuple[OpenAITextGenerator, ElevenLabsAudioGenerator]:
    """
    Create and return AI client instances
    
    Args:
        openai_key: OpenAI API key
        elevenlabs_key: ElevenLabs API key
        
    Returns:
        Tuple of (OpenAITextGenerator, ElevenLabsAudioGenerator)
    """
    text_generator = OpenAITextGenerator(openai_key)
    audio_generator = ElevenLabsAudioGenerator(elevenlabs_key)
    
    return text_generator, audio_generator


def test_ai_connections(openai_key: str, elevenlabs_key: str) -> bool:
    """
    Test connections to both AI services
    
    Args:
        openai_key: OpenAI API key
        elevenlabs_key: ElevenLabs API key
        
    Returns:
        True if both services are accessible, False otherwise
    """
    try:
        # Test OpenAI
        text_gen = OpenAITextGenerator(openai_key)
        test_response = text_gen.generate_text(
            prompt="Say 'API test successful'",
            max_tokens=10
        )
        print("✅ OpenAI API connection successful")
        
        # Test ElevenLabs
        audio_gen = ElevenLabsAudioGenerator(elevenlabs_key)
        test_audio = audio_gen.generate_audio(
            text="Test",
            voice="Liam"
        )
        print("✅ ElevenLabs API connection successful")
        
        return True
        
    except Exception as e:
        print(f"❌ AI service connection failed: {e}")
        return False


if __name__ == "__main__":
    print("AI Utils module - Use this module to interact with OpenAI and ElevenLabs services")