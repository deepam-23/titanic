import requests
import json

def test_backend():
    """Test the backend API with sample questions."""
    backend_url = "http://localhost:8000"
    
    # Test if backend is running
    try:
        response = requests.get(f"{backend_url}/")
        if response.status_code == 200:
            print("✅ Backend is running!")
        else:
            print("❌ Backend is not responding correctly")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on http://localhost:8000")
        return
    
    # Test dataset info endpoint
    print("\n📊 Testing dataset info endpoint...")
    try:
        response = requests.get(f"{backend_url}/dataset_info")
        if response.status_code == 200:
            info = response.json()
            print(f"Dataset shape: {info['shape']}")
            print(f"Columns: {info['columns']}")
        else:
            print("❌ Dataset info endpoint failed")
    except Exception as e:
        print(f"❌ Error testing dataset info: {e}")
    
    # Test sample queries
    test_questions = [
        "What percentage of passengers were male on the Titanic?",
        "What was the average ticket fare?",
        "How many passengers embarked from each port?",
        "What was the survival rate?",
        "Show me a histogram of passenger ages"
    ]
    
    print("\n💬 Testing sample queries...")
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Question: {question}")
        try:
            response = requests.post(
                f"{backend_url}/query",
                json={"question": question},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   Answer: {result['answer']}")
                if result.get('visualization'):
                    print(f"   Chart: {result['chart_type']} chart generated")
                else:
                    print("   Chart: No visualization")
            else:
                print(f"   ❌ Failed with status code: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n✅ Backend testing complete!")

if __name__ == "__main__":
    test_backend()
