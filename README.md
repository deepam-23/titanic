# 🚢 Titanic Dataset Chat Agent

A friendly AI-powered chatbot that analyzes the famous Titanic dataset using natural language queries. Users can ask questions in plain English and receive both text answers and interactive visualizations about Titanic passengers.

## ✨ Features

- 🤖 **Natural Language Processing** - Ask questions in plain English
- 📊 **Interactive Visualizations** - Automatic chart generation with Plotly
- 💬 **Real-time Chat Interface** - Modern Streamlit UI with chat history
- 🎯 **Smart Query Analysis** - Intelligent response system for dataset queries
- 📱 **Responsive Design** - Works on desktop and mobile devices

## 🛠️ Tech Stack

- **Backend**: FastAPI with intelligent query processing
- **Frontend**: Streamlit with responsive chat interface  
- **Data Analysis**: Pandas, NumPy, Matplotlib, Seaborn
- **Visualizations**: Plotly for interactive charts
- **Dataset**: Stanford Titanic dataset (887 passengers)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/deepam-23/titanic.git
cd titanic
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Start the backend**
```bash
python backend.py
```

4. **Start the frontend** (in a new terminal)
```bash
streamlit run frontend.py
```

5. **Open your browser**
Navigate to `http://localhost:8501` to start chatting!

## 📱 Live Demo

**Try the chatbot here:** https://deepam-23-titanic-chat.streamlit.app

## 💬 Example Questions

Here are some questions you can ask the Titanic chatbot:

### Demographics
- "What percentage of passengers were male on the Titanic?"
- "What was the average passenger age?"
- "How many first-class passengers were there?"

### Survival Analysis
- "What was the survival rate?"
- "How many passengers survived the Titanic disaster?"
- "Show me survival rates by passenger class"

### Financial Data
- "What was the average ticket fare?"
- "Show me the relationship between age and fare"
- "How did fares vary by passenger class?"

### Visualizations
- "Show me a histogram of passenger ages"
- "Create a pie chart of gender distribution"
- "Plot survival rate by class"

### Embarkation
- "How many passengers embarked from each port?"
- "Which port had the most passengers?"

## 🏗️ Project Structure

```
titanic/
├── backend.py              # FastAPI backend server
├── frontend.py             # Streamlit frontend interface
├── data_loader.py          # Dataset loading and preprocessing
├── requirements.txt        # Python dependencies
├── test_backend.py         # Backend testing script
├── start.py               # Startup script
├── deploy_instructions.md # Deployment guide
├── titanic.csv            # Dataset (auto-downloaded)
└── README.md              # This file
```

## 🔧 API Endpoints

### Backend API (http://localhost:8000)

- `GET /` - Health check
- `GET /dataset_info` - Get dataset information
- `POST /query` - Process natural language queries

### Example API Usage
```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"question": "What percentage of passengers were male?"}'
```

## 🌐 Deployment

### Streamlit Cloud (Recommended)
1. Push code to GitHub
2. Go to https://share.streamlit.io/
3. Connect your GitHub repository
4. Select `frontend.py` as main file
5. Deploy!

### Other Options
- **Ngrok** - For temporary public URLs
- **Railway.app** - Full-stack deployment
- **Render.com** - Free hosting option

See [deploy_instructions.md](deploy_instructions.md) for detailed deployment guide.

## 📊 Dataset Information

The chatbot uses the Stanford Titanic dataset containing:
- **887 passengers** with complete records
- **9 features**: Survived, Pclass, Name, Sex, Age, Siblings/Spouses, Parents/Children, Fare, Embarked
- **Cleaned data** with missing values handled

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Stanford University for the Titanic dataset
- Streamlit team for the amazing framework
- FastAPI for the robust backend framework
- Plotly for beautiful visualizations

## 📞 Contact

Created by Deepam Kumar - [GitHub](https://github.com/deepam-23)

---

⭐ **Star this repository if it helped you!**
