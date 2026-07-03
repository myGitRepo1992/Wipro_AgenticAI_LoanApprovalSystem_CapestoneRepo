# Agentic AI Loan Approval System - Architecture Reference

## System Overview

```
┌────────────────────────────────────────────────────────────────────────┐
│                                                                        │
│                       PRESENTATION LAYER                               │
│                    Streamlit Chatbot UI (8501)                         │
│                                                                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐       │
│  │ New Application │  │ Status Lookup   │  │ Analytics       │       │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘       │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ HTTP/JSON
                                  ▼
┌────────────────────────────────────────────────────────────────────────┐
│                                                                        │
│                    MICROSERVICE LAYER                                  │
│                  FastAPI REST Server (8000)                            │
│                                                                        │
│  POST /submit_application                                             │
│  GET  /application_status/{id}                                        │
│  GET  /applications                                                   │
│  GET  /health                                                         │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ Python Objects
                                  ▼
┌────────────────────────────────────────────────────────────────────────┐
│                                                                        │
│                   ORCHESTRATION LAYER                                  │
│              LangGraph Workflow Engine (In-Process)                    │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │  Validate Node                                               │    │
│  │  ├─ Schema Validation                                        │    │
│  │  ├─ Data Type Checking                                       │    │
│  │  └─ Range Validation                                         │    │
│  └──────────────────────────────────────────────────────────────┘    │
│                            │                                          │
│                 ┌──────────┴──────────┐                               │
│                 ▼                     ▼ (Parallel)                    │
│  ┌──────────────────────────┐ ┌──────────────────────────┐           │
│  │ Applicant Profile Node   │ │ Financial Risk Node      │           │
│  │ ├─ Income Stability      │ │ ├─ DTI Calculation      │           │
│  │ ├─ Employment Risk       │ │ ├─ Credit Risk          │           │
│  │ ├─ Credit Summary        │ │ ├─ Loan Risk            │           │
│  │ └─ Completeness Flags    │ │ └─ Anomaly Detection    │           │
│  └──────────────────────────┘ └──────────────────────────┘           │
│                 │                     │                               │
│                 └──────────┬──────────┘                               │
│                            ▼                                          │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │ Decision Node                                                │    │
│  │ ├─ Risk Score Calculation (Weighted)                        │    │
│  │ ├─ Decision Logic (Approve/Reject/Review)                   │    │
│  │ ├─ Confidence Level Calculation                             │    │
│  │ └─ Key Factors Identification                               │    │
│  └──────────────────────────────────────────────────────────────┘    │
│                            │                                          │
│                            ▼                                          │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │ Compliance Node                                              │    │
│  │ ├─ Case ID Generation                                        │    │
│  │ ├─ Action Determination                                      │    │
│  │ ├─ Notification Sending                                      │    │
│  │ └─ Audit Trail Creation                                      │    │
│  └──────────────────────────────────────────────────────────────┘    │
│                            │                                          │
└────────────────────────────┼────────────────────────────────────────┘
                             │
                             │ (Agents delegate to MCP Servers)
                             │
       ┌─────────────────────┼─────────────────────┐
       │                     │                     │
       ▼                     ▼                     ▼
┌─────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ ApplicantDB     │ │ RiskRulesDB      │ │ DecisionSynthesis│
│ MCP Server      │ │ MCP Server       │ │ MCP Server       │
│ (Port 8001)     │ │ (Port 8002)      │ │ (Port 8003)      │
└─────────────────┘ └──────────────────┘ └──────────────────┘
        │                   │                     │
┌───────┴───────────────────┴─────────────────────┴─────────┐
│                                                           │
│  ┌────────────────────────────────────────────────────┐  │
│  │ NotificationSystem MCP Server (Port 8004)         │  │
│  │ ├─ Notification Management                        │  │
│  │ ├─ Logging & Audit Trail                          │  │
│  │ └─ Case Tracking                                  │  │
│  └────────────────────────────────────────────────────┘  │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

## Data Flow Sequence

```
1. USER INPUT
   └─→ Streamlit UI collects loan application form

2. API SUBMISSION
   └─→ HTTP POST to /submit_application (FastAPI)

3. VALIDATION
   └─→ Pydantic schema validation
   └─→ Range checking on all numeric fields

4. LANGGRAPH ORCHESTRATION
   ├─→ State initialized as LoanProcessingState
   ├─→ Validate node executes
   ├─→ Parallel node execution:
   │   ├─→ Applicant Profile Agent (independent)
   │   └─→ Financial Risk Agent (independent)
   ├─→ Results merged in DAG
   ├─→ Decision node synthesizes
   └─→ Compliance node finalizes

5. RESPONSE AGGREGATION
   └─→ All agent outputs combined
   └─→ LoanApplicationResponse created

6. CLIENT RESPONSE
   ├─→ JSON response to API caller
   └─→ Streamlit displays formatted results
```

## State Management

### LoanProcessingState (TypedDict)

```python
{
    "application_id": str,           # Unique ID
    "application": LoanApplication,  # Input data
    "applicant_profile": ApplicantProfileOutput,      # Agent output
    "financial_risk": FinancialRiskOutput,           # Agent output
    "loan_decision": LoanDecisionOutput,             # Agent output
    "compliance_action": ComplianceActionOutput,     # Agent output
    "error": str                     # Error accumulation
}
```

### State Flow Through Nodes

```
validate() 
  ├─ Input: Full LoanProcessingState
  ├─ Checks: Schema + data ranges
  └─ Output: Updated state or error

applicant_profile_node()
  ├─ Input: application field
  ├─ Computation: Profile analysis
  └─ Output: applicant_profile field populated

financial_risk_node()
  ├─ Input: application field
  ├─ Computation: Risk analysis
  └─ Output: financial_risk field populated

decision_node()
  ├─ Input: applicant_profile + financial_risk
  ├─ Computation: Score + classification
  └─ Output: loan_decision field populated

compliance_node()
  ├─ Input: application + loan_decision
  ├─ Computation: Action + notification
  └─ Output: compliance_action field populated
```

## Agent Communication Patterns

### Request/Response Pattern

```
Agent Node
├─ Receives state from LangGraph
├─ Extracts relevant data
├─ Calls agent function
├─ Updates state field
└─ Returns updated state

Example (Applicant Profile):
  input_data = state["application"]
  result = analyze_applicant_profile(input_data)
  state["applicant_profile"] = result
  return state
```

### MCP Server Communication (Future)

```
Agent Node
├─ Constructs MCP request
├─ POSTs to MCP server endpoint
├─ Receives JSON response
├─ Parses response
├─ Updates state with result
└─ Returns updated state
```

## Risk Scoring Calculation

### Formula Breakdown

```
Total Risk Score (0-100) = Sum of weighted factors

1. Income Stability Factor (25%)
   ├─ Base Score: 50
   ├─ Tenure Bonus: Years * 5 (max 30)
   ├─ Status Bonus: 5-20 based on employment type
   ├─ Income Bonus: 5-10 based on income level
   └─ Result: 100 - this_score

2. Employment Risk Factor (20%)
   ├─ Maps: employed→10, self-employed→30, etc.
   └─ Weight: 0.20

3. Credit Score Risk Factor (25%)
   ├─ Maps: 750+→5, 700-749→20, etc.
   └─ Weight: 0.25

4. Loan Amount Risk Factor (15%)
   ├─ Ratio: Loan Amount / Annual Income
   ├─ Maps: ≤50%→10, 50-75%→25, etc.
   └─ Weight: 0.15

5. Anomaly Penalty (5%)
   ├─ Count: Number of detected anomalies
   ├─ Penalty: count * 5 points
   └─ Direct addition (no weight)

6. DTI Factor (10%)
   ├─ Formula: (DTI / 43) * 15
   ├─ Capped at 15
   └─ Direct addition (no weight)

Final: Min(total, 100.0)
```

### Decision Thresholds

```
Risk Score | Completeness   | Decision  | Confidence | Action
-----------+----------------+-----------+------------+------------------
< 30       | 0 flags        | Approved  | 0.95       | Send approval letter
< 50       | 0-1 flags      | Approved  | 0.85       | Send approval letter
< 60       | 0 flags        | Review    | 0.70       | Queue for review
< 70       | ≤1 anomalies   | Review    | 0.60       | Queue for review
≥ 75       | Any            | Rejected  | 0.90       | Send rejection letter
Others     | -              | Review    | 0.65       | Queue for review
```

## Technology Stack Mapping

| Layer | Technology | Purpose | Version |
|-------|-----------|---------|---------|
| Presentation | Streamlit | Real-time chat UI | 1.28.1 |
| API | FastAPI | REST endpoints | 0.104.1 |
| Server | Uvicorn | ASGI server | 0.24.0 |
| Orchestration | LangGraph | Workflow DAG | 0.0.45 |
| LLM Framework | LangChain | LLM integration | 0.1.1 |
| LLM Model | Anthropic Claude | AI decision making | Sonnet 4 |
| SDK | Anthropic SDK | API client | 0.7.8 |
| MCP Servers | FastMCP | Agent communication | 0.5.0 |
| Validation | Pydantic | Type safety | 2.5.0 |
| Config | python-dotenv | Environment vars | 1.0.0 |
| HTTP | httpx | Async HTTP | 0.25.2 |
| Runtime | Python | Execution | 3.x |

## Scalability Architecture (Future)

### Horizontal Scaling

```
Load Balancer (Port 80/443)
    ├─→ API Instance 1 (FastAPI)
    ├─→ API Instance 2 (FastAPI)
    └─→ API Instance N (FastAPI)
         │
         ├─→ Agent Pool (Stateless, auto-scaling)
         │   ├─ Applicant Profile Agents (Replicated)
         │   ├─ Financial Risk Agents (Replicated)
         │   ├─ Decision Agents (Replicated)
         │   └─ Compliance Agents (Replicated)
         │
         ├─→ MCP Server Pool (Stateless, replicated)
         │   ├─ ApplicantDB Replicas (Cached)
         │   ├─ RiskRulesDB Replicas (Cached)
         │   ├─ DecisionSynthesis Replicas (Cached)
         │   └─ NotificationSystem (Queue-backed)
         │
         └─→ Data Layer
             ├─ PostgreSQL (Application Storage)
             ├─ Redis (Caching)
             ├─ RabbitMQ (Notifications)
             └─ S3 (Audit Logs)
```

### Performance Characteristics

| Metric | Single Instance | Multi-Instance |
|--------|-----------------|-----------------|
| Throughput | 600-1000 apps/hour | 10k+ apps/hour |
| P50 Latency | 2-3 seconds | 1-2 seconds |
| P95 Latency | 4-5 seconds | 2-3 seconds |
| P99 Latency | 6-8 seconds | 3-4 seconds |
| Memory/Instance | 200-300MB | 200-300MB |
| CPU/Instance | 1-2 cores | 1-2 cores |

## Error Handling Strategy

```
Error Detection Level
├─ Input Validation (Pydantic)
│  └─ HTTPException 422 (Unprocessable Entity)
├─ Agent Execution (Try-Catch)
│  ├─ State error accumulation
│  └─ HTTPException 500 (Internal Server Error)
├─ MCP Server Communication
│  ├─ Retry logic (3 attempts)
│  └─ Fallback values
└─ Business Logic
   └─ Review classification for edge cases
```

## Security Measures

```
Data Security
├─ Pydantic validation (no injection)
├─ Type hints (prevent type confusion)
└─ No dynamic eval/exec

API Security
├─ CORS configured
├─ Error messages sanitized
└─ No stack traces exposed

Credential Security
├─ API keys in environment
├─ No hardcoded secrets
└─ .env in .gitignore

Audit Trail
├─ Case IDs generated
├─ Timestamps recorded
├─ All decisions logged
└─ No sensitive data in logs
```

## Testing Strategy

```
Unit Testing
├─ Agent functions (isolated)
├─ Calculation correctness
└─ Edge case handling

Integration Testing
├─ Full workflow execution
├─ State management
├─ Error propagation

E2E Testing
├─ API endpoints
├─ UI interactions
└─ Database operations

Performance Testing
├─ Throughput measurement
├─ Latency profiling
└─ Memory usage monitoring
```

---

**Architecture Version:** 1.0  
**Last Updated:** 2026-07-01  
**For Evaluation:** See CLAUDE.md for design decisions and trade-offs
