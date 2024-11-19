from transformers import pipeline
import torch
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
import textwrap
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def initialize_pipeline():
    """Initialize the model pipeline."""
    print("Loading model pipeline...")
    pipe = pipeline(
        "text-generation",
        model="meta-llama/Llama-3.2-3B-Instruct",
        torch_dtype=torch.bfloat16,
        device_map="auto",
        token="YOUR_HUGGING_FACE_TOKEN"  # Replace with your token
    )
    return pipe

def format_messages(messages):
    """Format messages into a single prompt string."""
    formatted_prompt = "<|START|>\n"  # Add clear conversation start marker
    for message in messages:
        role = message["role"]
        content = message["content"]
        if role == "system":
            formatted_prompt += f"System: {content}\n"
        elif role == "user":
            formatted_prompt += f"Human: {content}\n"
        elif role == "assistant":
            formatted_prompt += f"Assistant: {content}\n"
    formatted_prompt += "Assistant:"  # Add explicit prompt for the assistant
    return formatted_prompt

def generate_response(messages, pipe, max_length=256):
    """Generate a response using the pipeline."""
    prompt = format_messages(messages)
    outputs = pipe(
        prompt,
        max_new_tokens=max_length,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        pad_token_id=pipe.tokenizer.eos_token_id,
        eos_token_id=pipe.tokenizer.eos_token_id,
    )
    
    # Extract only the new response
    full_response = outputs[0]["generated_text"]
    response_start = full_response.rfind("Assistant:") + len("Assistant:")
    new_response = full_response[response_start:].strip()
    
    # Clean up the response
    new_response = new_response.split("<|START|>")[0]  # Remove any new conversation starts
    new_response = new_response.split("Human:")[0]     # Remove any new user messages
    new_response = new_response.split("System:")[0]    # Remove any new system messages
    
    return new_response.strip()

def format_text(text, width=80):
    """Format text with proper wrapping."""
    return textwrap.fill(text, width=width)

def main():
    console = Console()
    
    try:
        pipe = initialize_pipeline()
        clear_screen()
        console.print("[bold green]Chat initialized! Type 'quit' to exit.[/bold green]\n")
        
        # Initialize conversation with a more specific system message
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant. Keep your responses focused and relevant to the current conversation only."}
        ]
        
        while True:
            user_input = Prompt.ask("[bold blue]You[/bold blue]")
            
            if user_input.lower() in ['quit', 'exit']:
                console.print("\n[bold green]Goodbye![/bold green]")
                break
            
            messages.append({"role": "user", "content": user_input})
            console.print("\n[bold purple]Assistant[/bold purple]:", style="bold")
            
            try:
                response = generate_response(messages, pipe)
                formatted_response = format_text(response)
                console.print(Markdown(formatted_response))
                messages.append({"role": "assistant", "content": response})
            except Exception as e:
                console.print(f"[bold red]Error generating response: {str(e)}[/bold red]")
            
            console.print()
            
    except Exception as e:
        console.print(f"[bold red]An error occurred: {str(e)}[/bold red]")

if __name__ == "__main__":
    main()