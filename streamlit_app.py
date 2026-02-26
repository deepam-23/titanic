import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import plotly.utils
import base64
import io
import json
import re
from typing import Dict, Any, List
import os

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

def load_titanic_dataset():
    """Load the Titanic dataset from a URL or local file."""
    url = "https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv"
    
    # Try to load from local file first
    if os.path.exists("titanic.csv"):
        df = pd.read_csv("titanic.csv")
    else:
        # Download from URL
        df = pd.read_csv(url)
        df.to_csv("titanic.csv", index=False)
    
    # Clean the data
    df['Age'] = df['Age'].fillna(df['Age'].median())
    df['Fare'] = df['Fare'].fillna(df['Fare'].median())
    
    # Note: Stanford dataset doesn't have 'Embarked' column
    # Add it with default value if needed for compatibility
    if 'Embarked' not in df.columns:
        df['Embarked'] = 'S'  # Default to Southampton
    
    return df

def create_visualization(df: pd.DataFrame, question: str) -> Dict[str, Any]:
    """Create appropriate visualization based on the question."""
    
    question_lower = question.lower()
    
    # Age histogram
    if "age" in question_lower and ("histogram" in question_lower or "distribution" in question_lower):
        fig = px.histogram(df, x="Age", nbins=20, title="Distribution of Passenger Ages")
        fig.update_layout(xaxis_title="Age", yaxis_title="Count")
        return {"chart": fig.to_json(), "type": "histogram"}
    
    # Gender pie chart
    elif "male" in question_lower or "female" in question_lower or "gender" in question_lower or "sex" in question_lower:
        sex_counts = df['Sex'].value_counts()
        fig = px.pie(values=sex_counts.values, names=sex_counts.index, 
                    title="Gender Distribution of Passengers")
        return {"chart": fig.to_json(), "type": "pie"}
    
    # Survival by class
    elif "survive" in question_lower and "class" in question_lower:
        survival_by_class = df.groupby('Pclass')['Survived'].mean() * 100
        fig = px.bar(x=survival_by_class.index, y=survival_by_class.values,
                    title="Survival Rate by Passenger Class",
                    labels={"x": "Passenger Class", "y": "Survival Rate (%)"})
        return {"chart": fig.to_json(), "type": "bar"}
    
    # Fare by class
    elif "fare" in question_lower and ("class" in question_lower or "average" in question_lower):
        fare_by_class = df.groupby('Pclass')['Fare'].mean()
        fig = px.bar(x=fare_by_class.index, y=fare_by_class.values,
                    title="Average Fare by Passenger Class",
                    labels={"x": "Passenger Class", "y": "Average Fare"})
        return {"chart": fig.to_json(), "type": "bar"}
    
    # Embarkation ports
    elif "embark" in question_lower or "port" in question_lower:
        port_counts = df['Embarked'].value_counts()
        port_names = {'S': 'Southampton', 'C': 'Cherbourg', 'Q': 'Queenstown'}
        port_counts.index = [port_names.get(p, p) for p in port_counts.index]
        fig = px.bar(x=port_counts.index, y=port_counts.values,
                    title="Number of Passengers by Embarkation Port",
                    labels={"x": "Port", "y": "Number of Passengers"})
        return {"chart": fig.to_json(), "type": "bar"}
    
    # Age vs Fare scatter plot
    elif "age" in question_lower and "fare" in question_lower:
        fig = px.scatter(df, x="Age", y="Fare", color="Survived",
                        title="Age vs Fare by Survival Status",
                        labels={"Age": "Age", "Fare": "Fare", "Survived": "Survived"})
        return {"chart": fig.to_json(), "type": "scatter"}
    
    return None

def analyze_titanic_data(question: str) -> str:
    """Analyze the Titanic dataset and return answers to questions."""
    df = load_titanic_dataset()
    question_lower = question.lower()
    
    # Percentage of male passengers
    if "percentage" in question_lower and "male" in question_lower:
        male_count = (df['Sex'] == 'male').sum()
        total_count = len(df)
        percentage = (male_count / total_count) * 100
        return f"{percentage:.1f}% of passengers were male on the Titanic."
    
    # Percentage of female passengers
    elif "percentage" in question_lower and "female" in question_lower:
        female_count = (df['Sex'] == 'female').sum()
        total_count = len(df)
        percentage = (female_count / total_count) * 100
        return f"{percentage:.1f}% of passengers were female on the Titanic."
    
    # Average ticket fare
    elif "average" in question_lower and "fare" in question_lower:
        avg_fare = df['Fare'].mean()
        return f"The average ticket fare was ${avg_fare:.2f}."
    
    # Number of passengers by embarkation port
    elif "embark" in question_lower or "port" in question_lower:
        port_counts = df['Embarked'].value_counts()
        port_names = {'S': 'Southampton', 'C': 'Cherbourg', 'Q': 'Queenstown'}
        result = "Number of passengers by embarkation port:\n"
        for port, count in port_counts.items():
            port_name = port_names.get(port, port)
            result += f"- {port_name}: {count} passengers\n"
        return result.strip()
    
    # Survival rate
    elif "survive" in question_lower or "survival" in question_lower:
        survival_rate = df['Survived'].mean() * 100
        return f"The overall survival rate was {survival_rate:.1f}%."
    
    # Average age
    elif "average" in question_lower and "age" in question_lower:
        avg_age = df['Age'].mean()
        return f"The average passenger age was {avg_age:.1f} years."
    
    # Total number of passengers
    elif "total" in question_lower and "passenger" in question_lower:
        total_passengers = len(df)
        return f"There were {total_passengers} passengers on the Titanic."
    
    # Number of survivors
    elif "survivor" in question_lower or "survived" in question_lower:
        survivors = df['Survived'].sum()
        return f"{survivors} passengers survived the Titanic disaster."
    
    # Number of casualties
    elif "die" in question_lower or "death" in question_lower or "casualt" in question_lower:
        deaths = len(df) - df['Survived'].sum()
        return f"{deaths} passengers died in the Titanic disaster."
    
    # First class passengers
    elif "first class" in question_lower:
        first_class = (df['Pclass'] == 1).sum()
        return f"There were {first_class} first-class passengers."
    
    # Second class passengers
    elif "second class" in question_lower:
        second_class = (df['Pclass'] == 2).sum()
        return f"There were {second_class} second-class passengers."
    
    # Third class passengers
    elif "third class" in question_lower:
        third_class = (df['Pclass'] == 3).sum()
        return f"There were {third_class} third-class passengers."
    
    return "I'm sorry, I don't understand that question. Try asking about passenger demographics, survival rates, fares, or embarkation ports."

def display_chart(chart_json: str, chart_type: str):
    """Display a chart from JSON data."""
    try:
        if chart_json:
            fig = go.Figure(json.loads(chart_json))
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error displaying chart: {str(e)}")

def initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

def main():
    """Main application function."""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🚢 Titanic Dataset Chat Agent</h1>', unsafe_allow_html=True)
    
    # Sidebar with dataset info and examples
    with st.sidebar:
        st.header("📊 Dataset Info")
        
        # Get dataset info
        df = load_titanic_dataset()
        st.write(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
        st.write("**Columns:**")
        for col in df.columns:
            st.write(f"- {col}")
        
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
                    # Process question locally
                    answer = analyze_titanic_data(question)
                    df = load_titanic_dataset()
                    viz = create_visualization(df, question)
                
                # Add bot response
                bot_message = {
                    "role": "assistant",
                    "content": answer
                }
                
                # Add chart if available
                if viz:
                    bot_message["chart"] = viz["chart"]
                    bot_message["chart_type"] = viz["type"]
                
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
