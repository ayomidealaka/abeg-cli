# abeg-cli

abeg-cli is a Command Line Interface (CLI) companion designed to streamline your CLI workflow by generating quick command line instructions for common tasks. Acting like a co-pilot for your terminal, abeg-cli translates natural language descriptions into succinct, executable commands.

This currently uses OpenAI's gpt-4-0125-preview model.

## How it Works

Simply tell abeg-cli what you need in plain English, and it will provide you with the exact command to execute. Whether you need to stop all services running on a particular port, set up a local server, or manage containerized applications, abeg-cli is your go-to assistant for fast and reliable command generation.

## Example Usage

Imagine you need to stop all running services on port 3000. Instead of scouring the web for solutions, simply type:

```bash
abeg command to stop all running services on port 3000
```

'abeg-cli' will immediately respond with a command like:

```bash
kill $(lsof -t -i:3000)
```

Run the returned command in your terminal, and your task is done!

## Configuration

Before using the CLI tool, you need to set up your OpenAI API key as an environment variable. This ensures secure authentication with the OpenAI service.

### Obtaining Your OpenAI API Key

If you don't already have an OpenAI API key, you can obtain one by signing up or logging into your account at OpenAI API.

### Setting Up Your API Key

Set the required environment variables:

```bash
export OPENAI_API_KEY='your_api_key_here'
```