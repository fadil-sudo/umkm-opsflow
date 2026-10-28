# UMKM OpsFlow — Workflow Diagram (Mermaid)

```mermaid
graph TD
    A[User provides CSV/XLSX file] --> B[WorkBuddy Agent receives file]
    B --> C[1. INGEST: parse_file.py reads CSV/XLSX]
    C --> D{File parseable?}
    D -- No --> E[Error: report parse failure]
    D -- Yes --> F[2. PARSE: normalize columns to standard schema]
    F --> G{Records found?}
    G -- No --> H[Error: no valid records]
    G -- Yes --> I[3. VALIDATE: check data quality]
    I --> J[Flag: missing fields, duplicates, outliers, negatives]
    I --> K[Flag: date range, payment method anomalies]
    J --> L{Any ERROR severity?}
    L -- All errors --> M[Error: all records failed]
    L -- Some valid --> N[3b. CLARIFY: detect ambiguities]
    N --> N1[Mixed payment status? Similar products? Holiday?]
    N1 --> N2[Ask user for clarification]
    N2 --> O[4. COMPUTE: deterministic Python]
    O --> P[Expenses = sum of expense totals]
    O --> Q[Net = Revenue - Expenses]
    O --> R[Top products, payment breakdown]
    P --> S[5. GENERATE REPORT: Markdown]
    Q --> S
    R --> S
    S --> T[6. ACTIONS: rule-based triggers]
    T --> U[Unpaid orders → follow up]
    T --> V[Low stock → reorder]
    T --> W[Outliers → verify]
    T --> X[Duplicates → review]
    U --> Y[7. DRAFT MESSAGES: LLM formats]
    V --> Y
    W --> Y
    X --> Y
    Y --> Z[8. HUMAN APPROVAL GATE]
    Z --> AA{User approves?}
    AA -- No --> AB[Discard drafts]
    AA -- Yes --> AC[9. DELIVER: save to output/]
    AC --> AD[daily_report.md + clarification_log]
    AC --> AE[draft_messages.md]
    AC --> AF[action_items.csv]
    AC --> AG[validation_issues.csv]
    AC --> AH[metrics.json]
    
    style Z fill:#ff9800,color:#000
    style N1 fill:#ffeb3b,color:#000
    style N fill:#4caf50,color:#fff
    style S fill:#2196f3,color:#fff
```

## Layer Separation

```mermaid
graph LR
    subgraph LLM Layer [LLM Layer - WorkBuddy Agent]
        L1[Understand user intent]
        L2[Format report text]
        L3[Draft follow-up messages]
        L4[Explain results]
    end
    
    subgraph Python Layer [Deterministic Layer - Python Scripts]
        P1[Parse input file]
        P2[Validate records]
        P3[Compute all metrics]
        P4[Generate action items]
        P5[Export to files]
    end
    
    subgraph File System [File System - Local Only]
        F1[Read: data/*.csv]
        F2[Write: output/*.md]
        F3[Write: output/*.csv]
        F4[Write: output/*.json]
    end
    
    LLM Layer -->|pre-computed data| Python Layer
    Python Layer -->|structured results| LLM Layer
    Python Layer -->|read/write| File System
    
    style LLM Layer fill:#e3f2fd
    style Python Layer fill:#e8f5e9
    style File System fill:#fff3e0
```

## Data Flow with Audit Trail

```mermaid
sequenceDiagram
    participant U as User
    participant A as WorkBuddy Agent
    participant P as Python Pipeline
    participant F as File System
    
    U->>A: "Here's my sales data" + file path
    A->>P: Run opsflow.py --input <file>
    P->>F: Read CSV/XLSX
    F-->>P: Raw rows
    
    P->>P: Parse → normalize columns
    P->>P: Validate → flag issues
    P->>P: Compute → metrics (deterministic)
    P->>P: Generate → action items (rules)
    P->>P: Export → format report
    
    P->>F: Write daily_report.md
    P->>F: Write draft_messages.md
    P->>F: Write action_items.csv
    P->>F: Write validation_issues.csv
    P->>F: Write metrics.json
    
    P-->>A: JSON result with metrics + issues + actions
    A-->>U: "Report ready. 14 transactions processed. 4 issues found. 4 actions proposed."
    
    U->>A: "Show me the unpaid orders"
    A->>U: Shows report section + draft messages
    
    U->>A: "OK, prepare the follow-up messages"
    A->>U: Shows draft_messages.md content
    
    U->>U: Copies messages, sends manually via WhatsApp
```
