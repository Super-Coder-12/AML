# 🧠 AML Smart Agent System

This project implements an intelligent anti-money laundering (AML) agent that monitors financial transactions using a behavior tree. The system balances autonomy with control through identity governance, policy enforcement, and hybrid storage design.

---

## A. System Use Case and Rationale

**Use Case:**  
Detect and respond to suspicious transactions based on user risk score, PEP status, transaction amount, country, and activity frequency.

**Why Agentic Design:**  
This system simulates a rational agent making policy-bounded decisions in real-time or batch workflows. It mimics modern compliance systems which must act autonomously while being auditable and override-capable by humans.

---

## B. Governance Rules Used

| Rule Name             | Description                                              |
|----------------------|----------------------------------------------------------|
| `HighRisk+Foreign`   | If risk_score > 0.85 and country ≠ US → Block transaction |
| `PEP+LargeTX`        | If user is PEP and amount > 10,000 → Flag for review     |
| `HighFreqTX`         | If user makes ≥ 5 transactions recently → Block (simulated Redis) |
| `Reviewer Override`  | If role = reviewer → Override system decision             |

**Access Control:**
- **PBAC**: Reviewer can override decisions.
- **ABAC**: Decisions influenced by user attributes (e.g., `risk_score`, `is_pep`, `transaction_country`).

---

## C. Architectural Tradeoffs and Constraints

| Dimension            | Tradeoff Description |
|----------------------|----------------------|
| **Autonomy vs Control** | The agent acts independently but can be overridden by role-based access (PBAC). |
| **Speed vs Consistency** | In-memory cache (dict) enables fast frequency checks, trading off persistence. |
| **Batch vs Stream** | System simulates batch via list processing; can extend to real-time stream. |
| **SQL vs NoSQL** | Structured data (SQL-style schema) is combined with simulated NoSQL-style cache (Python dict) for recent transactions. |

---

## 🧩 Agent Architecture

The decision logic is implemented via a **behavior tree** (using `py_trees`), enabling modular and explainable rules. The agent's actions and triggers are fully logged for traceability.

> Example output log: `logs/decision_log.json`  
> Behavior tree image: `behavior_tree.png`

---

## ✅ Deliverables

- `main.py`: Main agent executor
- `decision_logic.py`: Behavior tree logic
- `logs/decision_log.json`: Sample governance logs
- `batch_job.py` (optional): Batch processing module
- `README.md`: This file
