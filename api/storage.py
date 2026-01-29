"""In-memory storage layer for ticket data."""
from api.models import Ticket

tickets: dict[str, Ticket] = {}


def get_all(status_filter: str | None = None) -> list[Ticket]:
    if status_filter:
        return [t for t in tickets.values() if t.status.value == status_filter]
    return list(tickets.values())


def get_by_id(ticket_id: str) -> Ticket | None:
    return tickets.get(ticket_id)


def save(ticket: Ticket) -> Ticket:
    tickets[ticket.id] = ticket
    return ticket


def delete(ticket_id: str) -> bool:
    if ticket_id in tickets:
        del tickets[ticket_id]
        return True
    return False


def clear():
    tickets.clear()
