# Movie Recap Generator - Command Line Interface

A streamlined command-line tool that creates AI-narrated movie recaps from video files using OpenAI GPT-4 and ElevenLabs text-to-speech.

## Features

- **AI Scene Selection**: GPT-4 analyzes movie content to select the most plot-relevant scenes
- **AI Narration**: ElevenLabs generates natural-sounding voice commentary
- **Audio-Video Synchronization**: Automatically adjusts video speed to match narration timing
- **Background Music**: Optional background music integration
- **Command Line Interface**: Simple, scriptable operation
- **Modular AI Services**: Separate utilities for OpenAI and ElevenLabs with error handling and retry logic

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

**Note**: This tool uses the latest versions of the packages:
- MoviePy v2.0+ (with breaking changes from v1.x)
- OpenAI Python SDK v1.0+ (new client-based API)
- ElevenLabs Python SDK v1.0+ (updated API)

### Package Updates
If you're upgrading from older versions, note these key changes:
- **MoviePy**: Import from `moviepy` instead of `moviepy.editor`, use `.with_*()` methods instead of `.set_*()`
- **OpenAI**: Use `OpenAI()` client instead of `openai.ChatCompletion.create()`
- **ElevenLabs**: Use `ElevenLabs()` client instead of `elevenlabs.generate()` directly

2. Set up your configuration file (copy and modify `config_template.json`):
```bash
cp config_template.json config.json
```

## Configuration

Edit `config.json` with your settings:

```json
{
    "openai_api_key": "sk-your-openai-api-key",
    "elevenlabs_api_key": "your-elevenlabs-api-key",
    "movie_path": "/path/to/your/movie.mp4",
    "script_path": "/path/to/movie/script.txt",
    "srt_path": "/path/to/movie/subtitles.srt",
    "background_music_dir": "/path/to/background/music/folder",
    "output_path": "my_movie_recap.mp4",
    "temp_dir": "temp_clips"
}
```

### Required Fields:
- `openai_api_key`: Your OpenAI API key (requires GPT-4 access)
- `elevenlabs_api_key`: Your ElevenLabs API key
- `movie_path`: Path to the input movie file (.mp4)

### Optional Fields:
- `script_path`: Path to movie script file (.txt) - if available
- `srt_path`: Path to subtitle file (.srt) - if available
- `background_music_dir`: Directory containing background music files
- `output_path`: Output video file path (default: "output_recap.mp4")
- `temp_dir`: Temporary files directory (default: "temp_clips")

**Note**: You must provide either `script_path` or `srt_path` (or both) for the tool to work.

## Usage

### Basic Usage
```bash
python movie_recap.py
```

### With Custom Config File
```bash
python movie_recap.py --config my_config.json
```

### With Cleanup
```bash
python movie_recap.py --cleanup
```

## How It Works

1. **Content Analysis**: Reads movie script and/or subtitle files
2. **AI Scene Selection**: GPT-4 analyzes content and selects 20-30 key scenes
3. **Video Processing**: Extracts selected video clips from the original movie
4. **Narration Generation**: ElevenLabs creates AI voice commentary for each scene
5. **Synchronization**: Adjusts video speed to match narration timing
6. **Assembly**: Combines clips with narration and optional background music
7. **Export**: Outputs final recap video

## Input File Formats

### Script Files (.txt)
Plain text movie scripts. The tool works best with:
- Full movie scripts with dialogue
- Scene descriptions
- Character names and actions

### Subtitle Files (.srt)
Standard SRT subtitle format:
```
1
00:00:10,500 --> 00:00:13,000
This is the first subtitle.

2
00:00:15,000 --> 00:00:18,000
This is the second subtitle.
```

### Background Music
Supported audio formats: `.mp3`, `.wav`, `.m4a`
- Place multiple music files in a directory
- Tool will randomly select and loop music to match video duration
- Music volume is automatically lowered to 10% for background effect

## API Requirements

### OpenAI API
- Requires GPT-4 access (GPT-4o model)
- Tier 2 API account recommended for longer scripts
- Costs vary based on script length and number of clips

### ElevenLabs API
- Uses "Liam" voice with "eleven_multilingual_v2" model
- Costs based on character count of generated narration
- Supports multiple languages

## Output

The tool generates:
- A single MP4 video file with AI narration
- Duration: typically 2.5-4.5 minutes
- Format: H.264 video with AAC audio
- Resolution: matches input video resolution

## Troubleshooting

### Common Issues

1. **"Missing required configuration"**
   - Ensure `openai_api_key`, `elevenlabs_api_key`, and `movie_path` are set

2. **"No script or subtitle content available"**
   - Provide either `script_path` or `srt_path` in config

3. **"Script too large for AI processing"**
   - Try using subtitle files instead of full scripts
   - Split very long movies into parts

4. **API Rate Limits**
   - The tool includes automatic retry logic
   - Consider upgrading API tiers for faster processing

### Performance Tips

- Use SRT files for faster processing (smaller than full scripts)
- Ensure movie files are in MP4 format for best compatibility
- Use shorter movies (under 3 hours) for optimal results
- Background music files should be longer than 60 seconds

## Example Workflow

1. Prepare your files:
   ```
   /movies/
     ├── citizen_kane.mp4
     ├── citizen_kane.srt
   /music/
     ├── background1.mp3
     ├── background2.mp3
   ```

2. Configure:
   ```json
   {
     "openai_api_key": "sk-...",
     "elevenlabs_api_key": "...",
     "movie_path": "/movies/citizen_kane.mp4",
     "srt_path": "/movies/citizen_kane.srt",
     "background_music_dir": "/music",
     "output_path": "citizen_kane_recap.mp4"
   }
   ```

3. Run:
   ```bash
   python movie_recap.py --cleanup
   ```

4. Result: `citizen_kane_recap.mp4` with AI narration and background music


## AI Services Architecture

The tool uses a modular approach with separate AI utilities:

### `ai_utils.py` - AI Service Utilities

**OpenAITextGenerator Class:**
- Handles GPT-4 text generation with retry logic
- Specialized method for movie scene analysis
- Configurable temperature and token limits
- Exponential backoff for failed requests

**ElevenLabsAudioGenerator Class:**
- Manages text-to-speech conversion
- Automatic file saving with proper chunk handling
- Voice and model selection
- Error handling with retry mechanisms

**Utility Functions:**
- `create_ai_clients()`: Initialize both AI services
- `test_ai_connections()`: Validate API connectivity

### Benefits:
- **Separation of Concerns**: AI logic separated from video processing
- **Error Handling**: Robust retry mechanisms for API failures
- **Reusability**: AI functions can be used independently
- **Maintainability**: Easier to update AI service implementations


## License

This tool is for educational and personal use. Ensure you have proper rights to the movie content you're processing.