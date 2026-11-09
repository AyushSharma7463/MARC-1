# MARC-1 (Jarvis Voice Assistant)

MARC-1 is an event-driven, real-time voice assistant powered by **Faster-Whisper** (Speech-to-Text), an **Energy-based Voice Activity Detector (VAD)**, a **Brain Orchestrator** supporting specialized skills (Calculator, Web Browser, Filesystem, Terminal, Vision) and **Ollama LLM**, and **Piper TTS** (Offline Text-to-Speech) with interruptible playback.

---

## Quick Start

### 1. Requirements & Virtual Environment
Ensure your Python environment has the dependencies installed:
```bash
pip install -r requirements.txt
```
*(Dependencies: `sounddevice`, `soundfile`, `numpy`, `scipy`, `faster-whisper`, `piper-tts`, `webrtcvad`, `requests`, `python-dotenv`, `pytest`)*

Make sure Ollama is running if you want conversational LLM responses:
```bash
ollama serve
ollama run llama3.2
```

### 2. Run MARC
You can run MARC directly from the project root or from inside `jarvis`:

**From Project Root:**
```bash
python run.py
# or
python main.py
```

**From `jarvis/` directory:**
```bash
cd jarvis
python -m backend.main
# or
python backend/run_voice.py
```

### 3. Run Automated Tests
```bash
jarvis/.venv/bin/pytest jarvis
```
All 11 tests across audio, VAD, wakeword, TTS, calculator, brain, and skills will execute and pass.

---

## Architecture

```
[ Microphone ]
      │
      ▼
 [ VAD ] ──────────────► [ AudioBuffer ]
                                │
                                ▼
                         [ Faster-Whisper ]
                                │ (text.transcribed)
       ┌────────────────────────┴────────────────────────┐
       ▼                                                 ▼
[ InterruptManager ]                              [ Brain Orchestrator ]
  (interrupts TTS)                                  ├── Planner
                                                    ├── Skills (Calculator, Browser, Filesystem, Terminal, Vision)
                                                    └── LLM (Ollama / Llama 3.2)
                                                                 │ (response.generated)
                                                                 ▼
                                                        [ PlaybackManager / Piper TTS ]
```

---

## Supported Capabilities
- **Voice Recognition:** Streaming microphone input via sounddevice with automatic speech segmentation.
- **Interruptible Speech:** Say *"stop"*, *"cancel"*, *"pause"*, or *"be quiet"* while MARC is speaking to immediately halt playback.
- **Math & Calculator:** Natural language math queries like *"what is 25 * 4?"*, *"100 divided by 5"*, or *"10 plus 20"*.
- **System & Terminal:** Safe command execution (`whoami`, `date`, `uptime`, etc.).
- **Filesystem Queries:** Check directory contents, current working directory, and file presence.
- **Web Search & Knowledge:** DuckDuckGo instant answers with LLM synthesis fallback.
- **Conversational Memory:** Full dialog context with automatic history summarization.
# MARC-1
