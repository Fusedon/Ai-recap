#!/usr/bin/env python3
"""
Streamlined Movie Recap Generator - Command Line Interface
Creates AI-narrated movie recaps from video files using OpenAI and ElevenLabs
"""

import os
import json
import argparse
import random
import re
import ast
import time
from moviepy import VideoFileClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip, concatenate_audioclips
from ai_utils import create_ai_clients, OpenAITextGenerator, ElevenLabsAudioGenerator

# Configuration constants
MIN_NUM_CLIPS = 20
MAX_NUM_CLIPS = 30
MIN_TOTAL_DURATION = 2.5 * 60  # 2.5 minutes
MAX_TOTAL_DURATION = 4.5 * 60  # 4.5 minutes

class MovieRecapGenerator:
    def __init__(self, config_path="config.json"):
        """Initialize with configuration from JSON file"""
        self.config = self.load_config(config_path)
        self.openai_key = self.config.get('openai_api_key')
        self.elevenlabs_key = self.config.get('elevenlabs_api_key')
        self.movie_path = self.config.get('movie_path')
        self.script_path = self.config.get('script_path', None)
        self.srt_path = self.config.get('srt_path', None)
        self.background_music_dir = self.config.get('background_music_dir', None)
        self.output_path = self.config.get('output_path', 'output_recap.mp4')
        self.temp_dir = self.config.get('temp_dir', 'temp_clips')
        
        # Validate required fields
        if not self.openai_key or not self.elevenlabs_key or not self.movie_path:
            raise ValueError("Missing required configuration: openai_api_key, elevenlabs_api_key, and movie_path are required")
        
        # Initialize AI clients
        self.text_generator, self.audio_generator = create_ai_clients(
            self.openai_key, 
            self.elevenlabs_key
        )
        
        # Create temp directory
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(os.path.join(self.temp_dir, "audio"), exist_ok=True)

    def load_config(self, file_path):
        """Load configuration from JSON file"""
        with open(file_path, 'r') as file:
            config = json.load(file)
        return config

    def read_script_file(self, file_path):
        """Read and return script content from file"""
        if not file_path or not os.path.exists(file_path):
            return None
        
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def read_srt_file(self, file_path):
        """Read and parse SRT file, return timestamped dialogue"""
        if not file_path or not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin1') as file:
                content = file.read()
        
        # Parse SRT format
        srt_data = []
        blocks = re.split(r'\n\s*\d+\s*\n', content)
        
        for block in blocks:
            if '-->' in block:
                lines = block.strip().split('\n')
                if len(lines) >= 2:
                    timestamp = lines[0].strip()
                    dialogue = ' '.join(lines[1:]).strip()
                    
                    # Convert timestamp to seconds
                    if ' --> ' in timestamp:
                        start_time, end_time = timestamp.split(' --> ')
                        start_seconds = self.convert_timestamp_to_seconds(start_time)
                        end_seconds = self.convert_timestamp_to_seconds(end_time)
                        srt_data.append({
                            'start': start_seconds,
                            'end': end_seconds,
                            'text': dialogue
                        })
        
        return srt_data

    def convert_timestamp_to_seconds(self, timestamp):
        """Convert SRT timestamp to seconds"""
        # Handle format: 00:01:23,456
        time_part = timestamp.replace(',', '.')
        parts = time_part.split(':')
        if len(parts) == 3:
            hours, minutes, seconds = parts
            return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
        return 0

    def combine_script_and_srt(self, script_content, srt_data):
        """Combine script content with SRT timestamps"""
        if not script_content and not srt_data:
            raise ValueError("Either script_path or srt_path must be provided")
        
        if not srt_data:
            # If no SRT, just return script content
            return script_content
        
        if not script_content:
            # If no script, create content from SRT
            combined = ""
            for entry in srt_data:
                combined += f"{entry['start']}\n{entry['text']}\n{entry['end']}\n"
            return combined
        
        # If both exist, create a more sophisticated combination
        # For simplicity, we'll use the SRT data with timestamps
        combined = "0\n"  # Start marker
        for entry in srt_data:
            combined += f"{entry['start']}\n{entry['text']}\n{entry['end']}\n"
        
        return combined

    def get_ai_scene_selection(self, combined_script, movie_title, num_clips):
        """Use GPT-4 to select key scenes from the movie"""
        prompt = f'''Read and understand this script of the movie "{movie_title}", which includes timestamps (indicating number of seconds into the movie): "{combined_script}"

From this, choose {num_clips} time ranges that are most essential to the plot and development of the movie's story. Each chosen range should be between 10 seconds and 30 seconds. Choose ranges from the script provided.

Only output the time ranges, formatted in a Python dictionary in the format of: {{"120-145": "PLOT SUMMARY OF WHAT OCCURS DURING THAT TIME RANGE", "280-300": "..."}}

Don't overlap time ranges.

Each value in this dictionary should be a commentary describing what is happening in the scene. This should be a description of each event within the time duration. Use full sentences like you're a commentator speaking to an audience going scene-by-scene for each dict value.

For the first dict value start it with: "Here we go, let's go over the movie {movie_title}." Write at least 3 sentences for each value.

Make sure the whole movie's plot arc is covered, up until the final scene. Output the time ranges in numerical order. Ignore the very first time range, which starts at 0.'''

        try:
            # Use the AI utility function for text generation
            answer = self.text_generator.generate_text(
                prompt=prompt,
                system_message="You are a movie expert and commentator."
            )
            
            # Clean up the response
            answer = answer.replace("```", "").replace("python", "").replace("    ", "")
            answer = re.sub(r'\n\n+', '', answer)
            
            # Parse as Python dictionary
            scene_dict = ast.literal_eval(answer)
            
            if not isinstance(scene_dict, dict):
                raise ValueError("AI response is not a valid dictionary")
            
            return scene_dict
            
        except Exception as e:
            print(f"Error getting AI scene selection: {e}")
            if "too large" in str(e).lower():
                raise ValueError("Script too large for AI processing")
            time.sleep(5)  # Rate limit handling
            raise

    def extract_video_clips_and_generate_narration(self, video_path, scene_dict):
        """Extract video clips and generate AI narration for each scene"""
        video = VideoFileClip(video_path)
        clips = []
        audio_clips = []
        
        print(f"Processing {len(scene_dict)} scenes...")
        
        for i, (time_range, narration_text) in enumerate(scene_dict.items()):
            print(f"Processing scene {i+1}/{len(scene_dict)}: {time_range}")
            
            # Parse time range
            start_str, end_str = time_range.split('-')
            start = int(start_str)
            end = int(end_str)
            
            # Ensure we don't exceed video duration
            if end > video.duration:
                end = int(video.duration)
            if start >= video.duration:
                continue
            
            # Extract video clip
            clip = video.subclipped(start, end)
            clips.append(clip)
            
            # Generate AI narration
            print(f"Generating narration: {narration_text[:50]}...")
            try:
                # Use the AI utility function for audio generation
                audio_file_path = self.audio_generator.generate_narration_audio(
                    narration_text=narration_text,
                    output_dir=os.path.join(self.temp_dir, "audio"),
                    clip_index=i+1,
                    voice="Liam"
                )
                
                # Load as audio clip
                audio_clip = AudioFileClip(audio_file_path)
                audio_clips.append(audio_clip)
                
            except Exception as e:
                print(f"Error generating narration for scene {i+1}: {e}")
                # Use silent audio as fallback
                from moviepy import AudioClip
                silent_audio = AudioClip(lambda t: 0, duration=clip.duration)
                audio_clips.append(silent_audio)
        
        video.close()
        return clips, audio_clips

    def synchronize_audio_video(self, clips, audio_clips):
        """Synchronize video clips with AI narration"""
        adjusted_clips = []
        
        print("Synchronizing audio and video...")
        
        for i, (clip, audio) in enumerate(zip(clips, audio_clips)):
            print(f"Adjusting clip {i+1}/{len(clips)}")
            
            # Calculate speed adjustment factor
            if audio.duration > 0:
                slowdown_factor = audio.duration / clip.duration
                
                # If there's significant timing difference (>4 seconds), adjust video speed
                if abs(clip.duration - audio.duration) > 4:
                    from moviepy import SpeedEffect
                    clip = clip.with_effects([SpeedEffect(1/slowdown_factor)])
                    clip = clip.with_duration(audio.duration)
                
                # Replace original audio with AI narration
                clip = clip.with_audio(audio.with_volume_scaled(4.0))
            
            adjusted_clips.append(clip)
        
        return adjusted_clips

    def add_background_music(self, final_clip):
        """Add background music if available"""
        if not self.background_music_dir or not os.path.exists(self.background_music_dir):
            print("No background music directory specified or found")
            return final_clip
        
        music_files = [f for f in os.listdir(self.background_music_dir) 
                      if f.lower().endswith(('.mp3', '.wav', '.m4a'))]
        
        if not music_files:
            print("No music files found in background music directory")
            return final_clip
        
        print("Adding background music...")
        
        # Select random music file
        music_file = random.choice(music_files)
        music_path = os.path.join(self.background_music_dir, music_file)
        
        try:
            background_music = AudioFileClip(music_path)
            
            # Start from 40 seconds to avoid intros
            if background_music.duration > 40:
                background_music = background_music.subclipped(40)
            
            # Loop music to match video duration
            if background_music.duration < final_clip.duration:
                loops_needed = int(final_clip.duration / background_music.duration) + 1
                music_clips = [background_music] * loops_needed
                background_music = concatenate_audioclips(music_clips)
            
            # Trim to exact duration and lower volume
            background_music = background_music.subclipped(0, final_clip.duration).with_volume_scaled(0.1)
            
            # Combine with existing audio
            combined_audio = CompositeAudioClip([final_clip.audio, background_music])
            final_clip = final_clip.with_audio(combined_audio)
            
        except Exception as e:
            print(f"Error adding background music: {e}")
        
        return final_clip

    def generate_recap(self):
        """Main function to generate movie recap"""
        print(f"Starting movie recap generation for: {self.movie_path}")
        
        # Extract movie title from filename
        movie_title = os.path.splitext(os.path.basename(self.movie_path))[0]
        print(f"Movie title: {movie_title}")
        
        # Read script and SRT files
        print("Reading script and subtitle files...")
        script_content = self.read_script_file(self.script_path)
        srt_data = self.read_srt_file(self.srt_path)
        
        # Combine script and SRT data
        combined_script = self.combine_script_and_srt(script_content, srt_data)
        
        if not combined_script:
            raise ValueError("No script or subtitle content available")
        
        # Determine number of clips
        num_clips = random.randint(MIN_NUM_CLIPS, MAX_NUM_CLIPS)
        print(f"Generating {num_clips} clips...")
        
        # Get AI scene selection
        print("Getting AI scene selection...")
        scene_dict = self.get_ai_scene_selection(combined_script, movie_title, num_clips)
        
        print(f"Selected {len(scene_dict)} scenes:")
        for time_range, description in scene_dict.items():
            print(f"  {time_range}: {description[:100]}...")
        
        # Extract clips and generate narration
        clips, audio_clips = self.extract_video_clips_and_generate_narration(self.movie_path, scene_dict)
        
        if not clips:
            raise ValueError("No video clips were successfully extracted")
        
        # Synchronize audio and video
        adjusted_clips = self.synchronize_audio_video(clips, audio_clips)
        
        # Concatenate all clips
        print("Concatenating video clips...")
        final_clip = concatenate_videoclips(adjusted_clips)
        
        # Add background music
        final_clip = self.add_background_music(final_clip)
        
        # Export final video
        print(f"Exporting final video to: {self.output_path}")
        final_clip.write_videofile(self.output_path, codec='libx264', audio_codec='aac')
        
        # Cleanup
        final_clip.close()
        for clip in adjusted_clips:
            clip.close()
        
        print(f"Movie recap generated successfully: {self.output_path}")
        print(f"Duration: {final_clip.duration:.1f} seconds")

    def cleanup(self):
        """Clean up temporary files"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            print("Temporary files cleaned up")


def main():
    parser = argparse.ArgumentParser(description='Generate AI movie recaps from video files')
    parser.add_argument('--config', default='config.json', help='Path to configuration file')
    parser.add_argument('--cleanup', action='store_true', help='Clean up temporary files after processing')
    
    args = parser.parse_args()
    
    try:
        generator = MovieRecapGenerator(args.config)
        generator.generate_recap()
        
        if args.cleanup:
            generator.cleanup()
            
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())