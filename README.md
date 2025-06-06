# 🏆 CardioGuard AI - CCLS Datathon 2025 Winner

[![Winner](https://img.shields.io/badge/s://img.g.OpenAI](https://img.shields..microsoft.com/en-us/products Winning Submission at CCLS Datathon 2025 (Aachen, organized by HDS-LEE)**

An intelligent healthcare tool that extracts data from doctor's notes, calculates Framingham Heart Failure Risk Scores, and provides personalized preventative care recommendations through a multi-agent AI system[1][2][3].

## ✨ Features

- **📄 PDF Data Extraction**: Automatically extracts patient data from doctor's notes using RAG with structured output
- **🧮 Risk Score Calculation**: Implements Framingham Heart Failure Risk Score algorithm
- **🤖 Multi-Agent Recommendations**: Personalized health advice using specialized AI agents for different risk levels
- **📧 Critical Alert System**: Automatic email notifications for critical vital parameters
- **🎯 Risk-Stratified Care**: Tailored recommendations for low, medium, and high-risk patients
- **🖥️ User-Friendly Interface**: Clean Gradio-based web interface

## 🛠️ Tech Stack

- **Frontend**: Gradio
- **LLM**: Azure OpenAI (GPT-4.1)
- **RAG Framework**: agno with structured output
- **Vector Database**: ChromaDB
- **Agent Framework**: smolagents
- **PDF Processing**: PyPDF with chunking
- **Search Integration**: DuckDuckGo API
- **Email Alerts**: SMTP with SSL

## 🚀 Installation

### Prerequisites
- Python 3.8+
- Conda environment manager
- Azure OpenAI API access

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/your-username/cardioguard-ai
cd cardioguard-ai
```

2. **Create conda environment**
```bash
conda create -n cardioguard python=3.8
conda activate cardioguard
```

3. **Install dependencies**
```bash
pip install gradio agno smolagents chromadb numpy azure-openai
pip install -r requirements.txt
```

4. **Configure email settings**
Edit the email configuration in `agent_selector.py`:
```python
SENDER_EMAIL = "your-email@gmail.com"
SENDER_PASSWORD = "your-app-password" 
RECEIVER_EMAIL = "doctor@hospital.com"
```

5. **Set up Azure OpenAI credentials**
Update the credentials in `extract_pdf.py` and `agent_selector.py`

## 📖 Usage

1. **Launch the interface**
```bash
python interface.py
```

2. **Extract patient data**
   - Upload a PDF containing doctor's notes
   - Click "Daten aus PDF extrahieren" (Extract from PDF)
   - Review and manually adjust extracted data if needed

3. **Generate recommendations**
   - Click "Score berechnen" (Calculate Score)
   - View risk stratification and personalized recommendations
   - Critical cases automatically trigger email alerts

## 📱 Screenshots

![Main Interface](https://github.com/user-attachments/assets for patient data input and PDF upload*

![Risk Calculation](https://github.com/user-attachments/assets display*

![Recommendations](https://github.com/user-attachments/assets/alized health recommendations*

## 🏗️ Architecture

### Risk Stratification System
- **Low Risk**: General prevention strategies and lifestyle advice
- **Medium Risk**: Targeted interventions and enhanced monitoring  
- **High Risk**: Critical care protocols with immediate medical alerts

### Multi-Agent Framework
- **PDF Extraction Agent**: Structured data extraction using Pydantic models
- **Risk Assessment Agent**: Framingham score calculation with clinical alerts
- **Prevention Agents**: Specialized agents for each risk category
- **Search Integration**: Real-time medical literature search via DuckDuckGo

### Data Flow
```
PDF Upload → RAG Extraction → Risk Calculation → Agent Selection → Recommendations → Email Alerts
```

## ⚠️ Current Limitations

- **Email Trigger Logic**: Agent to determine when email alerts should be sent needs refinement
- **PDF Format Support**: Currently optimized for English-language medical notes
- **Real-time Integration**: No direct EHR system integration yet

## 👥 Team

**Developed by:**
- **Suchandra Bhattacharyya**
- **Marie Mehlfeldt** 
- **Angelina Jordine** 

## 🏆 Event Details

- **Event**: CCLS Datathon 2025
- **Location**: Aachen, Germany
- **Organizer**: HDS-LEE
- **Dates**: June 5-6, 2025
- **Result**: 🥇 **Winning Submission**

## 🔬 Clinical Validation

The Framingham Heart Failure Risk Score implementation follows established clinical guidelines and includes validation for:
- Age-stratified risk factors
- Gender-specific risk calculations  
- Comprehensive vital parameter monitoring
- Evidence-based intervention thresholds

## 🚀 Future Enhancements

- [ ] EHR system integration
- [ ] Multi-language PDF support
- [ ] Advanced ML risk prediction models
- [ ] Real-time patient monitoring dashboard
- [ ] Mobile application development

---

*This project demonstrates the potential of AI-powered healthcare tools to improve preventative care and patient outcomes through intelligent risk assessment and personalized recommendations.*

[1] programming.medical_applications
[2] programming.patient_education
[3] programming.agent_selection
