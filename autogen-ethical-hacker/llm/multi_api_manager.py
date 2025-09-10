import time
from autogen_agentchat.agents import AssistantAgent
import json
import os


# Load API keys from the repo-level config directory robustly
def load_apis():
    # project root is one level above the package directory
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    config_path = os.path.join(project_root, 'config', 'apis.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[multi_api_manager] Warning: apis.json not found at {config_path}")
        return {}
    except Exception as e:
        print(f"[multi_api_manager] Error reading apis.json: {e}")
        return {}


apis = load_apis()


def llm_ensemble_reasoning(exploit_results):
    responses = []
    if not apis:
        return {'error': 'no API keys configured'}

    config_list = []
    for k in apis.get('groq', []):
        config_list.append({
            "api_type": "groq",
            "model": "groq/gpt-oss-120b",
            "api_key": k,
            "base_url": "https://api.groq.com/openai/v1"
        })
    for k in apis.get('gemini', []):
        config_list.append({
            "api_type": "google",
            "model": "gemini-1.5-pro",
            "api_key": k
        })

    # Create a Groq client from the first groq api key and run a completion for ensemble reasoning
    if apis.get('groq'):
        from groq import Groq
        groq_client = Groq(api_key=apis.get('groq', {}).get('api_key', ''))
        try:
            completion = groq_client.chat.completions.create(
                model="groq/gpt-oss-120b",
                messages=[{"role": "user", "content": f"Analyze exploit results: {json.dumps(exploit_results)}. Return a JSON object with findings and confidence score."}],
                temperature=1,
                max_completion_tokens=8192,
                top_p=1,
                reasoning_effort="medium",
                stream=False
            )
            responses.append({'api': 'ensemble', 'response': completion.choices[0].message.content})
        except Exception as e:
            responses.append({'api': 'ensemble', 'error': str(e)})
    # Ensemble voting: pick the most confident response (if available)
    for r in responses:
        if 'response' in r:
            resp = r['response']
            # If response is a string, try to parse as JSON
            if isinstance(resp, str):
                try:
                    parsed = json.loads(resp)
                    return parsed
                except Exception:
                    # Return as string if not JSON
                    return {'findings': resp, 'confidence': None}
            return resp
    # If all failed, return collected errors for debugging
    return {'errors': responses}
