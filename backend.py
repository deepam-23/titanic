from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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
from data_loader import load_titanic_dataset

app = FastAPI(title="Titanic Chat Agent API")

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    visualization: str = None
    chart_type: str = None

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

@app.post("/query", response_model=QueryResponse)
async def query_titanic_data(request: QueryRequest):
    """Process a query about the Titanic dataset."""
    try:
        # Get text answer
        answer = analyze_titanic_data(request.question)
        
        # Create visualization if applicable
        df = load_titanic_dataset()
        viz = create_visualization(df, request.question)
        
        response = QueryResponse(answer=answer)
        
        if viz:
            response.visualization = viz["chart"]
            response.chart_type = viz["type"]
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Titanic Chat Agent API is running!"}

@app.get("/dataset_info")
async def get_dataset_info():
    """Get information about the Titanic dataset."""
    df = load_titanic_dataset()
    return {
        "shape": df.shape,
        "columns": list(df.columns),
        "sample_data": df.head().to_dict("records")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
