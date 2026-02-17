# DOT Sentinel AI 🚨  
### Agentic AI–Driven Network Intrusion Detection System

DOT Sentinel AI is a capstone project focused on detecting anomalous network behavior from PCAP traffic and translating low-level alerts into **human-readable, actionable cybersecurity intelligence** using Agentic AI and the MITRE ATT&CK framework.

---

## 📌 Project Overview

Traditional IDS tools generate alerts that are difficult for non-experts to interpret.  
DOT Sentinel AI bridges this gap by:

- Parsing raw **PCAP network traffic**
- Extracting **flow-level statistical features**
- Detecting anomalies using **unsupervised machine learning**
- Explaining threats using **Agentic AI**
- Mapping alerts to **MITRE ATT&CK tactics and techniques**
- Displaying insights on an interactive dashboard


---

## 🧰 Technology Stack

### 🔹 Data Ingestion & Parsing
- **PCAP** – Industry-standard network traffic format  
- **Tshark** – CLI-based automated packet parsing  
- **Wireshark** – Traffic validation and analysis  

---

### 🔹 Feature Engineering & Machine Learning
- **Python**
- **Pandas / NumPy**
- **Scikit-learn**
- **Isolation Forest** (Unsupervised Anomaly Detection)

**Why Isolation Forest?**
- No labeled data required  
- Effective for unknown/zero-day attacks  
- Lightweight and explainable  

---

### 🔹 Backend
- **FastAPI** – High-performance REST APIs  
- **SQLite** – Lightweight alert storage  
- **Uvicorn** – ASGI server  

---

### 🔹 Agentic AI Layer
- **Google AI Studio (Gemini)**
- **Prompt Engineering**
- **MITRE ATT&CK Framework**

**Purpose:**  
Convert numerical anomalies into interpretable cybersecurity intelligence.

---

### 🔹 Frontend & Visualization
- **React.js**
- **Chart.js**
- **MITRE ATT&CK Heatmap**
- **Alert Detail Panels**

---

## 🎯 Key Outcome

DOT Sentinel AI demonstrates how **raw network traffic** can be transformed into **actionable security insights** by combining:

- Network traffic analysis  
- Unsupervised ML  
- Agentic AI reasoning  
- Industry-standard threat frameworks  

---

## 🧪 Demo Flow

1. Upload PCAP file  
2. System detects anomalous flows  
3. Alerts are generated  
4. AI explains the threat  
5. MITRE ATT&CK mapping is displayed  
6. Recommended actions are shown  

---

## 📚 Academic & Industry Relevance

- Aligns with modern SOC workflows  
- Uses accepted datasets and frameworks  
- Balances explainability with automation  

---

## 👨‍💻 Authors
Capstone Project – Final Year  

