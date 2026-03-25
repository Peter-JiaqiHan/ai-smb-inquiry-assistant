import requests
import os
from dotenv import load_dotenv

load_dotenv()

# 尝试访问一个公共网站
def test_basic_http_request():
    print("Testing basic HTTP request to google.com...")
    try:
        response = requests.get("https://www.google.com", timeout=10)
        if response.status_code == 200:
            print("Successfully connected to Google!")
        else:
            print(f"Failed to connect to Google. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Google: {e}")

# 尝试访问 OpenAI API (无需实际有效的API Key，只是测试连接)
def test_openai_api_connection():
    print("\nTesting connection to OpenAI API endpoint...")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    test_url = f"{OPENAI_BASE_URL}/models" # 一个不需要认证就能访问的公共端点
    try:
        # 使用 requests 库直接测试，不依赖于 openai 客户端
        response = requests.get(test_url, timeout=10)
        if response.status_code == 200:
            print(f"Successfully connected to OpenAI API endpoint: {test_url}")
        else:
            print(f"Failed to connect to OpenAI API endpoint. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to OpenAI API endpoint: {e}")

if __name__ == "__main__":
    test_basic_http_request()
    test_openai_api_connection()
