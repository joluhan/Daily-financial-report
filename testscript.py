from openai import OpenAI

def test_api_connection():
    """Test OpenAI API connection"""
    try:
        # Load API key from file
        with open('api_key.txt', 'r', encoding='utf-8') as file:
            api_key = file.read().strip()
        
        if not api_key:
            print("❌ API key file is empty")
            return False
        
        print("🔑 API key loaded successfully")
        print(f"🔑 Key starts with: {api_key[:10]}...")
        
        # Initialize client
        client = OpenAI(api_key=api_key)
        
        # Test simple request
        print("🧪 Testing API connection...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using cheaper model for testing
            messages=[
                {"role": "user", "content": "Hello! Just testing the API connection. Please respond with 'API connection successful!'"}
            ],
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        print(f"✅ API Response: {result}")
        
        # Test if we can access GPT-4
        print("🧪 Testing GPT-4 access...")
        response_gpt4 = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": "Reply with 'GPT-4 access confirmed!'"}
            ],
            max_tokens=50
        )
        
        result_gpt4 = response_gpt4.choices[0].message.content
        print(f"✅ GPT-4 Response: {result_gpt4}")
        
        print("🎉 All tests passed! Your API key is working correctly.")
        return True
        
    except FileNotFoundError:
        print("❌ api_key.txt file not found")
        print("Please create an api_key.txt file with your OpenAI API key")
        return False
    except Exception as e:
        print(f"❌ API Test Failed: {e}")
        
        # Check for common errors
        if "invalid_api_key" in str(e):
            print("💡 Your API key appears to be invalid")
        elif "insufficient_quota" in str(e):
            print("💡 Your account has insufficient credits")
        elif "model_not_found" in str(e):
            print("💡 The requested model is not available for your account")
        
        return False

if __name__ == "__main__":
    print("🚀 OpenAI API Connection Test")
    print("=" * 40)
    test_api_connection()