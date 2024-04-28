from yaspin import yaspin
import argparse
import sys
import platform
import os
from openai import OpenAI
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
import sys, traceback

class Style:
    GREY = '\033[90m'
    RED = '\033[31m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    CYAN = '\033[36m'
    UNDERLINE = '\033[4m'
    YELLOW = "\033[1;33m"
    GREEN = "\033[0;32m"

def print_custom_help():
    custom_help_text = f"""
{Style.BOLD}Usage of abeg:{Style.RESET}
  {Style.BOLD}abeg{Style.RESET} [command you need help with]
  Type a command after '{Style.BOLD}abeg{Style.RESET}' to get specific CLI commands generated for various tasks.

Examples:
  $ {Style.BOLD}abeg{Style.RESET} stop all services on port 3000
  $ {Style.BOLD}abeg{Style.RESET} setup a new Django project

{Style.BOLD}Setting Up the OpenAI API Key:{Style.RESET}
  Before using 'abeg', you must set your OpenAI API key as an environment variable.
  
  1. Obtain your API key from OpenAI by visiting:
     {Style.BOLD}https://platform.openai.com/account/api-keys{Style.RESET}

  2. Set your API key in your terminal:
     {Style.BOLD}$ export OPENAI_API_KEY='your_openai_api_key_here'{Style.RESET}
  
  3. You can add the export line to your shell's profile script (.bashrc, .zshrc, etc.) to make it permanent.

Please replace 'your_openai_api_key_here' with the actual API key you obtained from OpenAI.
"""
    print(custom_help_text)

def print_version():
    print(__version__)

__version__ = "v0.0.1"

def requestFromAI(question, client):
    architecture = platform.machine()
    os_name = os.name
    sysinfo = f"Architecture: {architecture}, OS: {os_name}"
    prompt = f"""
        You are ABEG, a CLI code generator. Respond with the CLI command to generate the code with only one short sentence description in first line 
        Your response should always and MUST always be accompanied with only one short sentence description in the first line even when the user repeats the same question.
		If the user asks for a specific language, respond with the CLI command to generate the code in that language.
		If CLI command is multiple lines, separate each line with a newline character and always have the one short sentence description in the first line before the command.
		Do not write any markdown. Do not write any code.
        System Info: {sysinfo}
    
		First line is the description in one sentence.
		
        Example output:

		Building and installing a Go binary
		go build main.go
		go install main
        """
    try:
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": question}
            ]            
        )
        response_content = response.choices[0].message.content
        lines = response_content.split('\n')

        formatted_lines = [f"{Style.YELLOW}{lines[0]}{Style.RESET}\n"] + \
                        [f"{Style.GREEN}${Style.RESET} {line}" for line in lines[1:]]

        formatted_output = '\n'.join(formatted_lines)
        print(formatted_output)

        return response.choices[0].message.content
    except ConnectionError:
        print(f"{Style.RED}Error:{Style.RESET} Failed to get help due to network issues. Please check your internet connection.")
    except SystemExit as e:
        sys.exit(e)
    except Exception as e:
        print(f"An error occurred: {e}")
        # traceback.print_exc() 
        sys.exit(1)
    except:
        raise SystemExit()


def main():
    if "-h" in sys.argv or "--help" in sys.argv:
        print_custom_help()
        sys.exit(0) 
    elif "-v" in sys.argv or "--version" in sys.argv:
        print_version()
        sys.exit(0) 

    api_key = os.getenv('OPENAI_API_KEY')
    
    if api_key is None:
        print(f"{Style.RED}Error:{Style.RESET} OpenAI API key not found. Please set the OPENAI_API_KEY environment variable using 'export OPENAI_API_KEY=your_openai_api_key'")
        sys.exit(1)
    
    client = OpenAI(
        api_key=api_key
    )
    
    command_description = ' '.join(sys.argv[1:])
    requestFromAI(command_description, client)
        
if __name__ == "__main__":
    main()