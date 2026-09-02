# 🛡️ SupplyGuard — Complete Technical Documentation

**Project:** AI Supply Chain Risk Assessment System  
**Architecture:** RAG (Retrieval-Augmented Generation) with LangChain + Gemini  
**Version:** 1.0.0  
**Last Updated:** April 2026

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Technology Stack](#technology-stack)
3. [Architecture Diagram](#architecture-diagram)
4. [Component Breakdown](#component-breakdown)
5. [Data Flow & Workflow](#data-flow--workflow)
6. [API Endpoints](#api-endpoints)
7. [Database Schema](#database-schema)
8. [Configuration & Setup](#configuration--setup)
9. [Error Handling & Resilience](#error-handling--resilience)
10. [Performance Considerations](#performance-considerations)
11. [Deployment Guide](#deployment-guide)

---

## System Overview

### Purpose

SupplyGuard is an advanced proactive supply chain risk assessment platform that leverages Generative AI and Retrieval-Augmented Generation (RAG) to:

- **Identify real-time supply chain risks** from live news feeds and weather data
- **Contextualize risks** using historical disruption patterns and semantic similarity
- **Generate scenarios** for potential supply chain disruptions
- **Provide mitigation strategies** powered by AI intelligence
- **Maintain resilience** with automatic fallback mechanisms when API quotas are exhausted

### Key Capabilities

| Capability             | Description                                                       |
| ---------------------- | ----------------------------------------------------------------- |
| **Risk Assessment**    | Real-time analysis of supply chain vulnerabilities                |
| **Scenario Planning**  | Generate potential disruption scenarios with cascading effects    |
| **Chat Intelligence**  | Conversational interface to explore supply chain knowledge base   |
| **Weather Monitoring** | Live monitoring of critical port/logistics cities                 |
| **News Aggregation**   | Automated collection of supply-chain-related news from RSS feeds  |
| **Historical Context** | 10+ real-world supply chain disruption cases for pattern matching |
| **Fallback Engine**    | Automatic data-driven assessment when LLM quota exceeded          |

---

## Technology Stack

### Frontend

- **Language:** HTML5 + Vanilla CSS + Vanilla JavaScript
- **Framework:** None (zero dependencies for frontend)
- **Styling:** CSS Variables, CSS Grid/Flexbox, Custom Animations
- **State Management:** Client-side JavaScript with async API calls
- **Features:** Responsive dashboard, real-time status updates, dark theme

### Backend

- **Framework:** FastAPI (Python async web framework)
- **Python Version:** 3.10+
- **Server:** Uvicorn (ASGI server)
- **API Style:** REST with JSON payloads

### AI/ML Components

- **LLM:** Google Gemini 2.5 Flash (free tier: 15 RPM, 1M tokens/day)
- **LLM Framework:** LangChain (orchestration, prompt engineering, chains)
- **Vector Store:** ChromaDB (local, persistent, zero-config)
- **Embeddings:** HuggingFace sentence-transformers (`all-MiniLM-L6-v2`)
  - **Model Size:** 22MB, runs on CPU
  - **Embedding Dimension:** 384
  - **Speed:** ~1000 docs per second

### Data Ingestion

- **News Feeds:** feedparser (RSS parsing)
- **Weather Data:** OpenWeatherMap API (free tier)
- **HTTP Requests:** requests library
- **HTML Parsing:** BeautifulSoup4 (for future extensions)

### Database & Storage

- **Vector Database:** ChromaDB (persisted to `vector_store/chroma_db/`)
- **Persistence:** SQLite3 (chroma.sqlite3)
- **Data Format:** JSON documents, stored as embeddings in vector space

### Dependencies

```
langchain==0.3.7
langchain-google-genai==2.0.7
langchain-community==0.3.7
langchain-core==0.3.19
google-generativeai==0.8.3
chromadb==0.5.20
sentence-transformers==3.3.1
fastapi==0.115.5
uvicorn==0.32.1
python-dotenv==1.0.1
requests==2.32.3
feedparser==6.0.11
beautifulsoup4==4.12.3
numpy==1.26.4
pydantic==2.10.3
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          CLIENT LAYER (Browser)                          │
│  HTML5 | Vanilla CSS | Vanilla JS | Dashboard UI | WebSocket Comms     │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         FASTAPI SERVER (Python)                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ API Routes                                                       │   │
│  │  • GET  /api/health          — System status                   │   │
│  │  • GET  /api/data-summary    — Cached data overview            │   │
│  │  • POST /api/assess-risk     — Real-time risk assessment       │   │
│  │  • POST /api/generate-scenarios — Scenario planning            │   │
│  │  • POST /api/chat            — Conversational interface        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
           ┌─────────────────┼─────────────────┐
           ▼                 ▼                 ▼
    ┌─────────────┐  ┌─────────────┐  ┌──────────────┐
    │   Data      │  │   RAG       │  │   Vector     │
    │ Ingestion   │  │  Chains     │  │   Store      │
    │             │  │             │  │              │
    │ • News RSS  │  │ • Risk      │  │ • ChromaDB   │
    │ • Weather   │  │   Assessment│  │ • HF Embeds  │
    │ • Historical│  │ • Scenarios │  │ • Semantic   │
    │   Data      │  │ • Chat      │  │   Search     │
    └─────────────┘  └────────────┬┘  └──────────────┘
                                  │
                     ┌────────────┴─────────────┐
                     ▼                          ▼
            ┌──────────────────┐      ┌──────────────────┐
            │   LLM Service    │      │  Fallback Engine │
            │                  │      │                  │
            │ • Google Gemini  │      │ • Data-driven    │
            │   2.5 Flash      │      │   Analysis       │
            │ • Prompt         │      │ • Pattern Match  │
            │   Engineering    │      │ • No API Calls   │
            │ • Token Mgmt     │      └──────────────────┘
            └──────────────────┘
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
   ┌─────────────┐         ┌──────────────┐
   │ Rate Limit? │         │   Return     │
   │   (Quota)   │────YES──│  Fallback    │
   └──────┬──────┘         │  Response    │
          │                └──────────────┘
          │
         NO
          ▼
    ┌──────────────┐
    │   Return AI  │
    │  Response    │
    └──────────────┘
```

---

## Component Breakdown

### 1. Frontend (`frontend/index.html`)

**Purpose:** Single-Page Application providing interactive UI for risk assessment

**Structure:**

- Responsive dashboard layout using CSS Grid
- Real-time data visualization and charts
- Tabbed interface: Dashboard, Assessment, Scenarios, Chat, Weather
- Dark theme with accent colors (cyan, purple, green)

**Key Features:**

- **Dashboard Tab:** Real-time health status, data summary, quick stats
- **Assessment Tab:** Company profile input form, risk query input, results display
- **Scenarios Tab:** Risk type selection, scenario generation, cascading effect visualization
- **Chat Tab:** Conversational search interface with history
- **Weather Tab:** Live weather alerts for critical ports

**DOM Elements:**

```html
<div id="app">
  <header>
    <!-- Logo, status indicator -->
    <nav>
      <!-- Tab navigation -->
      <div id="dashboard">
        <!-- Dashboard view -->
        <div id="assessment">
          <!-- Risk assessment form -->
          <div id="scenarios">
            <!-- Scenario generation -->
            <div id="chat">
              <!-- Chat interface -->
              <div id="weather"><!-- Weather data display --></div>
            </div>
          </div>
        </div>
      </div>
    </nav>
  </header>
</div>
```

**JavaScript Architecture:**

- Event listeners for form submissions
- Async API calls using `fetch()`
- State management in global scope
- DOM updates via innerHTML and classList manipulation
- Loading states with spinner animations

---

### 2. Backend — Data Ingestion (`backend/data_ingestion.py`)

**Purpose:** Fetch real-time and historical data from multiple sources

**Components:**

#### 2.1 RSS News Feed Parser

```python
def fetch_news_articles(max_per_feed: int = 10) -> List[Dict]
```

**Sources:**

- Reuters World News: `https://feeds.reuters.com/reuters/worldNews`
- Reuters Business: `https://feeds.reuters.com/reuters/businessNews`
- BBC World: `https://feeds.bbci.co.uk/news/world/rss.xml`
- ReliefWeb Disasters: `https://reliefweb.int/disasters/rss.xml`
- GDACS Global Disaster Alerts: `https://www.gdacs.org/xml/rss.xml`

**Keyword Filtering:**

```
supply chain, disruption, shortage, flood, earthquake, hurricane,
typhoon, war, conflict, sanction, strike, port, shipping, logistics,
factory, semiconductor, geopolitical, trade war, tariff, blockade,
pandemic, drought, wildfire, volcano, tsunami, recession
```

**Output Format:**

```json
{
  "source": "reuters_world",
  "title": "article title",
  "summary": "article summary text",
  "link": "https://...",
  "published": "2024-04-22T10:30:00Z",
  "type": "news"
}
```

#### 2.2 Weather Data Fetcher

```python
def fetch_weather_data() -> List[Dict]
```

**Critical Port Cities Monitored:**

- Shanghai (China) — Port volume: 43.3M TEU
- Rotterdam (Netherlands) — Port volume: 14.6M TEU
- Singapore — Port volume: 37.1M TEU
- Los Angeles (USA) — Port volume: 9.4M TEU
- Dubai (UAE) — Port volume: 14.9M TEU
- Navi Mumbai (India) — Port volume: 1.0M TEU
- Surat (India) — Textile hub

**Data Points:**

- Temperature, Wind speed, Weather condition
- Severe weather detection (thunderstorms, snow, extreme winds)
- Timestamp

**Output Format:**

```json
{
  "city": "Shanghai",
  "weather_id": 501,
  "description": "moderate rain",
  "temp_c": 18,
  "wind_kmh": 22.0,
  "is_severe": true,
  "timestamp": "2024-04-22T10:30:00Z",
  "type": "weather"
}
```

**API Integration:**

- **Provider:** OpenWeatherMap (free tier)
- **Rate Limit:** 1000 calls/day
- **Fallback:** Mock weather data if API key missing

#### 2.3 Historical Disruption Database

**Built-in Dataset (10 Events):**

1. **Suez Canal Blockage (2021)** — Logistics impact
2. **COVID-19 Pandemic (2020)** — Global pandemic
3. **Fukushima Nuclear Disaster (2011)** — Natural disaster
4. **Taiwan Semiconductor Shortage (2021)** — Geopolitical
5. **Russia-Ukraine War (2022)** — Geopolitical
6. **US-China Trade War (2018)** — Trade conflict
7. **Thailand Floods (2011)** — Natural disaster
8. **LA Port Strike (2014)** — Labor dispute
9. **Yemen Red Sea Attacks (2023)** — Geopolitical
10. **Panama Canal Drought (2023)** — Natural disaster

**Event Structure:**

```python
{
    "event": "Event name",
    "date": "YYYY-MM-DD",
    "region": "Geographic region",
    "type": "natural_disaster|pandemic|geopolitical|labor|logistics",
    "impact": "Text description of impact",
    "affected_sectors": ["sector1", "sector2"],
    "resolution_days": 180,
    "severity": "low|medium|high|critical",
}
```

#### 2.4 Aggregation Function

```python
def fetch_all_data() -> Dict[str, List[Dict]]
```

Returns combined dictionary:

```python
{
    "news": [...],       # ~20-50 filtered articles
    "weather": [...],    # ~8 port cities
    "historical": [...]  # 10 disruption records
}
```

**Execution Time:** 5-10 seconds per call

---

### 3. Backend — Vector Store (`backend/vector_store.py`)

**Purpose:** Index and retrieve semantically similar documents

#### 3.1 Embeddings Model

```python
def get_embeddings() -> HuggingFaceEmbeddings
```

**Model:** `sentence-transformers/all-MiniLM-L6-v2`

- **Size:** 22MB (lightweight, CPU-friendly)
- **Dimensions:** 384-dimensional vectors
- **Speed:** ~1000 docs/second on CPU
- **Training:** Trained on 1 billion sentence pairs (SBERT)
- **License:** Open source (Apache 2.0)

#### 3.2 Document Conversion

**News Documents:**

```python
def _news_to_doc(item: Dict) -> Document:
    content = f"""[NEWS] {item['title']}
Source: {item['source']}
Published: {item['published']}
Summary: {item['summary']}"""
```

**Weather Documents:**

```python
def _weather_to_doc(item: Dict) -> Document:
    severity = "SEVERE" if item["is_severe"] else "normal"
    content = f"""[WEATHER ALERT - {severity}] {item['city']}
Condition: {item['description']}
Temperature: {item['temp_c']}C, Wind: {item['wind_kmh']} km/h
Supply chain risk: {risk_assessment}
Timestamp: {item['timestamp']}"""
```

**Historical Documents:**

```python
def _historical_to_doc(item: Dict) -> Document:
    content = f"""[HISTORICAL DISRUPTION] {item['event']}
Date: {item['date']}
Region: {item['region']}
Type: {item['type']}
Impact: {item['impact']}
Affected sectors: {sectors}
Severity: {item['severity']}
Resolution time: {item['resolution_days']} days"""
```

#### 3.3 Vector Store Building

```python
def build_vector_store(data: Dict[str, List[Dict]]) -> Chroma
```

**Process:**

1. Convert all data items to LangChain `Document` objects
2. Initialize HuggingFace embeddings model (first run: ~5 seconds download)
3. Create ChromaDB collection with `Chroma.from_documents()`
4. Persist to disk at `vector_store/chroma_db/`
5. Metrics: ~80 documents total, ~30KB index size

**File Structure:**

```
vector_store/
├── chroma_db/
│   ├── chroma.sqlite3           # SQLite metadata
│   ├── {uuid}/
│   │   ├── data_level0.bin      # HNSW index
│   │   ├── header.bin
│   │   ├── length.bin
│   │   └── link_lists.bin
```

#### 3.4 Semantic Retrieval

```python
def retrieve_relevant_context(query: str, vectordb: Chroma, k: int = 6) -> List[Document]
```

**Algorithm:** Cosine similarity search in embedding space

- Query text is embedded to 384D vector
- Finds k=6 nearest documents (default)
- Returns sorted by similarity score (0-1)

**Example Query:**

```
Input: "What are the risks of chip shortage?"
→ Embedded to 384D vector
→ ChromaDB returns top 6 similar documents
→ Mix of Taiwan shortage news, recent semiconductor news, historical docs
```

#### 3.5 Context Formatting

```python
def format_context_for_llm(docs: List[Document]) -> str
```

**Output:**

```
--- Source 1 [NEWS] ---
[NEWS] Semiconductor shortage worsens...
Source: reuters_world
Published: 2024-04-22
Summary: ...

--- Source 2 [WEATHER] ---
[WEATHER ALERT - SEVERE] Shanghai...
Condition: moderate rain
...

--- Source 3 [HISTORICAL] ---
[HISTORICAL DISRUPTION] Taiwan Semiconductor Shortage...
Date: 2021-01-01
...
```

---

### 4. Backend — RAG Chain (`backend/rag_chain.py`)

**Purpose:** Orchestrate LangChain pipelines for AI-powered analysis

#### 4.1 LLM Configuration

```python
def get_llm(temperature: float = 0.7) -> ChatGoogleGenerativeAI
```

**Model:** Google Gemini 2.5 Flash

- **Cost:** Free tier (15 RPM, 1M tokens/day)
- **Speed:** ~50 tokens/second
- **Max Tokens:** 8192 output tokens (per request)
- **Temperature Range:** 0.0 (deterministic) to 1.0 (creative)

**Temperature Settings:**

- Risk Assessment: 0.2 (deterministic, factual)
- Scenario Generation: 0.7 (creative, exploratory)
- Chat: 0.5 (balanced)

#### 4.2 Prompt Templates

**Risk Assessment Prompt:**

```
Input Variables: context, realtime_data, company_profile, query

Key Instructions:
- Respond with ONLY a JSON object (no markdown, no text)
- Prioritize real-time data over historical
- 3-4 risks maximum
- Keep strings concise (1-2 sentences max)
- Specify data_source: "realtime", "historical", or "both"

Output JSON Structure:
{
  "overall_risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
  "risk_score": 0-100,
  "executive_summary": "string",
  "identified_risks": [
    {
      "risk_id": "R001",
      "title": "string",
      "category": "string",
      "severity": "LOW|MEDIUM|HIGH|CRITICAL",
      "probability": "LOW|MEDIUM|HIGH|CRITICAL",
      "affected_regions": ["region"],
      "affected_sectors": ["sector"],
      "description": "string",
      "potential_impact": "string",
      "time_horizon": "short_term|medium_term|long_term",
      "evidence": "string",
      "data_source": "realtime|historical|both"
    }
  ],
  "mitigation_strategies": [
    {
      "risk_id": "R001",
      "strategy": "string",
      "actions": ["action1", "action2"],
      "timeline": "string",
      "cost_estimate": "low|medium|high"
    }
  ],
  "early_warning_indicators": ["indicator1", "indicator2"],
  "recommended_immediate_actions": ["action1", "action2"]
}
```

**Scenario Generation Prompt:**

```
Input Variables: context, scenario_type, region, industry

Generates 3 scenarios with:
- Trigger events
- Cascade effects
- Financial impact estimates
- Historical analogs
- Recovery timelines
```

**Chat Prompt:**

```
Input Variables: context, chat_history, question

Conversational interface maintaining history for multi-turn dialogue
```

#### 4.3 JSON Parsing & Repair

```python
def _safe_parse_json(text: str) -> Dict
```

**Robustness Features:**

1. Strip markdown code fences (`json...`)
2. Direct JSON parsing attempt
3. Extract outermost `{...}` block
4. Attempt repair of truncated JSON (token limit overflow)
5. Close unclosed brackets: `_attempt_repair()`

**Truncation Repair Logic:**

```python
def _attempt_repair(text: str) -> str:
    # Track bracket/brace stack
    # Detect string boundaries (to not count braces inside strings)
    # Close all open brackets at end
    # Remove trailing commas
```

#### 4.4 RiskAssessmentChain Class

```python
class RiskAssessmentChain:
    def __init__(self, vectordb: Chroma)
    def run(query, company_profile, realtime_data, k=6) -> Dict
```

**Execution Flow:**

1. Retrieve top-k documents from ChromaDB
2. Format context string
3. Format real-time data string
4. Invoke LLMChain with all context
5. Parse JSON response
6. Catch rate-limit errors → trigger fallback
7. Attach retrieved sources metadata

#### 4.5 ScenarioGenerationChain Class

```python
class ScenarioGenerationChain:
    def run(scenario_type, region, industry) -> Dict
```

**Generates 3 scenarios** with:

- Probability score (1-10)
- Severity score (1-10)
- Cascade effects
- Financial impact range (USD millions)

#### 4.6 ChatChain Class

```python
class ChatChain:
    def __init__(self, vectordb: Chroma)
    def run(question: str) -> str
```

**Features:**

- Maintains conversation history (last 6 exchanges)
- RAG-powered context retrieval per question
- Multi-turn conversation support

#### 4.7 Fallback Engine

**Triggered When:**

- `chain.invoke()` raises exception (quota exceeded, rate limit, network error)
- LLM returns error response

**Fallback Functions:**

`_build_fallback_assessment():`

- Extracts severe weather from real-time data
- Maps news to company regions
- Calculates average risk score
- Returns identically-structured JSON (no LLM call)

`_build_fallback_scenarios():`

- Uses historical documents as scenario templates
- Generates scenarios by remixing historical patterns
- Maintains same JSON structure

`_build_fallback_chat():`

- Returns retrieved documents formatted as answer
- Alerts user: "AI model temporarily unavailable"
- Suggests retry in 60 seconds

---

### 5. Backend — FastAPI Server (`backend/main.py`)

**Purpose:** HTTP API server orchestrating all components

#### 5.1 Initialization Lifecycle

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    await _initialize_system()
    yield
    # SHUTDOWN (cleanup)
```

**Startup Tasks:**

1. Load environment variables
2. Fetch all data (news, weather, historical)
3. Build vector store (or load from disk)
4. Initialize all chains (Risk, Scenario, Chat)
5. Log initialization status

**Error Handling:**

- Fresh vector store build fails → tries loading from disk
- If both fail → chains remain None, API returns 503

#### 5.2 API Routes

**Route 1: Health Check**

```
GET /api/health

Response:
{
  "status": "ok",
  "vector_store": "ready|unavailable",
  "last_refresh": "2024-04-22T10:30:00Z",
  "api_key_set": true
}
```

**Route 2: Data Summary**

```
GET /api/data-summary

Response:
{
  "news_articles": 42,
  "weather_readings": 8,
  "historical_events": 10,
  "last_refresh": "2024-04-22T10:30:00Z",
  "news_sources": ["reuters_world", "bbc_world", ...],
  "weather_cities": ["Shanghai", "Rotterdam", ...],
  "severe_weather": ["Shanghai", "Singapore"]
}
```

**Route 3: Risk Assessment**

```
POST /api/assess-risk

Request Body:
{
  "query": "Assess current supply chain risks",
  "company_profile": {
    "name": "Tech Corp",
    "industry": "Electronics",
    "regions": ["Asia Pacific", "North America"],
    "key_suppliers": ["TSMC", "Samsung"],
    "critical_inputs": ["semiconductors", "rare earths"]
  }
}

Response:
{
  "success": true,
  "data": {
    "overall_risk_level": "HIGH",
    "risk_score": 75,
    "identified_risks": [...],
    "mitigation_strategies": [...],
    ...
  },
  "timestamp": "2024-04-22T10:30:00Z",
  "realtime_fetch": {
    "news_articles": 42,
    "weather_readings": 8,
    "severe_weather": ["Shanghai"]
  }
}
```

**Route 4: Scenario Generation**

```
POST /api/generate-scenarios

Request Body:
{
  "scenario_type": "natural_disaster",
  "region": "Asia Pacific",
  "industry": "Electronics"
}

Response:
{
  "scenarios": [
    {
      "scenario_id": "S001",
      "title": "Earthquake in Indonesia",
      "probability_score": 7,
      "severity_score": 8,
      "cascade_effects": [...],
      ...
    },
    ...
  ]
}
```

**Route 5: Chat**

```
POST /api/chat

Request Body:
{
  "message": "What are semiconductor supply risks?"
}

Response:
{
  "response": "Based on the knowledge base, semiconductor risks include...",
  "sources": [...]
}
```

#### 5.3 Request Models (Pydantic)

```python
class CompanyProfile(BaseModel):
    name: str
    industry: str
    regions: List[str]
    key_suppliers: List[str]
    critical_inputs: List[str]

class RiskAssessmentRequest(BaseModel):
    query: str
    company_profile: Optional[CompanyProfile]

class ScenarioRequest(BaseModel):
    scenario_type: str
    region: str
    industry: str

class ChatRequest(BaseModel):
    message: str
```

#### 5.4 CORS & Static Files

```python
app.add_middleware(CORSMiddleware, allow_origins=["*"])
app.mount("/static", StaticFiles(directory="frontend/"))
```

---

## Data Flow & Workflow

### Complete Request Lifecycle (Risk Assessment)

```
1. USER INTERACTION (Frontend)
   ├─ User fills company profile
   ├─ User enters risk query
   └─ User clicks "Assess Risk" button

2. API REQUEST
   ├─ JavaScript: fetch POST /api/assess-risk
   ├─ Headers: Content-Type: application/json
   └─ Body: { query, company_profile }

3. BACKEND RECEPTION (main.py)
   ├─ FastAPI parses request → RiskAssessmentRequest object
   ├─ Validates Pydantic model
   └─ Routes to assess_risk() handler

4. REAL-TIME DATA FETCH
   ├─ fetch_news_articles(max_per_feed=5)
   │  ├─ Fetch 5 articles per RSS feed
   │  ├─ Filter by risk keywords
   │  └─ Return ~20-50 filtered articles
   ├─ fetch_weather_data()
   │  ├─ Call OpenWeatherMap for 8 port cities
   │  └─ Return weather readings
   └─ Assemble realtime_data dict with timestamp

5. RAG CONTEXT RETRIEVAL (rag_chain.py)
   ├─ Call retrieve_relevant_context(query, k=6)
   ├─ Embed query to 384D vector
   ├─ ChromaDB cosine similarity search
   ├─ Return top 6 documents (sorted by similarity)
   └─ Format documents into context string

6. PROMPT CONSTRUCTION
   ├─ Format company_profile as JSON
   ├─ Format realtime_data as readable text
   ├─ Combine with RISK_ASSESSMENT_PROMPT template
   └─ Final prompt: ~2-3K tokens

7. LLM INVOCATION (chain.invoke)
   ├─ Send prompt to Google Gemini 2.5 Flash
   ├─ Wait for response (2-5 seconds typical)
   └─ Receive JSON response string

8. RESPONSE PARSING
   ├─ _safe_parse_json(response_text)
   ├─ Strip markdown fences
   ├─ Direct parse attempt
   ├─ If fails: extract { } block
   ├─ If fails: attempt repair
   └─ Return parsed Dict

9. SUCCESS RESPONSE
   ├─ Attach retrieved_sources metadata
   ├─ Attach realtime_summary
   ├─ Wrap in { success: true, data: ..., timestamp }
   └─ Return to frontend

10. FALLBACK (if LLM error)
    ├─ Catch exception (rate limit, timeout, etc)
    ├─ Call _build_fallback_assessment()
    ├─ Analyze realtime_data + historical docs
    ├─ Return data-driven assessment (identical JSON structure)
    ├─ Flag: { fallback: true, llm_error: "..." }
    └─ Return to frontend (same status code)

11. FRONTEND RENDERING
    ├─ Receive response
    ├─ Extract identified_risks array
    ├─ Extract mitigation_strategies
    ├─ Render risk cards (severity color-coded)
    ├─ Render mitigation timeline
    ├─ Display weather alerts
    └─ Update UI with results
```

### Scenario Generation Workflow

```
1. User selects scenario parameters:
   ├─ Scenario type: natural_disaster|geopolitical|pandemic|labor
   ├─ Region: Asia Pacific|Europe|Americas|Middle East
   └─ Industry: Electronics|Automotive|Pharma|Food

2. Backend:
   ├─ Retrieve historical + current data matching scenario parameters
   ├─ Build query: "{scenario_type} {region} {industry}"
   ├─ Retrieve top-5 similar documents from ChromaDB
   ├─ Invoke ScenarioGenerationChain
   └─ Generate 3 distinct scenarios

3. Each scenario includes:
   ├─ Probability score (1-10)
   ├─ Severity score (1-10)
   ├─ Trigger events
   ├─ Cascade effects
   ├─ Affected supply chain nodes
   ├─ Estimated recovery days
   ├─ Financial impact estimate
   └─ Historical analog (reference event)

4. Frontend displays:
   ├─ Scenario cards with probability/severity heatmap
   ├─ Timeline of cascade effects
   ├─ Financial impact range
   └─ Recovery period timeline
```

### Chat Workflow

```
1. User types question (e.g., "What are semiconductor risks?")

2. Backend:
   ├─ Retrieve top-5 documents matching question
   ├─ Include conversation history (last 6 exchanges)
   ├─ Invoke ChatChain with context + history
   ├─ LLM generates contextual answer
   └─ Format response with source references

3. Frontend:
   ├─ Display answer
   ├─ Show source citations
   ├─ Add to chat history
   └─ Enable follow-up questions
```

---

## API Endpoints

### Complete API Reference

| Method | Endpoint                  | Purpose              | Status Code |
| ------ | ------------------------- | -------------------- | ----------- |
| GET    | `/`                       | Serve index.html     | 200         |
| GET    | `/api/health`             | System health status | 200         |
| GET    | `/api/data-summary`       | Cached data overview | 200/503     |
| POST   | `/api/assess-risk`        | Risk assessment      | 200/500/503 |
| POST   | `/api/generate-scenarios` | Scenario generation  | 200/500/503 |
| POST   | `/api/chat`               | Chat interface       | 200/500/503 |

### Error Responses

```json
// 503 Vector Store Unavailable
{
  "detail": "Vector store not initialized. Check GOOGLE_API_KEY in .env"
}

// 500 General Error
{
  "detail": "Error message describing the failure"
}

// 429 Rate Limited (caught internally)
// Automatically triggers fallback response (200 OK)
{
  "success": true,
  "data": { /* fallback assessment */ },
  "fallback": true,
  "llm_error": "Rate limit exceeded"
}
```

---

## Database Schema

### ChromaDB Collection Schema

**Collection Name:** `supply_chain_risks`

**Document Metadata Fields:**

```python
{
  "type": "news|weather|historical",
  "source": "reuters_world|bbc_world|...",
  "date": "YYYY-MM-DDTHH:MM:SSZ",
  "link": "https://...",        # for news
  "city": "Shanghai",           # for weather
  "is_severe": "true|false",    # for weather
  "event": "Event name",        # for historical
  "region": "Region name",      # for historical
  "severity": "low|medium|high|critical"  # for historical
}
```

**Document Vectors:**

- Dimension: 384
- Algorithm: Cosine similarity
- Normalization: L2 normalized

**Retrieval Query:**

```sql
-- Pseudocode (ChromaDB uses approximate nearest neighbor search)
SELECT documents
FROM supply_chain_risks
WHERE cosine_similarity(query_embedding, document_embedding) > threshold
ORDER BY cosine_similarity DESC
LIMIT 6
```

### Vector Store Persistence

**File Structure:**

```
vector_store/
├── chroma_db/
│   ├── chroma.sqlite3          -- SQLite metadata
│   └── {collection_id}/        -- Collection directory
│       ├── data_level0.bin     -- HNSW index (Hierarchical Navigable Small World)
│       ├── header.bin          -- Index metadata
│       ├── length.bin          -- Document length info
│       └── link_lists.bin      -- Graph connectivity
```

**Index Type:** HNSW (Hierarchical Navigable Small World)

- Approximate nearest neighbor search
- O(log n) search complexity
- Fast retrieval with ~99% accuracy

---

## Configuration & Setup

### Environment Setup

**Step 1: Create `.env` file**

```bash
# In project root directory
echo "GOOGLE_API_KEY=your_key_here" > .env
```

**Step 2: Get Google API Key**

- Visit: https://aistudio.google.com/apikey
- Create new API key
- Copy to `.env`

**Step 3: Optional Weather API**

```bash
echo "WEATHER_API_KEY=your_openweathermap_key" >> .env
```

### Dependencies Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Running the Server

**Option 1: One-command launch (recommended)**

```bash
python run.py
# Runs: uvicorn backend.main:app --reload --port 8000
```

**Option 2: Manual launch**

```bash
uvicorn backend.main:app --reload --port 8000
```

**Output:**

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
[STARTUP] Initializing Supply Chain Risk System...
[INFO] Fetching news articles...
[INFO] Fetching weather data...
[INFO] Loading historical disruptions...
[STARTUP] Vector store built successfully.
[STARTUP] All chains initialized. System ready.
```

**Access Dashboard:**

- Open browser: http://localhost:8000
- Or: http://127.0.0.1:8000

### Configuration Parameters

**FastAPI:**

```python
app = FastAPI(
    title="Supply Chain Risk Assessment API",
    version="1.0.0",
    lifespan=lifespan
)
```

**LLM Temperature Settings:**

```python
Risk Assessment:     temperature=0.2  (deterministic)
Scenario Generation: temperature=0.7  (creative)
Chat:               temperature=0.5  (balanced)
```

**Retrieval Parameters:**

```python
k=6          # Number of documents to retrieve
max_tokens=8192  # Max output tokens from Gemini
```

**Data Fetching:**

```python
max_per_feed=5      # News articles per RSS feed
news_keywords=[...] # Risk-related keywords for filtering
major_cities=[...]  # 8 critical port cities for weather
```

---

## Error Handling & Resilience

### Multi-Layer Error Handling

#### Layer 1: Data Ingestion Errors

```python
try:
    feed = feedparser.parse(url)
except Exception as e:
    print(f"[WARN] Feed {source} failed: {e}")
    # Continue with other feeds
```

**Resilience:** If one RSS feed fails, system continues with others

#### Layer 2: Weather API Errors

```python
if not api_key:
    return _mock_weather_data()  # Fallback to mock data

try:
    resp = requests.get(url, timeout=5)
except Exception as e:
    print(f"[WARN] Weather fetch failed for {city}: {e}")
    # Continue with other cities
```

**Resilience:** System works without weather API key (uses mock data)

#### Layer 3: Vector Store Errors

```python
try:
    _vectordb = build_vector_store(_data_cache)
except Exception as e:
    print(f"[WARN] Fresh vector store failed: {e}")
    try:
        _vectordb = load_vector_store()  # Load from disk
    except Exception as e2:
        print(f"[ERROR] No vector store available: {e2}")
        _vectordb = None
```

**Resilience:** Uses cached vector store if fresh build fails

#### Layer 4: LLM Rate Limiting

```python
try:
    result_dict = self.chain.invoke({...})
except Exception as e:
    if "429" in str(e) or "quota" in str(e).lower():
        result = _build_fallback_assessment(docs, realtime_data, ...)
        result["fallback"] = True
```

**Resilience:** Automatic fallback to data-driven assessment

#### Layer 5: JSON Parsing Errors

```python
def _safe_parse_json(text: str) -> Dict:
    try:
        return json.loads(text)  # Direct parse
    except:
        try:
            return json.loads(text[start:end])  # Extract block
        except:
            text = _attempt_repair(text)  # Repair truncation
            return json.loads(text)  # Final attempt
```

**Resilience:** Repairs truncated JSON responses

### Fallback Response Structure

**Key Feature:** Fallback responses maintain identical JSON structure to AI responses

```python
# AI Response
{
  "overall_risk_level": "HIGH",
  "risk_score": 75,
  "identified_risks": [...]
}

# Fallback Response (same structure, different source)
{
  "overall_risk_level": "HIGH",
  "risk_score": 72,  # Calculated from data
  "identified_risks": [...]  # From real-time + historical data
  "fallback": true,  # Additional flag
  "llm_error": "Rate limit exceeded"
}
```

**Frontend Compatibility:** No code changes needed — same response handling

### Error Codes & Meanings

| Code | Meaning                   | Fallback               |
| ---- | ------------------------- | ---------------------- |
| 200  | Success (AI or fallback)  | Automatic              |
| 429  | Rate limit (Gemini quota) | Automatic fallback     |
| 503  | Vector store unavailable  | Endpoint returns error |
| 500  | Unexpected error          | Some fallback support  |

---

## Performance Considerations

### Response Time Breakdown (Risk Assessment)

```
Component                          Time        Notes
─────────────────────────────────────────────────────
API request received               1ms
Data validation                    1ms
Real-time news fetch               3-5s        RSS feeds + filtering
Real-time weather fetch            2-3s        8 API calls (parallel)
Vector store retrieval             50ms        Similarity search
LLM invocation (Gemini)            3-5s        API round-trip + processing
JSON parsing                       10ms
Response formatting                5ms
─────────────────────────────────────────────────────
Total (with LLM)                   8-15s
Total (fallback, no LLM)           5-8s
```

### Optimization Strategies

**1. Data Fetching**

```python
# Parallel fetching of news + weather
news = fetch_news_articles()       # 3-5s
weather = fetch_weather_data()     # 2-3s
# Runs sequentially, but weather is faster than news overall
```

**Future:** Use asyncio for true parallelization

**2. Vector Store**

- HNSW index: O(log n) search
- 80 documents: ~6 similarity comparisons
- Result: 50ms retrieval time

**3. LLM Temperature**

- Risk Assessment: temperature=0.2 (faster, deterministic)
- Scenario Generation: temperature=0.7 (slower, creative)

**4. Token Optimization**

```
News: 50-100 tokens each
Weather: 20-50 tokens each
Historical: 100-150 tokens each
Context total: ~800-1000 tokens
Prompt template: ~300 tokens
Reserve: ~6000 tokens for output
= 8192 max tokens (comfortable buffer)
```

### Caching Strategy

**Current:** None (fresh fetch on every request)

**Potential Improvements:**

- Cache vector store in memory (already done)
- Cache news articles for 5 minutes
- Cache weather data for 15 minutes
- Cache LLM responses for identical queries

### Scalability Limits

**Current Bottlenecks:**

1. Gemini API rate limit: 15 RPM (1 request per 4 seconds)
2. Data ingestion time: 5-10 seconds per cycle
3. Frontend: Single-threaded JavaScript

**Scaling Options:**

- Use queue system (Celery, RabbitMQ) for async processing
- Cache results more aggressively
- Upgrade to higher Gemini tier (paid)
- Add load balancer for multiple servers

---

## Deployment Guide

### Development Deployment

**Local Machine Setup:**

```bash
# Clone repository
git clone <repo_url>
cd supply_chain_risk

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with GOOGLE_API_KEY

# Run server
python run.py
```

**Access:**

- Dashboard: http://localhost:8000
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Production Deployment (Linux Server)

**Step 1: Server Setup**

```bash
# SSH into server
ssh user@server.com

# Clone repository
git clone <repo_url>
cd supply_chain_risk

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env
nano .env
# Add: GOOGLE_API_KEY=<your_key>
```

**Step 2: Systemd Service (auto-restart)**

```bash
# Create service file
sudo nano /etc/systemd/system/supplyguard.service
```

```ini
[Unit]
Description=SupplyGuard Supply Chain Risk API
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/home/user/supply_chain_risk
Environment="PATH=/home/user/supply_chain_risk/venv/bin"
ExecStart=/home/user/supply_chain_risk/venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable supplyguard
sudo systemctl start supplyguard

# Check status
sudo systemctl status supplyguard
```

**Step 3: Nginx Reverse Proxy**

```bash
# Install Nginx
sudo apt-get install nginx

# Configure
sudo nano /etc/nginx/sites-available/supplyguard
```

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 60s;
    }
}
```

```bash
# Enable and restart
sudo ln -s /etc/nginx/sites-available/supplyguard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**Step 4: SSL Certificate (Let's Encrypt)**

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### Docker Deployment

**Dockerfile:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create vector store directory
RUN mkdir -p vector_store/chroma_db

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/api/health')"

# Run
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml:**

```yaml
version: "3.8"

services:
  supplyguard:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - WEATHER_API_KEY=${WEATHER_API_KEY}
    volumes:
      - ./vector_store:/app/vector_store
    restart: always
```

**Build and Run:**

```bash
docker-compose up -d
docker-compose logs -f
```

### Monitoring & Logging

**Log Files (Production):**

```bash
# Systemd logs
sudo journalctl -u supplyguard -f

# Application logs
tail -f /var/log/supplyguard.log
```

**Health Monitoring:**

```bash
# Check health endpoint
curl http://localhost:8000/api/health

# Expected response:
{
  "status": "ok",
  "vector_store": "ready",
  "last_refresh": "2024-04-22T10:30:00Z",
  "api_key_set": true
}
```

**Metrics to Monitor:**

- API response time (target: <15s)
- Error rate (target: <1%)
- Vector store size
- Gemini API quota usage
- Memory usage (target: <500MB)
- CPU usage (target: <20%)

---

## Troubleshooting Guide

### Common Issues

**Issue 1: "GOOGLE_API_KEY not set" Error**

```
Solution:
1. Get key from https://aistudio.google.com/apikey
2. Create .env file with: GOOGLE_API_KEY=your_key
3. Restart server
```

**Issue 2: Vector Store Not Found**

```
Solution:
1. Delete vector_store/ folder
2. Restart server (will rebuild from scratch)
3. Server will re-fetch data and rebuild
```

**Issue 3: Rate Limit Error (429)**

```
Solution:
- Gemini has 15 RPM limit on free tier
- System automatically uses fallback
- Wait 60 seconds before next request
- Or upgrade to paid Gemini tier
```

**Issue 4: Slow Response Times (>20s)**

```
Solution:
- Check internet connection
- Verify RSS feeds are accessible
- Check OpenWeatherMap API availability
- Monitor server CPU/memory
- Consider caching strategy
```

**Issue 5: News Feed Returns 0 Articles**

```
Solution:
- Check internet connectivity
- Verify RSS feed URLs are still active
- Check risk keyword filtering (may be too restrictive)
- Try manual feed testing:
  python -m backend.data_ingestion
```

### Debug Mode

**Enable Verbose Logging:**

```python
# In backend/main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Test Individual Components:**

```bash
# Test data ingestion
python -m backend.data_ingestion

# Test vector store
python -c "from backend.vector_store import *; print(load_vector_store())"

# Test LLM chain
python -c "from backend.rag_chain import *; print(get_llm())"
```

---

## Appendix

### Architecture Decision Records (ADR)

**ADR-001: Why ChromaDB?**

- Lightweight, no external DB needed
- Local persistence (works offline)
- Python-native integration
- Free and open-source

**ADR-002: Why HuggingFace Embeddings?**

- No API key required
- Fast on CPU (22MB model)
- High-quality semantic embeddings
- Works offline after first download

**ADR-003: Why Fallback Engine?**

- Gemini free tier has quota limits
- Users expect consistent service
- Data-driven assessment is valuable
- Maintains identical response structure

**ADR-004: Why Vanilla JS Frontend?**

- No framework bloat
- Single HTML file deployment
- Works on any browser
- Minimal dependencies

### Future Enhancement Ideas

1. **Multi-Language Support**
   - Translate prompts and responses
   - Support non-English news sources

2. **Real-Time Dashboard**
   - WebSocket updates for live data
   - Real-time risk score updates

3. **Advanced Analytics**
   - Risk trend tracking
   - Supply chain network visualization
   - Impact simulation engine

4. **Integration APIs**
   - Webhook support for external systems
   - Export to JSON/CSV/PDF

5. **Machine Learning**
   - Fine-tune risk scoring model
   - Anomaly detection on risk patterns
   - Predictive risk modeling

6. **Multi-Tenancy**
   - Support multiple organizations
   - Custom risk parameters per company
   - Role-based access control

---

## Glossary

| Term                  | Definition                                                  |
| --------------------- | ----------------------------------------------------------- |
| **RAG**               | Retrieval-Augmented Generation — combining search with LLM  |
| **Embedding**         | Numerical vector representation of text (384D)              |
| **ChromaDB**          | Vector database for similarity search                       |
| **LangChain**         | Framework for building LLM applications                     |
| **HNSW**              | Hierarchical Navigable Small World — fast similarity search |
| **RPM**               | Requests Per Minute (API rate limit)                        |
| **Fallback**          | Data-driven alternative when LLM is unavailable             |
| **Token**             | Unit of text (typically 4 characters)                       |
| **Cosine Similarity** | Measure of text similarity (0-1)                            |
| **TEU**               | Twenty-foot Equivalent Unit (shipping container)            |
| **Cascade Effects**   | Downstream impacts of a disruption                          |

---

## References

- [LangChain Documentation](https://python.langchain.com)
- [ChromaDB Docs](https://docs.trychroma.com)
- [Google Gemini API](https://ai.google.dev)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [HuggingFace Transformers](https://huggingface.co/transformers)
- [OpenWeatherMap API](https://openweathermap.org/api)

---

**Document Version:** 1.0  
**Last Updated:** April 22, 2026  
**Maintained By:** SupplyGuard Development Team
