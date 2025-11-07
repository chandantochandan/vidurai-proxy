# Vidurai Proxy Server

**Universal AI Memory Management Proxy**

A transparent, provider-agnostic proxy server that routes AI API calls through Vidurai for intelligent memory compression and token reduction. Works with any AI provider (Anthropic Claude, OpenAI, Google Gemini) without code changes.

---

## Overview

Vidurai Proxy sits between your AI tools and AI provider APIs, automatically compressing conversation context to reduce tokens and costs while maintaining response quality.

```
┌─────────────────────────────────────────┐
│  Your AI Tool (Claude Code, Cursor)    │
│  Uses standard Anthropic API format     │
└──────────────┬──────────────────────────┘
               │ (Standard API request)
               ▼
      ┌────────────────────┐
      │  Vidurai Proxy     │
      │  localhost:8080    │
      │                    │
      │  Auto-detects:     │
      │  - Provider        │
      │  - Session         │
      └────────┬───────────┘
               │
      ┌────────┴────────┐
      │                 │
      ▼                 ▼
┌──────────┐      ┌──────────┐
│ Vidurai  │      │ Terminal │
│ Memory   │      │ UI       │
│ (after   │      │ (stats)  │
│ 10 msgs) │      └──────────┘
└────┬─────┘
     │
     ▼
┌─────────────────────────┐
│  Anthropic/OpenAI API   │
│  (using your key)       │
└─────────────────────────┘
```

---

## Key Features

- **Transparent Proxy**: No code changes needed, just point your AI tool to the proxy URL
- **Provider-Agnostic**: Works with Anthropic, OpenAI, Google, and more
- **Automatic Sessions**: Sessions auto-created from API key hashes
- **Smart Compression**: Only compresses after threshold (default: 10 messages)
- **Pass-Through Security**: Your API keys never stored on proxy
- **Real-Time Metrics**: Terminal UI shows token/cost savings live
- **Fully Configurable**: All settings in `config.yaml`
- **Production-Ready**: Deploy locally or to cloud platforms

---

## 🎯 Current Status

**Version:** 1.0.0 (Production Ready)
**Last Updated:** November 2024
**Repository:** https://github.com/chandantochandan/vidurai-proxy

### ✅ What Works
- ✅ Transparent proxy for Anthropic, OpenAI, Google
- ✅ Automatic provider detection
- ✅ Zero-config session management (API key hashing)
- ✅ Vidurai memory compression with RL agent
- ✅ Real-time metrics (token savings, cost tracking)
- ✅ Beautiful terminal UI with live progress
- ✅ Health and metrics endpoints
- ✅ Graceful startup/shutdown

### 📝 Known Limitations
- ⚠️ **Session persistence disabled** - Sessions work perfectly but reset on server restart (acceptable for MVP, most sessions are short-lived)
- ⚠️ **Token counting uses word approximation** - Accurate enough for MVP (plan to add tiktoken)
- ⚠️ **No streaming support yet** - Works with standard responses only

See [KNOWN_ISSUES.md](KNOWN_ISSUES.md) for details and roadmap.

---

## Quick Start

### 1. Install Dependencies

```bash
# Clone repository
git clone https://github.com/chandantochandan/vidurai-proxy.git
cd vidurai-proxy

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure

```bash
# Copy environment template
cp .env.example .env

# Add your OpenAI API key (for compression)
echo "OPENAI_API_KEY=sk-..." >> .env
```

### 3. Run

```bash
# Option A: Using run script (recommended)
./run.sh

# Option B: Direct
python3 src/main.py

# Server starts on http://localhost:8080
```

### 4. Use with Any AI Tool

Just change the base URL:

```bash
# For Claude Code
export ANTHROPIC_BASE_URL=http://localhost:8080

# For OpenAI clients
export OPENAI_BASE_URL=http://localhost:8080/v1

# Everything else stays the same - use your original API key
```

### 5. Monitor

Watch the terminal for real-time display of:
- ✅ Request processing
- 🧠 Vidurai compression
- 📊 Token savings
- 💰 Cost savings
- ⏱️  Response times

---

## Architecture Decisions

Based on requirements for transparency, security, and ease of use:

### 1. API Request Format
**Choice: Transparent Proxy**

The proxy mimics provider APIs exactly. Clients send standard requests:

```bash
# Client sends normal Anthropic API request
curl http://localhost:8080/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

No custom formats, no provider field needed. The proxy auto-detects provider from the request path and headers.

### 2. Session Management
**Choice: Auto-Generated from API Key Hash**

Sessions are automatically created and tracked using a hash of the client's API key:

```python
session_id = hashlib.sha256(api_key.encode()).hexdigest()[:16]
```

**Benefits:**
- Zero configuration for users
- Automatic session persistence
- One session per API key (logical grouping)
- No manual session ID management

### 3. Vidurai Memory Strategy
**Choice: Threshold-Based Compression**

- **< 10 messages**: Pass-through mode (no compression)
- **≥ 10 messages**: Vidurai compression activated

**Rationale:**
- Short conversations don't benefit from compression overhead
- Compression ROI increases with conversation length
- Threshold configurable in `config.yaml`

### 4. Provider API Keys
**Choice: Pass-Through (Zero Trust)**

The proxy **never stores** your AI provider API keys:

- Client's API key is forwarded directly to provider
- Proxy only needs its own `OPENAI_API_KEY` for compression
- Maximum security and privacy

### 5. Response Format
**Choice: Identical to Provider (Transparent)**

Responses match provider format exactly:

```json
{
  "id": "msg_123",
  "type": "message",
  "content": [{"type": "text", "text": "Hello!"}],
  "model": "claude-sonnet-4"
}
```

**Optional**: Savings metrics in response header:

```
X-Vidurai-Stats: tokens_saved=150,cost_saved=0.00045,compression_ratio=0.72
```

### 6. Deployment
**Choice: Single Server (FastAPI)**

Simple, stateful server:
- In-memory session management
- Easy to deploy locally or to cloud
- Can migrate to serverless later if needed

### 7. Technology Stack
**Choice: Python + FastAPI**

- **FastAPI**: Async, high-performance Python web framework
- **Vidurai**: Native Python integration (no subprocess overhead)
- **Rich/Loguru**: Beautiful terminal UI and logging
- **YAML**: Human-friendly configuration

---

## Configuration

All behavior controlled via `config/config.yaml`:

```yaml
server:
  host: "0.0.0.0"
  port: 8080

vidurai:
  enable_decay: false
  reward_profile: "QUALITY"
  compression_threshold: 10
  min_importance: 0.3

ai_providers:
  anthropic:
    base_url: "https://api.anthropic.com"
  openai:
    base_url: "https://api.openai.com/v1"

metrics:
  track_savings: true
  show_realtime: true
```

See `config/config.yaml` for all options.

---

## Usage Examples

### Example 1: Claude Code

```bash
# In your terminal
export ANTHROPIC_BASE_URL=http://localhost:8080

# Use Claude Code normally
claude "Help me refactor this code"

# Proxy handles compression automatically
```

### Example 2: Python OpenAI Client

```python
from openai import OpenAI

# Point to proxy
client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="your-openai-key"  # Your real key, forwarded to OpenAI
)

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Example 3: Anthropic Python Client

```python
import anthropic

# Point to proxy
client = anthropic.Anthropic(
    base_url="http://localhost:8080",
    api_key="your-anthropic-key"
)

message = client.messages.create(
    model="claude-sonnet-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

---

## Terminal UI

When running, the proxy shows real-time stats:

```
╭─────────────────────────────────────────────────────────╮
│            VIDURAI PROXY SERVER - RUNNING               │
╰─────────────────────────────────────────────────────────╯

🚀 Server: http://localhost:8080
🔧 Mode: Transparent Proxy
🧠 Vidurai: Active (threshold: 10 messages)

╭───────────────── ACTIVE SESSIONS ─────────────────╮
│ Session: abc123...  Provider: anthropic           │
│ Messages: 15        Compressed: 5                 │
│ Tokens Saved: 450   Cost Saved: $0.0014          │
╰───────────────────────────────────────────────────╯

📊 TOTAL STATS (since startup):
  Requests: 42
  Sessions: 3
  Tokens Saved: 1,240
  Cost Saved: $0.0037
  Avg Compression: 34.2%

⏱️  Last request: 2s ago
```

---

## Project Structure

```
vidurai-proxy/
├── src/
│   ├── main.py                 # Server entry point
│   ├── routes/
│   │   ├── anthropic.py        # Anthropic API routes
│   │   ├── openai.py           # OpenAI API routes
│   │   └── google.py           # Google API routes
│   ├── middleware/
│   │   ├── session_manager.py  # Auto session creation
│   │   ├── vidurai_proxy.py    # Vidurai integration
│   │   └── metrics.py          # Token/cost tracking
│   └── utils/
│       ├── config_loader.py    # YAML config parser
│       ├── provider_detector.py# Auto-detect provider
│       └── terminal_ui.py      # Rich terminal display
├── config/
│   └── config.yaml             # All settings
├── tests/
│   ├── test_proxy.py
│   └── test_vidurai.py
├── logs/
│   └── proxy.log
├── .env.example                # Environment template
├── requirements.txt
└── README.md
```

---

## Environment Variables

```bash
# Required: For Vidurai compression
OPENAI_API_KEY=sk-...

# Optional: Override config.yaml
PROXY_HOST=0.0.0.0
PROXY_PORT=8080
VIDURAI_COMPRESSION_THRESHOLD=10
VIDURAI_REWARD_PROFILE=QUALITY
```

---

## Metrics & Savings

The proxy tracks:

- **Tokens saved**: Original tokens - Compressed tokens
- **Cost saved**: Based on provider pricing
- **Compression ratio**: Compressed / Original
- **Session statistics**: Per-session and aggregate

### Example Savings

Based on Vidurai benchmarks:

| Conversation Length | Tokens Saved | Cost Saved (Claude Sonnet 4.5) |
|---------------------|--------------|--------------------------------|
| 10 messages         | 150          | $0.00045                       |
| 50 messages         | 1,240        | $0.00372                       |
| 100 messages        | 3,600        | $0.01080                       |

*Actual savings vary by conversation content and configuration*

---

## Security

- **Zero Trust**: Proxy never stores user API keys
- **Pass-Through**: API keys forwarded directly to providers
- **Local First**: Runs on localhost by default
- **Audit Logs**: All requests logged (configurable)
- **Open Source**: Full transparency, review the code

---

## Deployment

### Local (Development)

```bash
python src/main.py
```

### Production (systemd)

```bash
# Create systemd service
sudo nano /etc/systemd/system/vidurai-proxy.service
```

```ini
[Unit]
Description=Vidurai Proxy Server
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/home/your-user/vidurai/vidurai-proxy
Environment="PATH=/home/your-user/vidurai/vidurai-proxy/venv/bin"
ExecStart=/home/your-user/vidurai/vidurai-proxy/venv/bin/python src/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable vidurai-proxy
sudo systemctl start vidurai-proxy
```

### Cloud (Docker)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "src/main.py"]
```

---

## Troubleshooting

### Issue: "Connection refused"
**Solution**: Check proxy is running on correct port:
```bash
curl http://localhost:8080/health
```

### Issue: "API key invalid"
**Solution**: Ensure you're using your real provider API key, not proxy key

### Issue: "Compression not working"
**Solution**: Check message threshold in `config.yaml`:
```yaml
vidurai:
  compression_threshold: 10  # Must have 10+ messages
```

---

## Roadmap

- [ ] Vercel serverless deployment
- [ ] Redis session persistence
- [ ] Web dashboard (React)
- [ ] Multi-tenant support
- [ ] Custom compression models
- [ ] Streaming response support
- [ ] Rate limiting
- [ ] Usage quotas

---

## Contributing

Built by Chandan for the Vidurai project.

---

## License

Part of the Vidurai ecosystem.

---

## Links

- **Main Site**: https://vidurai.ai
- **Documentation**: https://docs.vidurai.ai
- **GitHub**: https://github.com/chandantochandan/vidurai
- **Discord**: https://discord.gg/vidurai

---

जय विदुराई! 🕉️
