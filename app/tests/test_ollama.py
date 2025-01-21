import requests
import json

def generate_streaming(prompt, model="llama3.1:latest", api_url="http://localhost:11434/api/generate"):
    """
    Send a streaming request to Ollama API and yield responses
    
    Args:
        prompt (str): The prompt to send to the model
        model (str): The model to use (default: llama3.1:latest)
        api_url (str): The Ollama API endpoint URL
        
    Yields:
        dict: Parsed JSON response from the API
    """
    
    # Prepare the request payload
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # Send POST request with streaming enabled
        with requests.post(api_url, json=payload, headers=headers, stream=True) as response:
            response.raise_for_status()  # Raise exception for bad status codes
            
            # Process the streaming response
            for line in response.iter_lines():
                if line:
                    # Parse JSON response
                    json_response = json.loads(line)
                    yield json_response
                    
                    # Check if response is done
                    if json_response.get("done", False):
                        break
                        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        raise
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        raise

# Example usage
if __name__ == "__main__":
    prompt = "define earth"
    
    try:
        # Get streaming responses
        for response in generate_streaming(prompt):
            # Print the generated text if available
            if "response" in response:
                print(response["response"], end="", flush=True)
            
            # Print final statistics when done
            if response.get("done", False):
                print("\n\nGeneration complete!")
                print(f"Total duration: {response.get('total_duration', 0)}ms")
                print(f"Load duration: {response.get('load_duration', 0)}ms")
                print(f"Prompt eval count: {response.get('prompt_eval_count', 0)}")
                print(f"Prompt eval duration: {response.get('prompt_eval_duration', 0)}ms")
                print(f"Eval count: {response.get('eval_count', 0)}")
                print(f"Eval duration: {response.get('eval_duration', 0)}ms")
    
    except Exception as e:
        print(f"An error occurred: {e}")