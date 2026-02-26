import pandas as pd
import os

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

def get_dataset_info():
    """Get basic information about the Titanic dataset."""
    df = load_titanic_dataset()
    return {
        "shape": df.shape,
        "columns": list(df.columns),
        "description": {
            "Survived": "0 = No, 1 = Yes",
            "Pclass": "Ticket class (1 = 1st, 2 = 2nd, 3 = 3rd)",
            "Name": "Passenger name",
            "Sex": "Gender (male/female)",
            "Age": "Age in years",
            "Siblings/Spouses Aboard": "Number of siblings/spouses aboard",
            "Parents/Children Aboard": "Number of parents/children aboard",
            "Fare": "Passenger fare",
            "Embarked": "Port of Embarkation (C = Cherbourg, Q = Queenstown, S = Southampton)"
        }
    }
