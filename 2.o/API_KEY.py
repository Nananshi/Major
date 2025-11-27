import google.generativeai as genai

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyCB_6x5ef5qvE5jtAe0jmPC0YeRDoh9BOk"
genai.configure(api_key=GEMINI_API_KEY)

# List available models
models = genai.list_models()  # This returns a generator
for m in models:
    print(m)
