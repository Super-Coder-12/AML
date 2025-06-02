# AML Smart Agent System

## 🧠 Use Case Overview
This project implements an autonomous Anti-Money Laundering (AML) agent that monitors real-time and batch financial transactions. The agent identifies suspicious activities (e.g., large foreign transfers, rapid small transactions) and enforces policy actions like flagging or blocking transactions. This design simulates a real-world AML compliance system under architectural and governance principles.

## 🎯 Agent Goal & Action Space
The agent:
- Monitors user transactions (real-time and batch)
- Evaluates transactions against ABAC/PBAC-based rules
- Flags high-risk activities
- Blocks transactions if policy thresholds are exceeded
- Logs all decisions for traceability

## 🗄️ Data Layers
- **SQL Database (PostgreSQL)**: Stores user info, past transaction history, user risk scores.
- **NoSQL (Redis)**: Caches recent transactions for frequency analysis and performance.
- **Stream**: Handles real-time ingestion of new transactions.
- **Batch**: Periodic review of all transactions for nightly audits.

## 🔐 Identity & Access Governance
- **PBAC**: Distinguishes between end-users and AML reviewers.
- **ABAC**: Attributes like `location`, `risk_score`, `is_pep`, and `account_age` influence decisions.

## 🔎 Policy Enforcement Examples
- `IF risk_score > 0.85 AND transaction_country != "US" THEN block_transaction`
- `IF is_pep == True AND amount > 10,000 THEN flag_for_review`

## ⚖️ Architectural Tradeoffs
| Tradeoff | Decision |
|---------|----------|
| Consistency vs Speed | Redis caching may result in eventual consistency, favoring speed |
| Observability vs Autonomy | All agent actions are logged and auditable |
| Batch vs Stream | Batch is used for full audit sweeps, stream ensures real-time response |

## 📜 Observability & Rationality
- Every agent decision is logged with user ID, transaction ID, reason, and timestamp
- System rules are transparent and modular for auditing
