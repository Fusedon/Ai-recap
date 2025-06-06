#!/usr/bin/env python3
"""
Example usage of the Movie Recap Generator CLI
This script demonstrates how to use the tool programmatically
"""

import json
import os
from movie_recap import MovieRecapGenerator

def create_example_config():
    """Create an example configuration"""
    config = {
        "openai_api_key": "sk-your-openai-api-key-here",
        "elevenlabs_api_key": "your-elevenlabs-api-key-here",
        "movie_path": "example_movie.mp4",
        "script_path": "example_script.txt",
        "srt_path": "example_subtitles.srt",
        "background_music_dir": "background_music",
        "output_path": "example_recap.mp4",
        "temp_dir": "temp_example"
    }
    
    with open("example_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("Created example_config.json - modify with your actual values")

def create_sample_srt():
    """Create a sample SRT file for testing"""
    sample_srt = """1
00:00:10,500 --> 00:00:13,000
Welcome to our movie.

2
00:00:15,000 --> 00:00:18,000
This is the opening scene.

3
00:01:00,000 --> 00:01:05,000
The protagonist enters the story.

4
00:02:30,000 --> 00:02:35,000
A crucial plot point is revealed.

5
00:04:00,000 --> 00:04:08,000
The climax of our story unfolds dramatically.

6
00:05:00,000 --> 00:05:03,000
And here's how it all ends.
"""
    
    with open("example_subtitles.srt", "w") as f:
        f.write(sample_srt)
    
    print("Created example_subtitles.srt")

def create_sample_script():
    """Create a sample script file for testing"""
    sample_script = """MOVIE SCRIPT EXAMPLE

FADE IN:

EXT. CITY STREET - DAY

The bustling city comes alive as our protagonist JOHN walks down the street.

JOHN
(to himself)
Another day, another adventure.

He stops at a coffee shop, unaware that his life is about to change forever.

INT. COFFEE SHOP - CONTINUOUS

John orders his usual coffee. The BARISTA, SARAH, smiles at him.

SARAH
The usual, John?

JOHN
You know me too well.

Suddenly, a MYSTERIOUS STRANGER approaches John.

STRANGER
John Smith? I have something that belongs to you.

The stranger hands John an envelope and disappears into the crowd.

JOHN
(confused)
Wait! Who are you?

John opens the envelope to find a key and a note: "The truth awaits at the old warehouse."

EXT. OLD WAREHOUSE - NIGHT

John arrives at the warehouse, key in hand. He unlocks the door and steps inside.

INT. WAREHOUSE - CONTINUOUS

Inside, John discovers a room full of monitors showing surveillance footage of his entire life.

JOHN
(shocked)
What is this place?

A VOICE echoes from the shadows.

VOICE (O.S.)
Welcome to the truth, John. Everything you thought you knew was a lie.

FADE TO BLACK.

THE END
"""
    
    with open("example_script.txt", "w") as f:
        f.write(sample_script)
    
    print("Created example_script.txt")

def run_example():
    """Run the movie recap generator with example files"""
    
    print("Movie Recap Generator - Example Usage")
    print("=" * 40)
    
    # Check if we have a valid config
    if not os.path.exists("config.json"):
        print("No config.json found. Creating example files...")
        create_example_config()
        create_sample_srt()
        create_sample_script()
        
        print("\nExample files created! To run the actual tool:")
        print("1. Edit config.json with your API keys and movie path")
        print("2. Run: python movie_recap.py")
        return
    
    try:
        # Initialize the generator
        generator = MovieRecapGenerator("config.json")
        
        print("Configuration loaded successfully!")
        print(f"Movie: {generator.movie_path}")
        print(f"Output: {generator.output_path}")
        
        # Run the generation process
        generator.generate_recap()
        
        print("\n✅ Movie recap generated successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting tips:")
        print("- Make sure your API keys are valid")
        print("- Check that your movie file exists")
        print("- Ensure you have either a script or SRT file")
        print("- Run: python test_config.py to validate your setup")

def batch_process_example():
    """Example of processing multiple movies"""
    
    movies = [
        {
            "movie_path": "movie1.mp4",
            "srt_path": "movie1.srt",
            "output_path": "recap1.mp4"
        },
        {
            "movie_path": "movie2.mp4", 
            "script_path": "movie2_script.txt",
            "output_path": "recap2.mp4"
        }
    ]
    
    base_config = {
        "openai_api_key": "your-key-here",
        "elevenlabs_api_key": "your-key-here",
        "background_music_dir": "music",
        "temp_dir": "temp_batch"
    }
    
    for i, movie_config in enumerate(movies):
        print(f"\nProcessing movie {i+1}/{len(movies)}: {movie_config['movie_path']}")
        
        # Create config for this movie
        config = {**base_config, **movie_config}
        config_file = f"temp_config_{i}.json"
        
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)
        
        try:
            generator = MovieRecapGenerator(config_file)
            generator.generate_recap()
            print(f"✅ Completed: {movie_config['output_path']}")
            
        except Exception as e:
            print(f"❌ Failed: {e}")
        
        finally:
            # Cleanup temp config
            if os.path.exists(config_file):
                os.remove(config_file)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Movie Recap Generator Examples')
    parser.add_argument('--create-examples', action='store_true', 
                       help='Create example configuration and sample files')
    parser.add_argument('--batch', action='store_true',
                       help='Show batch processing example')
    
    args = parser.parse_args()
    
    if args.create_examples:
        create_example_config()
        create_sample_srt()
        create_sample_script()
        print("\nExample files created! Edit config.json with your actual values.")
    elif args.batch:
        print("Batch Processing Example:")
        print("This would process multiple movies in sequence")
        batch_process_example()
    else:
        run_example()