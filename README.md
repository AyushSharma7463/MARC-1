# MARC-1 — Local AI Voice Assistant

**MARC-1** is an event-driven, voice-controlled AI assistant designed to process spoken commands, understand user intent, execute specialized tasks, and respond through synthesized speech.

It combines **Faster-Whisper** for speech recognition, **Ollama** for locally hosted language-model inference, and **Piper TTS** for offline speech synthesis.

The project focuses on building a modular voice-assistant architecture with audio processing, conversational reasoning, task execution, and interruptible voice responses.

---

## Overview

MARC-1 follows a voice-first interaction pipeline:

1. **Listen:** Capture microphone input.
2. **Detect:** Identify speech using Voice Activity Detection (VAD).
3. **Transcribe:** Convert speech into text using Faster-Whisper.
4. **Understand:** Process the request through the Brain Orchestrator and language model.
5. **Execute:** Route the request to an appropriate skill.
6. **Respond:** Generate a response and convert it into speech using Piper TTS.

The system uses an event-driven architecture to coordinate its runtime components.

## Key Features

- **Voice Input:** Microphone-based audio capture and speech processing.
- **Speech Recognition:** Faster-Whisper transcription.
- **Voice Activity Detection:** Energy-based and VAD-based audio processing components.
- **Local AI Reasoning:** Integration with Ollama and Llama 3.2.
- **Skill-Based Execution:** Modular skills for different assistant tasks.
- **Offline Text-to-Speech:** Piper-powered speech generation.
- **Interruptible Playback:** Stop or interrupt ongoing speech output.
- **Conversation Context:** Conversation state and history management.
- **Modular Architecture:** Independent components for audio, reasoning, runtime and task execution.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Speech-to-Text | Faster-Whisper |
| Language Model Runtime | Ollama |
| AI Model | Llama 3.2 |
| Text-to-Speech | Piper TTS |
| Audio Processing | SoundDevice, SoundFile, NumPy, SciPy |
| Voice Activity Detection | VAD |
| Backend Framework | FastAPI |
| Runtime Architecture | Event-driven Python components |
| Testing | Pytest |
| Configuration | Python Dotenv |

## System Architecture

```text
                 USER
                   |
                   v
             MICROPHONE
                   |
                   v
          AUDIO CAPTURE SYSTEM
                   |
                   v
          VOICE ACTIVITY DETECTION
                   |
                   v
             AUDIO BUFFER
                   |
                   v
           FASTER-WHISPER
            (Speech-to-Text)
                   |
                   v
          BRAIN ORCHESTRATOR
                   |
          +--------+--------+
          |                 |
          v                 v
       PLANNER          OLLAMA LLM
          |              LLAMA 3.2
          |                 |
          +--------+--------+
                   |
                   v
             SKILL EXECUTOR
                   |
       +-----------+-----------+
       |           |           |
       v           v           v
   CALCULATOR    BROWSER    FILESYSTEM
       |           |           |
       +-----------+-----------+
                   |
                   v
             RESPONSE OUTPUT
                   |
                   v
                PIPER
             (Text-to-Speech)
                   |
                   v
             AUDIO PLAYBACK
                   |
                   v
                 USER
```

## Core Modules

### 1. Audio Processing

Responsible for capturing and managing microphone input.

Includes:
- Microphone streaming.
- Audio buffering.
- Audio frame management.
- Voice Activity Detection.
- Audio state management.

### 2. Speech Recognition

Uses Faster-Whisper to convert recorded audio into text.

The current transcription implementation uses:
- Whisper Base model.
- Automatic device selection.
- INT8 computation.
- English-language transcription.

### 3. Brain Orchestrator

The central reasoning and coordination layer.

Responsibilities:
- Process incoming requests.
- Coordinate planning and execution.
- Manage assistant state.
- Route requests to registered skills.
- Coordinate language-model responses.

### 4. Language Model Integration

Uses Ollama to communicate with a locally hosted language model.

Default configuration:
- Runtime: Ollama
- Model: `llama3.2`
- Default endpoint: `http://localhost:11434`

### 5. Skill Execution

MARC-1 includes modular skill implementations:

| Skill | Purpose |
|---|---|
| Calculator | Mathematical operations |
| Browser | Online information retrieval using DuckDuckGo Instant Answers |
| Filesystem | File and directory operations |
| Terminal | Terminal command execution with basic command restrictions |
| Vision | Vision-related skill integration |
| LLM | Language-model-based responses |

### 6. Speech Synthesis

Uses Piper TTS to generate spoken responses.

Features:
- Local speech synthesis.
- ONNX voice model support.
- Audio playback.
- Playback interruption.
- Temporary audio-file cleanup.

---

## Project Structure

```text
MARC-1/
│
├── jarvis/
│   ├── backend/
│   │   ├── audio/
│   │   │   └── Audio capture and processing
│   │   │
│   │   ├── brain/
│   │   │   └── Planning and orchestration
│   │   │
│   │   ├── components/
│   │   │   └── Assistant runtime components
│   │   │
│   │   ├── core/
│   │   │   └── Configuration and logging
│   │   │
│   │   ├── llm/
│   │   │   └── Ollama integration
│   │   │
│   │   ├── pipeline/
│   │   │   └── Assistant processing pipeline
│   │   │
│   │   ├── runtime/
│   │   │   └── Event-driven runtime
│   │   │
│   │   ├── skills/
│   │   │   └── Modular assistant skills
│   │   │
│   │   ├── state/
│   │   │   └── Conversation state
│   │   │
│   │   ├── stt/
│   │   │   └── Speech recognition
│   │   │
│   │   ├── tts/
│   │   │   └── Piper speech synthesis
│   │   │
│   │   └── models/
│   │       └── Piper voice model
│   │
│   ├── requirements.txt
│   │
│   └── main.py
│
├── requirements.txt
├── main.py
├── run.py
├── README.md
└── .gitignore
```

---

## Installation and Setup

### Prerequisites

Install the following:

- Python with pip.
- Ollama.
- Git.
- A working microphone and audio output device.

### 1. Clone the repository

```bash
git clone https://github.com/AyushSharma7463/MARC-1.git

cd MARC-1
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip

pip install -r requirements.txt
```

### 4. Configure Ollama

Install Ollama from:

https://ollama.com/

Download the default language model:

```bash
ollama pull llama3.2
```

Start the Ollama service if it is not already running:

```bash
ollama serve
```

### 5. Start MARC-1

From the project root:

```bash
python run.py
```

Alternatively:

```bash
python main.py
```

The application initializes its runtime components and starts the voice-assistant engine.

---

## Configuration

MARC-1 supports environment-based configuration through Python Dotenv.

Create a `.env` file if you want to override the default settings:

```env
OLLAMA_HOST=http://localhost:11434
MODEL=llama3.2
TIMEOUT=120
LOG_LEVEL=INFO
DEBUG=False
```

Piper voice model paths can also be configured:

```env
PIPER_MODEL=models/en_US-lessac-medium.onnx
PIPER_CONFIG=models/en_US-lessac-medium.onnx.json
```

Keep personal credentials and machine-specific configuration out of version control.

---

## Running Tests

The project includes tests for different modules, including audio processing, VAD, wakeword detection, TTS, settings, logging, and skill execution.

Run the test suite from the project root:

```bash
pytest jarvis/
```

---

## Design Principles

MARC-1 is developed around the following engineering principles:

- **Modularity:** Separate responsibilities into independent components.
- **Local Processing:** Use locally hosted AI and speech-processing components where supported.
- **Event-Driven Communication:** Coordinate runtime components through events.
- **Extensibility:** Allow new assistant skills to be registered and integrated.
- **Separation of Concerns:** Keep audio processing, reasoning, execution and speech synthesis independent.
- **Interruptibility:** Support interruption of ongoing speech playback.

## Current Limitations

- Speech recognition is currently configured for English.
- Ollama must be available locally for language-model responses.
- Microphone and speaker permissions are required.
- The browser skill uses DuckDuckGo Instant Answers rather than a full search-engine crawling system.
- Hardware performance affects transcription and language-model response times.
- Terminal execution has basic restrictions, not a complete security sandbox.

**Security note:** Do not expose the terminal skill to untrusted users. Its current implementation uses shell command execution and should not be treated as production-grade isolation.

---

## Future Improvements

Potential development directions include:

- Improved conversational context management.
- More robust wake-word detection.
- Expanded language support.
- Better task planning and execution.
- Improved audio streaming and latency.
- Stronger permission controls for system-level skills.
- More comprehensive automated testing.
- Cross-platform installation and configuration.

---

## Author

**Ayush Sharma**

Computer Science and Engineering

GitHub: https://github.com/AyushSharma7463

Project: [MARC-1](https://github.com/AyushSharma7463/MARC-1)

---

## License

No open-source license has currently been specified. All rights are reserved by the author unless a license is added to this repository.
