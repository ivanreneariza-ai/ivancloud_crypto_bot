import os
import sys
import json
import urllib.request
from pathlib import Path

def load_env():
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, val = line.split('=', 1)
                        os.environ[key.strip()] = val.strip()

def ask_deepseek(prompt):
    api_key = os.environ.get('DEEPSEEK_API_KEY')
    if not api_key:
        return "Error: DEEPSEEK_API_KEY no encontrada en variables de entorno."

    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data['choices'][0]['message']['content']
    except Exception as e:
        return f"Error llamando a DeepSeek: {str(e)}"

if __name__ == "__main__":
    load_env()
    prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else sys.stdin.read()
    if prompt.strip():
        print(ask_deepseek(prompt))
    else:
        print("Uso: python deepseek_bridge.py 'tu mensaje'")
