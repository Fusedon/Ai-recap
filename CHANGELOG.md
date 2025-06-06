# Changelog

## [2.0.0] - 2024-06-06

### 🚀 Major Package Updates

#### MoviePy v2.0+ Migration
- **BREAKING**: Updated from MoviePy v1.x to v2.0+
- Changed imports from `moviepy.editor` to `moviepy`
- Updated method calls:
  - `.subclip()` → `.subclipped()`
  - `.set_audio()` → `.with_audio()`
  - `.set_duration()` → `.with_duration()`
  - `.volumex()` → `.with_volume_scaled()`
  - `.fl_time()` → `.with_effects([SpeedEffect()])`
- Simplified import structure for better performance

#### OpenAI Python SDK v1.0+ Migration
- **BREAKING**: Updated from OpenAI v0.28 to v1.0+
- Changed from `openai.ChatCompletion.create()` to client-based API
- Updated API calls:
  - `openai.api_key = key` → `OpenAI(api_key=key)`
  - `response['choices'][0]['message']['content']` → `response.choices[0].message.content`
- Improved error handling and type safety

#### ElevenLabs Python SDK v1.0+ Migration
- **BREAKING**: Updated from ElevenLabs v0.2 to v1.0+
- Changed from `elevenlabs.set_api_key()` to client-based API
- Updated API calls:
  - `elevenlabs.generate()` → `client.generate()`
  - `elevenlabs.save()` → manual file writing with chunks
- Better streaming support for audio generation

### 🔧 Technical Improvements
- **NEW**: Created `ai_utils.py` with modular AI service utilities
- **NEW**: `OpenAITextGenerator` class with retry logic and specialized methods
- **NEW**: `ElevenLabsAudioGenerator` class with robust error handling
- Enhanced error handling for API failures with exponential backoff
- Improved audio file handling with proper chunk writing
- Better fallback mechanisms for failed narration generation
- Updated silent audio generation for MoviePy v2.0
- Separation of concerns: AI logic separated from video processing

### 📚 Documentation Updates
- Updated README with package migration notes
- Added installation notes for new package versions
- Created comprehensive changelog
- Updated example usage for new APIs
- Added AI Services Architecture section to README
- Documented new AI utility classes and functions

### 📁 New Files
- `ai_utils.py`: Modular AI service utilities
- `test_imports.py`: Package import validation
- `CHANGELOG.md`: Version history and changes

### 🛠️ Development
- All files now use latest package APIs
- Improved code compatibility with Python 3.9+
- Better type hints and error messages
- Streamlined dependency management

### ⚠️ Breaking Changes
If upgrading from v1.x, you must:
1. Update your Python environment: `pip install -r requirements.txt`
2. No code changes needed in your config files
3. The CLI interface remains the same

### 🔄 Migration Guide
For developers extending this code:
- Replace `moviepy.editor` imports with `moviepy`
- Use `.with_*()` methods instead of `.set_*()`
- Initialize OpenAI and ElevenLabs clients instead of setting global API keys
- Handle audio generation as streaming chunks

---

## [1.0.0] - 2024-06-06

### 🎉 Initial CLI Release
- Streamlined command-line interface
- Core AI movie recap functionality
- Configuration-based setup
- Background music integration
- Audio-video synchronization