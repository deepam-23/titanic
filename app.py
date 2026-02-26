import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

# Set page config
st.set_page_config(
    page_title="Titanic Dataset Chat Agent",
    page_icon="🚢",
    layout="wide"
)

# Load dataset
@st.cache_data
def load_data():
    url = "https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv"
    df = pd.read_csv(url)
    df['Age'] = df['Age'].fillna(df['Age'].median())
    df['Fare'] = df['Fare'].fillna(df['Fare'].median())
    return df

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

def analyze_data(question, df):
    """Analyze the Titanic dataset and return answers."""
    question_lower = question.lower()
    
    # Percentage calculations
    if "percentage" in question_lower and "male" in question_lower:
        male_count = (df['Sex'] == 'male').sum()
        percentage = (male_count / len(df)) * 100
        return f"{percentage:.1f}% of passengers were male on the Titanic.", create_pie_chart(df)
    
    elif "percentage" in question_lower and "female" in question_lower:
        female_count = (df['Sex'] == 'female').sum()
        percentage = (female_count / len(df)) * 100
        return f"{percentage:.1f}% of passengers were female on the Titanic.", create_pie_chart(df)
    
    # Average calculations
    elif "average" in question_lower and "fare" in question_lower:
        avg_fare = df['Fare'].mean()
        return f"The average ticket fare was ${avg_fare:.2f}.", create_fare_chart(df)
    
    elif "average" in question_lower and "age" in question_lower:
        avg_age = df['Age'].mean()
        return f"The average passenger age was {avg_age:.1f} years.", create_age_histogram(df)
    
    # Count calculations
    elif "total" in question_lower and "passenger" in question_lower:
        return f"There were {len(df)} passengers on the Titanic.", None
    
    elif "survivor" in question_lower or "survived" in question_lower:
        survivors = df['Survived'].sum()
        return f"{survivors} passengers survived the Titanic disaster.", create_survival_chart(df)
    
    elif "die" in question_lower or "death" in question_lower:
        deaths = len(df) - df['Survived'].sum()
        return f"{deaths} passengers died in the Titanic disaster.", None
    
    elif "first class" in question_lower:
        first_class = (df['Pclass'] == 1).sum()
        return f"There were {first_class} first-class passengers.", create_class_chart(df)
    
    elif "second class" in question_lower:
        second_class = (df['Pclass'] == 2).sum()
        return f"There were {second_class} second-class passengers.", create_class_chart(df)
    
    elif "third class" in question_lower:
        third_class = (df['Pclass'] == 3).sum()
        return f"There were {third_class} third-class passengers.", create_class_chart(df)
    
    # Survival rate
    elif "survive" in question_lower or "survival" in question_lower:
        survival_rate = df['Survived'].mean() * 100
        return f"The overall survival rate was {survival_rate:.1f}%.", create_survival_chart(df)
    
    # Visualizations
    elif "age" in question_lower and ("histogram" in question_lower or "distribution" in question_lower):
        return "Here's the distribution of passenger ages:", create_age_histogram(df)
    
    elif "male" in question_lower or "female" in question_lower or "gender" in question_lower:
        return "Here's the gender distribution of passengers:", create_pie_chart(df)
    
    elif "age" in question_lower and "fare" in question_lower:
        return "Here's the relationship between age and fare:", create_scatter_chart(df)
    
    # Default response
    return "I'm sorry, I don't understand that question. Try asking about passenger demographics, survival rates, fares, or embarkation ports.", None

def create_pie_chart(df):
    """Create gender pie chart."""
    sex_counts = df['Sex'].value_counts()
    fig = px.pie(values=sex_counts.values, names=sex_counts.index, 
                title="Gender Distribution of Passengers")
    return fig.to_json()

def create_age_histogram(df):
    """Create age histogram."""
    fig = px.histogram(df, x="Age", nbins=20, title="Distribution of Passenger Ages")
    fig.update_layout(xaxis_title="Age", yaxis_title="Count")
    return fig.to_json()

def create_fare_chart(df):
    """Create fare by class chart."""
    fare_by_class = df.groupby('Pclass')['Fare'].mean()
    fig = px.bar(x=fare_by_class.index, y=fare_by_class.values,
                title="Average Fare by Passenger Class",
                labels={"x": "Passenger Class", "y": "Average Fare"})
    return fig.to_json()

def create_survival_chart(df):
    """Create survival chart."""
    survival_by_class = df.groupby('Pclass')['Survived'].mean() * 100
    fig = px.bar(x=survival_by_class.index, y=survival_by_class.values,
                title="Survival Rate by Passenger Class",
                labels={"x": "Passenger Class", "y": "Survival Rate (%)"})
    return fig.to_json()

def create_class_chart(df):
    """Create passenger class chart."""
    class_counts = df['Pclass'].value_counts().sort_index()
    fig = px.bar(x=class_counts.index, y=class_counts.values,
                title="Number of Passengers by Class",
                labels={"x": "Passenger Class", "y": "Number of Passengers"})
    return fig.to_json()

def create_scatter_chart(df):
    """Create age vs fare scatter plot."""
    fig = px.scatter(df, x="Age", y="Fare", color="Survived",
                    title="Age vs Fare by Survival Status",
                    labels={"Age": "Age", "Fare": "Fare", "Survived": "Survived"})
    return fig.to_json()

def display_chart(chart_json):
    """Display a chart from JSON data."""
    if chart_json:
        try:
            fig = go.Figure(json.loads(chart_json))
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error displaying chart: {str(e)}")

# Main app
def main():
    st.title("🚢 Titanic Dataset Chat Agent")
    
    # Load data
    df = load_data()
    
    # Sidebar info
    with st.sidebar:
        st.header("📊 Dataset Info")
        st.write(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
        st.write("**Columns:**")
        for col in df.columns:
            st.write(f"- {col}")
        
        st.header("💡 Example Questions")
        examples = [
            "What percentage of passengers were male?",
            "What was the average ticket fare?",
            "What was the survival rate?",
            "How many passengers survived?",
            "Show me age distribution",
            "How many first-class passengers?"
        ]
        
        for example in examples:
            if st.button(example, key=f"example_{examples.index(example)}"):
                st.session_state.input_question = example
    
    # Chat interface
    st.header("💬 Chat with the Titanic Dataset")
    
    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**🤖 Titanic Agent:** {message['content']}")
            if message.get("chart"):
                display_chart(message["chart"])
    
    # Input
    question = st.text_input("Ask a question about the Titanic dataset:", 
                            key="input_question",
                            placeholder="e.g., What percentage of passengers survived?")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("📤 Send", type="primary"):
            if question.strip():
                # Add user message
                st.session_state.messages.append({"role": "user", "content": question})
                
                # Process question
                with st.spinner("Thinking..."):
                    answer, chart = analyze_data(question, df)
                
                # Add bot response
                bot_message = {"role": "assistant", "content": answer}
                if chart:
                    bot_message["chart"] = chart
                st.session_state.messages.append(bot_message)
                
                # Clear input and rerun
                st.session_state.input_question = ""
                st.rerun()
    
    with col2:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

if __name__ == "__main__":
    main()
