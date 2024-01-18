import requests
import json
import base64
import llama_chat_gui as chat
import llama_settings_gui as settings

def choose_model_generate_response(prompt, model, image):
    # If the chat is dynamic, see if there is an image and choose model accordingly
    if settings.model.strip().lower() == "dynamically chosen models":
        # If image is nothing, generate llama2 response
        if (image == ""):
            # Update model name in settings to display correctly -- change later to one name?
            settings.model = "dynamically chosen models"
            return generate_full_reponse_llama2(prompt)
        # Else, image has to be something, so generate llava response
        else:
            # Update model name in settings to display correctly -- change later to one name?
            settings.model = "dynamically chosen models"
            return generate_full_reponse_llava(prompt, image)
    # If the chat is not dynamic, use user's preferences
    else:
        pure_model = str(model).strip().lower()
        if (pure_model == "llama2" or pure_model == "llama"):
            return generate_full_reponse_llama2(prompt)
        if (pure_model == "llava" and image != ""):
            return generate_full_reponse_llava(prompt, image)
        if(pure_model == "llava" and image == ""):
            return("No image selected. Llava requires an image selection")

def generate_full_reponse_llama2(prompt):
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
    
def generate_full_reponse_llava(prompt, image_path):
    with open(image_path, "rb") as f:
      encoded_string = base64.b64encode(f.read()).decode('utf-8')
    image_array = [encoded_string] # Can add support for multiple images here
    
    data = {"model": "llava",
          "prompt": prompt,
          "images": image_array,
          "stream": False}
    url = "http://0.0.0.0:11434/api/generate"
    response = requests.post(url, data = json.dumps(data))
    response_json = response.json()
    return response_json['response']

def generate_adaptive_response_llama2(prompt):
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