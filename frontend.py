import streamlit as st
import requests
import json
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time

# Configure page
st.set_page_config(
    page_title="Titanic Dataset Chat Agent",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .bot-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .example-question {
        background-color: #f5f5f5;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.25rem 0;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    .example-question:hover {
        background-color: #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# API endpoint
BACKEND_URL = "http://localhost:8000"

def initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "api_available" not in st.session_state:
        st.session_state.api_available = False

def check_api_connection():
    """Check if the backend API is available."""
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=5)
        st.session_state.api_available = response.status_code == 200
        return st.session_state.api_available
    except:
        st.session_state.api_available = False
        return False

def query_backend(question: str):
    """Send a query to the backend API."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/query",
            json={"question": question},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection Error: {str(e)}"}

def display_chart(chart_json: str, chart_type: str):
    """Display a chart from JSON data."""
    try:
        if chart_json:
            fig = go.Figure(json.loads(chart_json))
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error displaying chart: {str(e)}")

def main():
    """Main application function."""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🚢 Titanic Dataset Chat Agent</h1>', unsafe_allow_html=True)
    
    # Check API connection
    if not check_api_connection():
        st.error("⚠️ Backend API is not running. Please start the backend with: `python backend.py`")
        st.info("The backend should be running on http://localhost:8000")
        return
    
    # Sidebar with dataset info and examples
    with st.sidebar:
        st.header("📊 Dataset Info")
        
        # Get dataset info
        try:
            response = requests.get(f"{BACKEND_URL}/dataset_info", timeout=5)
            if response.status_code == 200:
                info = response.json()
                st.write(f"**Shape:** {info['shape'][0]} rows × {info['shape'][1]} columns")
                st.write("**Columns:**")
                for col in info['columns']:
                    st.write(f"- {col}")
        except:
            st.write("Unable to fetch dataset info")
        
        st.header("💡 Example Questions")
        examples = [
            "What percentage of passengers were male on the Titanic?",
            "Show me a histogram of passenger ages",
            "What was the average ticket fare?",
            "How many passengers embarked from each port?",
            "What was the survival rate?",
            "How many first-class passengers were there?",
            "What was the average passenger age?",
            "Show me the relationship between age and fare"
        ]
        
        for example in examples:
            if st.button(example, key=f"example_{examples.index(example)}"):
                st.session_state.example_question = example
    
    # Check if an example question was selected
    if "example_question" in st.session_state:
        question = st.session_state.example_question
        del st.session_state.example_question
        # Add the question to the input
        st.session_state.input_question = question
    
    # Chat interface
    st.header("💬 Chat with the Titanic Dataset")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {message["content"]}</div>', 
                          unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message bot-message"><strong>🤖 Titanic Agent:</strong> {message["content"]}</div>', 
                          unsafe_allow_html=True)
                if "chart" in message and message["chart"]:
                    display_chart(message["chart"], message.get("chart_type", ""))
    
    # Input area
    st.subheader("Ask a Question:")
    
    # Use text_input with a key to preserve the example question
    question = st.text_input(
        "Type your question about the Titanic dataset:",
        key="input_question",
        placeholder="e.g., What percentage of passengers survived?"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("📤 Send", type="primary"):
            if question.strip():
                # Add user message to chat
                st.session_state.messages.append({"role": "user", "content": question})
                
                # Show loading spinner
                with st.spinner("🤔 Thinking..."):
                    # Query backend
                    response = query_backend(question)
                
                if "error" in response:
                    # Add error message
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": f"❌ {response['error']}"
                    })
                else:
                    # Add bot response
                    bot_message = {
                        "role": "assistant",
                        "content": response["answer"]
                    }
                    
                    # Add chart if available
                    if response.get("visualization"):
                        bot_message["chart"] = response["visualization"]
                        bot_message["chart_type"] = response.get("chart_type", "")
                    
                    st.session_state.messages.append(bot_message)
                
                # Clear the input
                st.session_state.input_question = ""
                
                # Rerun to update the chat
                st.rerun()
    
    with col2:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "Built with FastAPI, LangChain, and Streamlit | 🚢 Titanic Dataset Analysis"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
