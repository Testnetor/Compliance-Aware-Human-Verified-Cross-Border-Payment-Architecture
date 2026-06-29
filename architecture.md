# System Architecture

## Overview

This document describes the architecture of the **Compliance-Aware Human-Verified Cross-Border Payment Architecture** project.

The system is designed as a research and prototype-level financial technology architecture that compares traditional SWIFT-based international transfers with blockchain-based stablecoin settlement. It also adds security, compliance, auditability, and scalability layers to demonstrate how a real-world payment system should be designed beyond simple cost and speed comparison.

The architecture focuses on four main goals:

1. Compare payment efficiency between SWIFT and stablecoin settlement.
2. Require proof-of-human verification before each transfer request.
3. Apply compliance and risk-scoring checks before settlement.
4. Store audit logs for transparency, traceability, and review.

---

## High-Level Architecture

```text
User Interface
   ↓
Wallet / Account Connection
   ↓
Human Verification Layer
   ↓
Transfer Request API
   ↓
Compliance Engine
   ├── KYC/KYB status check
   ├── Sanctions-screening logic
   ├── Country corridor risk check
   ├── Transaction amount risk check
   └── Suspicious activity rules
   ↓
Risk Scoring Engine
   ↓
Settlement Router
   ├── Traditional SWIFT simulation
   └── Stablecoin settlement simulation
   ↓
Audit Log System
   ↓
Analytics / Reporting Dashboard
```

---

## Main Components

## 1. User Interface

The user interface allows a user to create a simulated cross-border payment request.

The user provides:

* Sender information
* Recipient information
* Transfer amount
* Destination country
* Preferred settlement route
* Wallet or account identifier

The interface displays:

* Estimated fee
* Estimated settlement time
* Human verification status
* Compliance decision
* Risk score
* Final transfer decision

---

## 2. Wallet / Account Connection

Before creating a transfer request, the user connects a wallet or account.

In the prototype version, this can be simulated using a mock wallet address.

Example:

```json
{
  "wallet": "0x1234567890abcdef",
  "userId": "USER-001"
}
```

In a future version, this layer may be connected to a real EVM-compatible wallet such as MetaMask.

---

## 3. Human Verification Layer

The human verification layer checks whether the user has passed proof-of-human verification before initiating a transfer.

This layer is inspired by Humanode-style human verification and Sybil-resistance concepts.

The purpose of this layer is to reduce:

* Bot-driven transfer attempts
* Fake account abuse
* Sybil attacks
* Repeated fraudulent account creation
* Automated spam transactions

Example verification response:

```json
{
  "wallet": "0x1234567890abcdef",
  "humanVerified": true,
  "verificationProvider": "Humanode-inspired mock verification"
}
```

If the user is not human-verified, the transfer request is blocked before reaching the compliance engine.

Example decision:

```json
{
  "decision": "Rejected",
  "reason": "Human verification required before transfer"
}
```

Important note: human verification is not the same as KYC or AML. It confirms human uniqueness or human presence, while KYC/AML focuses on legal identity, sanctions, source of funds, and regulatory requirements.

---

## 4. Transfer Request API

The transfer request API receives the user’s payment request after the human verification check.

Example transfer request:

```json
{
  "transactionId": "TX-001",
  "senderWallet": "0x1234567890abcdef",
  "recipientWallet": "0xabcdef1234567890",
  "amount": 1000,
  "currency": "USD",
  "destinationCountry": "Italy",
  "route": "stablecoin"
}
```

The API then forwards this request to the compliance engine.

---

## 5. Compliance Engine

The compliance engine evaluates whether the transaction should be approved, rejected, or sent for manual review.

The prototype compliance engine may include the following checks:

### KYC/KYB Status Check

Checks whether the sender and recipient have completed mock KYC or KYB verification.

Possible statuses:

```text
Verified
Pending
Rejected
Missing
```

### Sanctions Screening

Checks whether the sender, recipient, or wallet address appears on a mock sanctions list.

Possible result:

```json
{
  "sanctionsMatch": false,
  "screeningStatus": "Passed"
}
```

### Country Corridor Risk

Evaluates risk based on the transfer corridor.

Example:

```text
Turkey → Italy: Low risk
Unknown country → High-risk jurisdiction: High risk
```

### Transaction Amount Risk

Higher transaction amounts may increase compliance risk.

Example rules:

```text
Amount below $1,000: Low amount risk
Amount between $1,000 and $10,000: Medium amount risk
Amount above $10,000: High amount risk
```

### Suspicious Activity Rules

The system may flag suspicious behavior such as:

* Too many transfers in a short time
* Repeated transfers to the same recipient
* Transfers just below a reporting threshold
* Unverified user activity
* High-risk country corridor

---

## 6. Risk Scoring Engine

The risk scoring engine converts compliance signals into a numeric score.

Example scale:

```text
0–30: Low risk
31–70: Medium risk
71–100: High risk
```

Example scoring logic:

```text
Base score: 0

+30 if KYC is missing
+40 if sanctions match is found
+15 if transfer amount is high
+10 if destination corridor is medium risk
+25 if destination corridor is high risk
+20 if transaction frequency is suspicious
-10 if user is human-verified
```

Example output:

```json
{
  "transactionId": "TX-001",
  "riskScore": 22,
  "riskLevel": "Low",
  "decision": "Approved"
}
```

Decision rules:

```text
Low risk: Approved
Medium risk: Manual review
High risk: Rejected
```

---

## 7. Settlement Router

The settlement router selects the settlement route and calculates estimated fee and settlement time.

The project compares two routes:

### Traditional SWIFT-Based Route

```text
Estimated settlement time: 72 hours
Estimated fee ratio: 4.5%
```

Example calculation:

```text
Amount: $1,000
Fee: $1,000 × 4.5% = $45
Estimated received amount: $955
```

### Stablecoin-Based Route

```text
Estimated settlement time: 0.5 hours
Estimated fee ratio: 0.045%
```

Example calculation:

```text
Amount: $1,000
Fee: $1,000 × 0.045% = $0.45
Estimated received amount: $999.55
```

The stablecoin route is simulated for educational purposes and does not execute real transactions.

---

## 8. Audit Log System

The audit log system records every important decision and system event.

Audit logs are important because financial systems must be traceable, reviewable, and transparent.

The audit log may store:

* Transaction ID
* Sender wallet
* Recipient wallet
* Amount
* Currency
* Route
* Human verification result
* KYC/KYB status
* Sanctions-screening result
* Risk score
* Compliance decision
* Fee estimate
* Settlement time estimate
* Timestamp
* Simulated transaction hash

Example audit log:

```json
{
  "transactionId": "TX-001",
  "senderWallet": "0x1234567890abcdef",
  "recipientWallet": "0xabcdef1234567890",
  "amount": 1000,
  "currency": "USD",
  "route": "stablecoin",
  "humanVerified": true,
  "kycStatus": "Verified",
  "sanctionsScreening": "Passed",
  "riskScore": 22,
  "decision": "Approved",
  "estimatedFee": 0.45,
  "estimatedSettlementTimeHours": 0.5,
  "timestamp": "2026-01-01T12:00:00Z",
  "simulatedTransactionHash": "0xmocktransactionhash"
}
```

---

## Transfer Decision Flow

```text
Start transfer request
   ↓
Check human verification
   ↓
Is user human-verified?
   ├── No → Reject transfer
   └── Yes → Continue
           ↓
      Run compliance checks
           ↓
      Calculate risk score
           ↓
      Determine risk level
           ↓
      Is risk low?
           ├── Yes → Approve transfer
           ├── Medium → Manual review
           └── High → Reject transfer
           ↓
      Calculate fee and settlement time
           ↓
      Save audit log
           ↓
      Return result to user
```

---

## Example End-to-End Scenario

A user wants to send **$1,000** internationally.

### Input

```json
{
  "amount": 1000,
  "route": "stablecoin",
  "senderCountry": "Turkey",
  "destinationCountry": "Italy",
  "senderWallet": "0x1234567890abcdef",
  "recipientWallet": "0xabcdef1234567890"
}
```

### System Checks

```text
Human verification: Passed
KYC status: Verified
Sanctions screening: Passed
Country corridor risk: Low
Transaction amount risk: Medium
Suspicious activity: Not detected
```

### Output

```json
{
  "transactionId": "TX-001",
  "route": "stablecoin",
  "amount": 1000,
  "estimatedFee": 0.45,
  "estimatedSettlementTimeHours": 0.5,
  "riskScore": 22,
  "riskLevel": "Low",
  "decision": "Approved"
}
```

---

## Scalability Design

A real payment system must process many transfer requests at the same time. For this reason, the architecture can be extended using queues and workers.

### Basic Scalable Architecture

```text
Incoming Transfer Requests
   ↓
API Gateway
   ↓
Message Queue
   ↓
Compliance Workers
   ↓
Risk Scoring Workers
   ↓
Settlement Workers
   ↓
Database / Audit Log
   ↓
Analytics Dashboard
```

### Why Use a Queue?

A queue helps the system handle traffic spikes and prevents the API from becoming overloaded.

Benefits:

* More stable performance
* Better control of transaction processing
* Easier horizontal scaling
* Retry support for failed tasks
* Separation between request handling and settlement processing

### Example Worker Flow

```text
Worker 1: Human verification checks
Worker 2: Compliance checks
Worker 3: Risk scoring
Worker 4: Settlement simulation
Worker 5: Audit logging
```

---

## Scalability Metrics

The project can measure the following metrics during testing:

| Metric                     | Meaning                                         |
| -------------------------- | ----------------------------------------------- |
| Average latency            | Average time to process a transfer              |
| p95 latency                | Time below which 95% of transfers are processed |
| Throughput                 | Number of transfers processed per second        |
| Error rate                 | Percentage of failed transfer requests          |
| Queue delay                | Time spent waiting in queue                     |
| Compliance-processing time | Time spent on compliance checks                 |
| Settlement-processing time | Time spent on settlement simulation             |

---

## Security Considerations

The architecture includes several security-focused design choices:

* Human verification before transfer initiation
* Risk scoring before settlement
* Sanctions-screening logic
* Audit logging
* Manual review for medium-risk transactions
* Rejection of high-risk transactions
* Separation of verification, compliance, and settlement modules

The system is designed to reduce the risk of:

* Bot abuse
* Fake accounts
* Sybil attacks
* Suspicious transfers
* Unauthorized settlement attempts
* Missing compliance records

---

## Limitations

This is an educational prototype and not a production payment system.

Current limitations:

* Human verification is initially mocked
* No real stablecoin transfer is executed
* No real KYC provider is integrated
* No real sanctions database is used
* No real banking or SWIFT API is connected
* Regulatory logic is simplified
* Risk scoring is rule-based rather than machine-learning based

These limitations are intentional for the prototype stage. The purpose is to demonstrate system architecture, engineering thinking, and awareness of real-world financial technology constraints.

---

## Future Improvements

Possible future improvements include:

* Real Humanode or Biomapper integration
* EVM wallet connection
* Smart contract-based verification gate
* Real blockchain testnet simulation
* PostgreSQL database integration
* REST API implementation using FastAPI
* Dashboard using React or Next.js
* Advanced risk scoring
* Realistic transaction dataset
* Load testing using Locust
* Queue-based processing using Redis, RabbitMQ, or Kafka
* Manual review dashboard
* Exportable audit reports

---

## Summary

This architecture shows how a cross-border payment system can be designed with more than cost and speed in mind.

The project combines:

* Payment efficiency analysis
* Blockchain settlement modeling
* Human verification
* Compliance engineering
* Risk scoring
* Audit logging
* Scalability planning

The key engineering idea is that a faster payment system is only valuable if it is also secure, compliant, auditable, and scalable.
