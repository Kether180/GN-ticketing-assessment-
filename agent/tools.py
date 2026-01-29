import os
import httpx
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

API_URL = os.getenv("API_BASE_URL", "http://localhost:8001")


def _handle_response(response: httpx.Response) -> dict | str:
    """Parse API response, return error details if it fails"""
    if response.status_code >= 400: # 400, 404, 422 , etc = errors
        try:
            error = response.json()
            detail = error.get("detail", {})
            if isinstance(detail, dict):
                return f"Error: {detail.get('message', str(detail))}"
            elif isinstance(detail, list):
                msgs = [d.get("msg", str(d)) for d in detail]
                return f"Validation error: {', '.join(msgs)}"
            return f"Error: {detail}"
        except Exception:
            return f"Error: {response.status_code}"
    return response.json()


@tool
def create_ticket(title: str, description: str) -> dict | str:
    """Create a new support ticket."""
    response = httpx.post(
        f"{API_URL}/tickets",
        json={"title": title, "description": description},
    )
    return _handle_response(response)


@tool
def list_tickets(status: str = None) -> dict | str:
    """List all tickets, optional: filter by status: OPEN, RESOLVED OR CLOSED"""
    params = {"status": status} if status else {}
    response = httpx.get(f"{API_URL}/tickets", params=params)
    return _handle_response(response)


@tool
def get_ticket(ticket_id: str) -> dict | str:
    """Get details of a specific ticket by ID."""
    response = httpx.get(f"{API_URL}/tickets/{ticket_id}")
    return _handle_response(response)


@tool
def update_ticket(
    ticket_id: str,
    title: str = None,
    description: str = None,
    status: str = None,
    resolution: str = None,
) -> dict | str:
    """Update a ticket. Only provide fields you want to change.
    Status must be OPEN, RESOLVED, or CLOSED.
    Setting status to RESOLVED requires a resolution note.
    """
    data = {}
    if title:
        data["title"] = title
    if description:
        data["description"] = description
    if status:
        data["status"] = status
    if resolution:
        data["resolution"] = resolution

    response = httpx.patch(f"{API_URL}/tickets/{ticket_id}", json=data)
    return _handle_response(response)


@tool
def delete_ticket(ticket_id: str) -> str:
    """Delete a ticket permanently."""
    response = httpx.delete(f"{API_URL}/tickets/{ticket_id}")
    if response.status_code == 204:
        return f"Ticket {ticket_id} deleted successfully."
    return _handle_response(response)


@tool
def add_comment(ticket_id: str, text: str) -> dict | str:
    """Add a comment to a ticket."""
    response = httpx.post(
        f"{API_URL}/tickets/{ticket_id}/comments",
        params={"text": text},
    )
    return _handle_response(response)

# List given to LLM so it knows all available tools
ALL_TOOLS = [
    create_ticket,
    list_tickets,
    get_ticket,
    update_ticket,
    delete_ticket,
    add_comment,
]
