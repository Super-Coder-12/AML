# 🧠 AI Anti-Money Laundering Agent – Decision Flow Prompts

This prompt chain simulates how an intelligent AML agent evaluates a transaction and determines its risk level, using multi-step logical reasoning, pattern matching, and identity-aware access control.

---

## Prompt 1: Transaction Input

**User Input:**
Amount: $48,000

Origin: Cayman Islands

Receiving Account: Company registered 2 months ago

Customer ID: CUST_09423

Transaction Type: Wire Transfer

---

## Prompt 2: Amount Check

**Agent Prompt:**
> Is the amount greater than $10,000?

-  Yes → Proceed to risk country check  
-  No → Flag as Low Risk (no escalation)

---

## Prompt 3: Country Risk Check

**Agent Prompt:**
> Is "Cayman Islands" considered a high-risk jurisdiction?

- Yes → Increase risk weight  
- No → Decrease risk weight

---

## Prompt 4: Beneficiary Trustworthiness

**Agent Prompt:**
> Receiving company was registered only 2 months ago.  
> Is this beneficiary considered unverified?

- Yes → Add to risk score  
- No → Proceed with moderate risk level

---

## Prompt 5: Transaction Pattern Detection

**Agent Prompt:**
> This customer has made 4 large transactions across 3 continents in 30 days.  
> Matches typology: "Smurfing + Layering"

-  Confirm suspicious pattern → Increase risk score  
-  Unusual, but no match → Monitor only

---

## Prompt 6: Final Risk Assessment

**Agent Summary:**

Risk Score: 0.87 (High)
Criteria Triggered:
 • Amount > $10,000
 • Offshore origin
 • Unverified beneficiary
 • Pattern matched: Smurfing

 **Agent Prompt:**
> Generate alert and escalate?

- Yes → `Alert ID: AML_2025_0401_002`  
- No → Log internally only

---

## Prompt 7: Access Control Simulation

**Agent Prompt:**
> Current user role: `Junior Analyst`  
> View full alert trace?

- No → Partial Access (summary only)  
- Compliance Officer → Full Access Granted

---
