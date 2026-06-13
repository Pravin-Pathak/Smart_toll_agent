
# 🚗 Smart Toll Agent

Smart Toll Agent is an AI-powered toll management and traffic analysis system designed to automate toll operations, manage vehicle records, and provide intelligent traffic-related assistance through an interactive dashboard.

The system combines backend processing, data handling, and vector-based storage to efficiently analyze traffic rules and vehicle information.

---

## 📌 Features

- 🚦 Traffic law analysis and retrieval
- 🚘 Vehicle log management and tracking
- 🧠 AI-powered toll assistance
- 📊 Interactive dashboard interface
- 📁 Structured backend and frontend architecture
- ⚡ Fast data access using vector database storage

---

## 🏗️ Project Structure

```plaintext
Smart_toll_agent/
│
├── backend/
│   ├── app.py
│   ├── tools.py
│   └── __init__.py
│
├── frontend/
│   └── dashboard.py
│
├── data/
│   ├── traffic_laws.txt
│   └── vehicle_logs.csv
│
├── chroma_db_storage/
│
└── requirements.txt
```

---

## 🛠️ Technologies Used

- Python
- Streamlit (Dashboard/UI)
- ChromaDB
- Data Processing Libraries
- AI / Retrieval Components

---


Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

Start backend:

```bash
python backend/app.py
```

Start dashboard:

```bash
streamlit run frontend/dashboard.py
```

---

## 📂 Dataset

The project uses:

- `traffic_laws.txt` → Traffic rules and regulations
- `vehicle_logs.csv` → Vehicle-related records and logs

---

## 🎯 Future Improvements

- Real-time toll collection
- Vehicle number plate recognition
- Cloud deployment
- Analytics dashboard
- API integration

---



