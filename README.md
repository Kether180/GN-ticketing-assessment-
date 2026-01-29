# Ticketing System

A support ticket API with an AI-powered assistant that can create, update, and manage tickets through natural language.

## Project Structure

```
├── api/              # FastAPI backend
├── agent/            # LangGraph agent with Azure OpenAI
├── infra/            # Terraform config for Azure deployment
└── .github/workflows # PR review automation
```

## Technologies

**API**
- Python 3.11+
- FastAPI, Pydantic, Uvicorn

**Agent**
- LangChain, LangGraph
- Azure OpenAI (GPT-4)
- httpx for API calls

**Infrastructure**
- Terraform
- Azure Container Apps

**CI/CD**
- GitHub Actions

## Setup

### 1. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

Copy the example env file and fill in your Azure OpenAI credentials:

```bash
cp .env.example .env
```

Required variables:
- `AZURE_OPENAI_ENDPOINT` - Your Azure OpenAI endpoint
- `AZURE_OPENAI_API_KEY` - Your API key
- `AZURE_OPENAI_DEPLOYMENT` - Model deployment name (e.g., gpt-4)
- `AZURE_OPENAI_API_VERSION` - API version (e.g., 2024-02-01)

## Running the API

Start the ticket API server:

```bash
uvicorn api.main:app --port 8001 --reload
```

The API will be available at `http://localhost:8001`. You can view the docs at `/docs`.

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /tickets | Create a ticket |
| GET | /tickets | List all tickets |
| GET | /tickets/{id} | Get a specific ticket |
| PATCH | /tickets/{id} | Update a ticket |
| DELETE | /tickets/{id} | Delete a ticket |
| POST | /tickets/{id}/comments | Add a comment |

## Running the Agent

With the API running, start the agent in another terminal:

```bash
python -m agent.main
```

The agent understands natural language requests like:
- "Create a ticket about the login page being slow"
- "Show me all open tickets"
- "Mark ticket abc-123 as resolved, the fix was deployed"
- "Add a comment to ticket abc-123 saying we're looking into it"

## Terraform (Azure Deployment)

The `infra/` folder contains Terraform configuration for deploying to Azure Container Apps.

```bash
cd infra
terraform init
terraform validate
terraform plan
```

Note: You'll need Azure credentials configured to actually deploy.

## PR Review Bot

The `.github/workflows/pr-review.yml` workflow automatically reviews pull requests using Azure OpenAI. It triggers on new PRs and posts feedback as a comment.

Required GitHub secrets:
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`

## Authentication

The API requires an API key for all ticket endpoints. Pass it in the `X-API-Key` header:

```bash
curl -H "X-API-Key: secret" http://localhost:8001/tickets
```

Without the header, you'll get a 401 error.

For production, change the key in `api/auth.py` or switch to an environment variable.
