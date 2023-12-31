import requests
import json

def generate_full_reponse(prompt):
    r = requests.post('http://0.0.0.0:11434/api/generate',
                      json={
                          'model': "llama2",
                          'prompt': prompt,
                      },
                      stream=False)
    full_response = ""    
    for line in r.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            json_line = json.loads(decoded_line)
            full_response += json_line.get("response", "")
            if json_line.get("done"):
                break

    # print(full_response)
    return full_response

def generate_adaptive_response(prompt):
    r = requests.post('http://0.0.0.0:11434/api/generate',
                      json={
                          'model': "llama2",
                          'prompt': prompt,
                      },
                      stream=True)
    for line in r.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            json_line = json.loads(decoded_line)
            # print(json_line.get("response", ""), end="")
            if json_line.get("done"):
                print()
                break

# response = generate_adaptive_response("Why is mankind evil?")