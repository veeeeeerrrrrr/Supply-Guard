# How Historical Data Helps Process New Prompts in RAG_MPR System

## 📋 Executive Summary

Your RAG (Retrieval-Augmented Generation) system leverages historical data as a **contextual foundation** to analyze new prompts in combination with real-time news and weather data. Historical case studies provide:

1. **Pattern Recognition** - Identify recurring disruption types
2. **Baseline Comparison** - Compare current risks against past severity
3. **Predictive Anchoring** - Estimate recovery times and financial impacts
4. **Contextual Intelligence** - Understand regional/sectoral vulnerabilities
5. **Decision Support** - Provide proven mitigation strategies from past incidents

---

## 🔄 Complete Data Flow: New Prompt Processing

```
┌─────────────────────────────────────────────────────────────┐
│ USER SUBMITS NEW PROMPT (e.g., "Assess risks for electronics")│
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────────┐
        │ REAL-TIME DATA INGESTION LAYER   │
        ├──────────────────────────────────┤
        │ • RSS News Feeds (Reuters, BBC)  │
        │ • Weather API (OpenWeatherMap)   │
        │ • GDACS Disaster Alerts          │
        │ [FETCHED FRESH FOR EACH QUERY]   │
        └──────────────┬───────────────────┘
                       │
                       ▼
        ┌──────────────────────────────────────────────┐
        │ VECTOR STORE RETRIEVAL (ChromaDB)             │
        ├──────────────────────────────────────────────┤
        │ Historical Disruptions:                      │
        │ • Suez Canal Blockage (2021)                 │
        │ • COVID-19 Disruption (2020)                 │
        │ • Fukushima Nuclear Disaster (2011)          │
        │ • Taiwan Semiconductor Shortage (2021)       │
        │ • Russia-Ukraine War Impact (2022)           │
        │ [VECTORIZED + MATCHED TO QUERY]              │
        └──────────────┬───────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────────────────────┐
        │ UNIFIED CONTEXT CONSTRUCTION                  │
        ├──────────────────────────────────────────────┤
        │ 1. REAL-TIME DATA (formatted)                │
        │    - Current news articles                   │
        │    - Live weather alerts                     │
        │    - Immediate threats                       │
        │                                              │
        │ 2. HISTORICAL CONTEXT (retrieved docs)       │
        │    - Past disruption patterns                │
        │    - Recovery timelines                      │
        │    - Cascade effects                         │
        │    - Financial impacts                       │
        │                                              │
        │ 3. COMPANY PROFILE (input parameters)        │
        │    - Industry, regions, suppliers            │
        │    - Critical inputs                         │
        └──────────────┬───────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────────────────────┐
        │ LLM PROMPT INJECTION (Google Gemini)          │
        ├──────────────────────────────────────────────┤
        │ Template includes:                           │
        │ - Company context                            │
        │ - Historical/vector DB context               │
        │ - Real-time data (WEIGHTED HIGHER)           │
        │ - Instructions for analysis                  │
        └──────────────┬───────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────────────────────┐
        │ LLM GENERATES STRUCTURED RESPONSE             │
        ├──────────────────────────────────────────────┤
        │ JSON output with:                            │
        │ • Overall risk level                         │
        │ • Identified risks (3-4 max)                 │
        │ • Evidence sources (realtime/historical/both)│
        │ • Mitigation strategies                      │
        │ • Early warning indicators                   │
        │ • Recommended actions                        │
        └──────────────┬───────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────────────────────┐
        │ USER RECEIVES INTEGRATED RISK ASSESSMENT      │
        └──────────────────────────────────────────────┘
```

---

## 🗂️ Types of Historical Data Used

### **1. Historical Disruptions Database**

Located in: `backend/data_ingestion.py` (HISTORICAL_DISRUPTIONS list)

```python
HISTORICAL_DISRUPTIONS = [
    {
        "event": "Suez Canal Blockage (Ever Given)",
        "date": "2021-03-23",
        "region": "Middle East / Egypt",
        "type": "logistics",
        "impact": "Blocked ~12% of global trade for 6 days. $9.6B/day in delayed goods.",
        "affected_sectors": ["shipping", "oil", "manufacturing", "retail"],
        "resolution_days": 6,
        "severity": "critical",
    },
    # More entries...
]
```

**Key historical events indexed:**

- ✓ **Suez Canal Blockage** (2021) - Logistics disruption
- ✓ **COVID-19 Pandemic** (2020) - Pandemic/supply chain collapse
- ✓ **Fukushima Nuclear Disaster** (2011) - Natural disaster cascade
- ✓ **Taiwan Semiconductor Shortage** (2021) - Geopolitical/supply constraint
- ✓ **Russia-Ukraine War** (2022) - Geopolitical/commodity impact

---

## 🧠 How Historical Data Helps Analyze New Prompts

### **Scenario 1: User Asks "Assess electronics manufacturing risks in Asia Pacific"**

#### **Step 1: Real-Time Data Fetch**

```
- Reuters/BBC feeds scanned for:
  "semiconductor", "supply chain", "Asia", "disruption"
- OpenWeatherMap checked for severe weather in:
  Shanghai, Singapore, Navi Mumbai
- Latest articles ingested (e.g., recent trade news, weather alerts)
```

#### **Step 2: Vector Store Retrieval**

Your query gets embedded and matched against stored documents:

```
Query embedding: "electronics manufacturing risks in Asia Pacific"
         ↓
Similarity search returns (k=6 documents):
  [1] Taiwan Semiconductor Shortage (2021) ← HIGHLY RELEVANT
  [2] COVID-19 Disruption (2020) ← RELEVANT (Asia impact)
  [3] Suez Canal Blockage (2021) ← SOMEWHAT RELEVANT (shipping routes)
  [4] Recent Reuters article on chip exports
  [5] Current weather in Shanghai
  [6] Fukushima impacts (2011) ← HISTORICAL ANALOG
```

#### **Step 3: Unified Context Construction**

```
CONTEXT PASSED TO LLM:
═════════════════════════════════════════════════════════════

REAL-TIME DATA (fetched now):
  • Shanghai moderate rain, 18°C → port operations alert
  • 3 Reuters articles on Taiwan supply constraints
  • No severe weather in Singapore today

HISTORICAL CONTEXT (from vector store):
  • Taiwan Semiconductor Shortage (2021):
    - 18-month resolution time
    - Affected: automotive, consumer electronics
    - Root cause: geopolitical tensions + demand surge
    - Pattern: shortage cascaded through 6 supply tiers

  • COVID-19 Pandemic (2020):
    - 24-month disruption globally
    - Asia particularly affected
    - Recovery: staggered by region

COMPANY PROFILE:
  • Industry: Electronics Manufacturing
  • Regions: Asia Pacific
  • Key Suppliers: Taiwan, South Korea
  • Critical Inputs: Semiconductors, Rare Metals

═════════════════════════════════════════════════════════════
```

#### **Step 4: LLM Analysis with Weighted Evidence**

The **RISK_ASSESSMENT_PROMPT** in `rag_chain.py` instructs Gemini:

```python
IMPORTANT: Give higher weight to the REAL-TIME DATA when assessing
current risks, but also use historical context for patterns and analogies.
Clearly cite whether evidence comes from real-time or historical data.
```

#### **Step 5: Structured Output Example**

```json
{
  "overall_risk_level": "MEDIUM",
  "risk_score": 65,
  "executive_summary": "Current semiconductor supply constraints mirror 2021 Taiwan shortage patterns. Live weather in Shanghai may compound near-term logistics delays.",
  "identified_risks": [
    {
      "risk_id": "R001",
      "title": "Taiwan Supply Constraint (Geopolitical)",
      "category": "geopolitical",
      "severity": "HIGH",
      "probability": "HIGH",
      "affected_regions": ["Asia Pacific"],
      "affected_sectors": ["Electronics"],
      "description": "Ongoing trade tensions affecting semiconductor exports.",
      "potential_impact": "Electronics manufacturing could face 12-18 month supply delays (similar to 2021 event).",
      "time_horizon": "medium_term",
      "evidence": "Recent Reuters articles + historical 2021 shortage precedent.",
      "data_source": "both"  ← COMBINES real-time + historical
    },
    {
      "risk_id": "R002",
      "title": "Severe Weather - Shanghai Port",
      "category": "weather",
      "severity": "MEDIUM",
      "probability": "MEDIUM",
      "affected_regions": ["Shanghai"],
      "affected_sectors": ["Shipping", "Logistics"],
      "description": "Moderate rain, 22 km/h winds affecting port operations.",
      "potential_impact": "Short-term container handling delays (1-3 days typically).",
      "time_horizon": "short_term",
      "evidence": "OpenWeatherMap live data.",
      "data_source": "realtime"  ← PURE real-time
    }
  ],
  "mitigation_strategies": [
    {
      "risk_id": "R001",
      "strategy": "Diversify Semiconductor Sourcing",
      "actions": [
        "Increase purchases from South Korea suppliers",
        "Develop alternatives from Malaysia/Singapore",
        "Negotiate 6-month forward contracts (historically, this mitigates 2021-type events)"
      ],
      "timeline": "2-3 months",
      "cost_estimate": "medium"
    }
  ],
  "early_warning_indicators": [
    "Taiwan export licenses declined month-over-month",
    "Shipping costs Shanghai-to-US increased 40%",
    "Lead times for chip orders extended beyond 90 days (pre-2021 shock: 30 days)"
  ],
  "recommended_immediate_actions": [
    "Check current inventory levels vs. 2021 crisis reserves",
    "Activate secondary sourcing agreements",
    "Monitor Shanghai port operations during wet season"
  ]
}
```

---

## 📊 How Historical Data Improves Analysis

### **1. Pattern Recognition**

**Without Historical Data:**

```
"Shanghai has rain today. Risk = MEDIUM"
❌ Lacks context about typical impact duration
```

**With Historical Data:**

```
"Shanghai rain today + historical data shows:
- COVID-19 (2020): Shanghai ports recovered in 8 days
- Suez blockage (2021): cascading delays lasted 6 days
- Typical weather disruption: 1-3 days
Risk = MEDIUM (expected recovery: 1-3 days)"
✅ Informed baseline
```

### **2. Severity Calibration**

**Without Historical Data:**

```
"Taiwan supply issues detected"
Risk = MEDIUM (guess based on keywords)
```

**With Historical Data:**

```
"Taiwan supply issues detected.
Historical analog: 2021 Taiwan Semiconductor Shortage
- Lasted: 18 months
- Financial impact: $100B+ globally
- Resolution: 3-tier intervention (demand + supply + policy)
Risk = HIGH (severity calibrated to past precedent)
Recovery estimate: 6-12 months"
✅ Evidence-based severity
```

### **3. Impact Prediction**

**Without Historical Data:**

```
"Electronics manufacturing affected"
❌ No recovery timeline estimate
```

**With Historical Data:**

```
"Electronics manufacturing affected.
Historical precedents:
- COVID-19 impact: 24-month recovery (Asia took longer)
- Taiwan shortage: 18-month resolution
- Fukushima crisis: 6-month recovery
Expected recovery: 12-18 months (weighted by similarity to current situation)"
✅ Predictive timeline
```

### **4. Cascading Effects Identification**

**Without Historical Data:**

```
"Shanghai port disrupted"
❌ Limited understanding of cascade
```

**With Historical Data:**

```
"Shanghai port disrupted.
From Suez blockage (2021):
- Tier 1: Direct shipping delay → 6 days
- Tier 2: Container availability shortage → 12 days
- Tier 3: Secondary port congestion → 18 days
- Tier 4: Supplier production delays → 30+ days
Cascading effects expected to compound this issue"
✅ Multi-tier impact modeling
```

### **5. Regional Vulnerability Context**

**Without Historical Data:**

```
"Risk detected in Asia Pacific"
❌ Too broad
```

**With Historical Data:**

```
"Risk detected in Asia Pacific.
Regional history shows:
- Taiwan: Critical semiconductor hub (2021 shortage)
- Shanghai: 4 major disruptions (COVID, weather, Suez impact)
- Singapore: Resilient (only weather impacts)
Highest vulnerability: Taiwan supply chain"
✅ Prioritized hotspots
```

---

## 🔍 Technical Implementation Details

### **Vector Store Architecture** (`backend/vector_store.py`)

```python
def build_vector_store(data: Dict[str, List[Dict]]) -> Chroma:
    """Convert all data types into embeddings"""
    docs: List[Document] = []

    # News articles → documents
    for item in data.get("news", []):
        docs.append(_news_to_doc(item))  # [NEWS] Title, Source, Published, Summary

    # Weather data → documents
    for item in data.get("weather", []):
        docs.append(_weather_to_doc(item))  # [WEATHER] City, Condition, Impact

    # HISTORICAL data → documents
    for item in data.get("historical", []):
        docs.append(_historical_to_doc(item))  # [HISTORICAL] Event, Date, Region, Impact

    # All embedded using HuggingFace sentence-transformers
    embeddings = get_embeddings()  # all-MiniLM-L6-v2 model
    vectordb = Chroma.from_documents(documents=docs, embedding=embeddings)
    return vectordb
```

### **Retrieval Process** (`backend/vector_store.py`)

```python
def retrieve_relevant_context(query: str, vectordb: Chroma, k: int = 6) -> List[Document]:
    """For each new query, retrieve top-6 most similar documents (mix of types)"""
    retriever = vectordb.as_retriever(search_kwargs={"k": 6})
    docs = retriever.invoke(query)  # Semantic similarity search
    # Returns mix of:
    # - Historical events relevant to query
    # - Live news articles relevant to query
    # - Weather data relevant to query
    return docs
```

### **Context Formatting** (`backend/rag_chain.py`)

```python
def _format_realtime_data(data: Dict) -> str:
    """Format fetched real-time + historical data for LLM"""
    sections = []
    sections.append(f"[Data fetched at: {timestamp}]")

    # News section
    sections.append(f"\n── LIVE NEWS ({len(news)} articles) ──")
    for article in news[:10]:
        sections.append(f"  • {article['title']}")

    # Weather section
    sections.append(f"\n── LIVE WEATHER ({len(weather)} cities) ──")
    for w in weather:
        sections.append(f"  • {w['city']}: {w['description']}")

    return "\n".join(sections)
```

### **Prompt Template** (`backend/rag_chain.py`)

```python
RISK_ASSESSMENT_PROMPT = PromptTemplate(
    input_variables=["context", "realtime_data", "company_profile", "query"],
    template="""
Company: {company_profile}

HISTORICAL & VECTOR-DB CONTEXT (previously indexed data):
{context}

REAL-TIME DATA (fetched just now — news, weather, live alerts):
{realtime_data}

Query: {query}

IMPORTANT: Give higher weight to the REAL-TIME DATA when assessing
current risks, but also use historical context for patterns and analogies.
Clearly cite whether evidence comes from real-time or historical data.

Return JSON with identified_risks array containing:
{
  "data_source": "realtime or historical or both"
}
"""
)
```

---

## 📈 Data Flow Example: Complete Walkthrough

### **User Input:**

```
Query: "What are the risks for automotive manufacturing in Europe right now?"
Company Profile:
  - Industry: Automotive
  - Regions: Europe
  - Suppliers: Germany, Czech Republic, Poland
  - Critical Inputs: Semiconductors, Steel
```

### **Step 1: Real-Time Fetch**

```python
# backend/data_ingestion.py: fetch_all_data()
data = {
    "news": [
        {"title": "EU Trade War Escalates Over Green Tech", "source": "Reuters", ...},
        {"title": "Port Strike Affects German Exports", "source": "BBC", ...},
        {"title": "Steel Prices Spike on Ukraine Supply Cuts", "source": "Reuters", ...},
    ],
    "weather": [
        {"city": "Rotterdam", "description": "heavy rain", "is_severe": True, ...},
        {"city": "Munich", "description": "clear", "is_severe": False, ...},
    ],
    "historical": [  # Pre-loaded
        {"event": "Russia-Ukraine War Trade Impact", "date": "2022-02-24", ...},
        {"event": "COVID-19 Pandemic", "date": "2020-03-01", ...},
    ]
}
```

### **Step 2: Embed & Store**

```python
# backend/vector_store.py: build_vector_store()
# All data converted to Documents and embedded
# Stored in ChromaDB with metadata
```

### **Step 3: Vector Retrieval**

```python
# Query: "risks for automotive manufacturing in Europe right now?"
# Similarity search returns:
docs = [
    {"type": "news", "content": "EU Trade War..."},  # Real-time match
    {"type": "news", "content": "Port Strike..."},   # Real-time match
    {"type": "historical", "content": "Russia-Ukraine War (2022): Neon gas shortage, steel prices affected..."},  # Historical
    {"type": "weather", "content": "Rotterdam: heavy rain (severe)"},  # Real-time weather
    {"type": "historical", "content": "COVID-19 (2020): Supply chain collapse, automotive particularly hard hit..."},  # Historical
    {"type": "news", "content": "Steel Prices Spike..."},  # Real-time match
]
```

### **Step 4: Context Assembly**

```
HISTORICAL & VECTOR-DB CONTEXT:
══════════════════════════════════
--- Source 1 [HISTORICAL] ---
[HISTORICAL DISRUPTION] Russia-Ukraine War Trade Impact
Date: 2022-02-24
Region: Eastern Europe
Type: geopolitical
Impact: Wheat, sunflower oil, neon gas (semiconductor manufacturing) shortages.
Affected sectors: food, energy, semiconductors, fertilizers
Severity: high
Resolution time: Ongoing (>2 years)

--- Source 2 [HISTORICAL] ---
[HISTORICAL DISRUPTION] COVID-19 Pandemic Supply Disruption
Date: 2020-03-01
Region: Global
Impact: Factory shutdowns in China, Southeast Asia. Automotive production halted.
Affected sectors: automotive, electronics, pharma
Severity: critical
Resolution time: 730 days

REAL-TIME DATA:
═══════════════
[Data fetched at: 2026-04-22]

── LIVE NEWS (3 articles) ──
  1. [Reuters] EU Trade War Escalates Over Green Tech
     Summary: EU imposing tariffs on Chinese EV batteries...

  2. [BBC] Port Strike Affects German Exports
     Summary: Strike at Hamburg and Rotterdam ports expected to last 5 days...

  3. [Reuters] Steel Prices Spike on Ukraine Supply Cuts
     Summary: Steel prices up 15% due to reduced supply from Eastern Europe...

── LIVE WEATHER (2 cities) ──
  • Rotterdam: heavy rain | 14°C | Wind: 28 km/h | ⚠ SEVERE
  • Munich: clear sky | 15°C | Wind: 12 km/h | ✓ Normal
```

### **Step 5: LLM Analysis**

```
Gemini receives:
- Unified context above
- Company profile (Automotive, Europe-focused)
- Query
- Instructions to prioritize real-time but use historical for patterns

Generates analysis:
```

### **Step 6: Output**

```json
{
  "overall_risk_level": "HIGH",
  "risk_score": 78,
  "executive_summary": "European automotive manufacturing faces multiple converging risks: immediate port disruptions (Rotterdam strike) compounded by structural steel supply constraints (Ukraine impact similar to 2022 crisis pattern) and emerging EU-China trade tensions mirroring pre-COVID supply fragmentation.",

  "identified_risks": [
    {
      "risk_id": "R001",
      "title": "Port Strike — Rotterdam & Hamburg",
      "severity": "HIGH",
      "probability": "HIGH",
      "time_horizon": "immediate",
      "evidence": "BBC report: 5-day strike affecting German exports.",
      "data_source": "realtime"
    },
    {
      "risk_id": "R002",
      "title": "Steel Supply Shortage (Ukraine Analog)",
      "severity": "HIGH",
      "probability": "HIGH",
      "time_horizon": "medium_term",
      "evidence": "Reuters: 15% price spike. Historical precedent: Russia-Ukraine war (2022) caused 18-month disruption. Similar pattern emerging.",
      "data_source": "both"
    },
    {
      "risk_id": "R003",
      "title": "EU-China Trade War Escalation",
      "severity": "MEDIUM",
      "probability": "MEDIUM",
      "time_horizon": "medium_term",
      "evidence": "EU tariffs on EV batteries. Historical precedent: Pre-COVID 2019 had 15-18% average lead time increases during trade war.",
      "data_source": "realtime"
    },
    {
      "risk_id": "R004",
      "title": "Severe Weather — Port Operations",
      "severity": "MEDIUM",
      "probability": "HIGH",
      "time_horizon": "short_term",
      "evidence": "Heavy rain & high winds in Rotterdam. Expected impact: 1-3 day delays.",
      "data_source": "realtime"
    }
  ],

  "mitigation_strategies": [
    {
      "risk_id": "R002",
      "strategy": "Source Steel from Alternative Regions",
      "actions": [
        "Increase German/Polish domestic sourcing (reduce reliance on Eastern Europe)",
        "Establish 6-month forward contracts at current prices",
        "Note: COVID-19 crisis (2020): companies that locked in contracts 2 months early avoided worst shortages"
      ],
      "timeline": "1-2 months",
      "cost_estimate": "medium"
    }
  ],

  "early_warning_indicators": [
    "Steel price trend: if continues rising 5% weekly, indicates structural shortage (2022 baseline)",
    "Port recovery timeline: track Rotterdam strike resolution (precedent: average EU port strike lasts 5-7 days)",
    "EV battery tariff changes: any increase above 20% signals escalation (pre-COVID baseline: 0-5%)"
  ]
}
```

---

## 🎯 Key Insights: Why This Works

| Aspect                      | Benefit                       | Example                                                                                      |
| --------------------------- | ----------------------------- | -------------------------------------------------------------------------------------------- |
| **Pattern Matching**        | Identify recurring events     | "Current steel shortage mirrors 2022 Ukraine crisis"                                         |
| **Severity Calibration**    | Avoid under/over-estimating   | "Port strike typically lasts 5-7 days (historical data)"                                     |
| **Recovery Prediction**     | Estimate disruption duration  | "2021 Taiwan shortage: 18 months. Current situation: similar factors → 12-15 months"         |
| **Cascade Modeling**        | Understand multi-tier impacts | "Direct port impact (1-3 days) → supplier delays (7-10 days) → production impact (30+ days)" |
| **Geopolitical Context**    | Understand structural risks   | "EU-China tensions: pre-COVID escalation saw 15-18% lead time increases"                     |
| **Regional Prioritization** | Focus mitigation efforts      | "Rotterdam historically most impacted port; Munich least vulnerable"                         |

---

## 🚀 Conclusion

Your RAG system creates a **multi-layered intelligence framework**:

1. **Real-time Layer** - Current threats (news, weather)
2. **Historical Layer** - Contextual patterns (past disruptions)
3. **Integration Layer** - Unified analysis (LLM synthesis)
4. **Output Layer** - Actionable intelligence (structured risk assessment)

When a user submits a new prompt:

- ✅ **Real-time data** answers "what's happening NOW?"
- ✅ **Historical data** answers "how bad could this be?" and "how long will it last?"
- ✅ **Combined analysis** answers "what should we do about it?"

This approach transforms raw incident data into **strategic foresight** for supply chain decision-making.
