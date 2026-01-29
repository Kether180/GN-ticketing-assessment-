from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Query
from api.models import Ticket, TicketCreate, TicketUpdate, TicketStatus, Comment
from api import storage, exceptions

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("", status_code=201, summary="Create ticket")
def create_ticket(data: TicketCreate) -> Ticket:
    """Creates a new ticket with status OPEN."""
    ticket = Ticket(
        id=str(uuid4()),
        title=data.title,
        description=data.description,
    )
    return storage.save(ticket)


@router.get("", summary="List tickets")
def list_tickets(
    status: str | None = Query(None, description="Filter: OPEN, RESOLVED, or CLOSED")
) -> list[Ticket]:
    """Returns all tickets. Use ?status= to filter."""
    if status and status not in [s.value for s in TicketStatus]:
        raise exceptions.invalid_status(status)
    return storage.get_all(status)


@router.get("/{ticket_id}", summary="Get ticket")
def get_ticket(ticket_id: str) -> Ticket:
    """Returns a single ticket by ID."""
    ticket = storage.get_by_id(ticket_id)
    if not ticket:
        raise exceptions.not_found(ticket_id)
    return ticket


@router.patch("/{ticket_id}", summary="Update ticket")
def update_ticket(ticket_id: str, data: TicketUpdate) -> Ticket:
    """
    Updates ticket fields. Only send fields you want to change.
    Note: RESOLVED status requires a resolution note.
    """
    ticket = storage.get_by_id(ticket_id)
    if not ticket:
        raise exceptions.not_found(ticket_id)

    # can't resolve without explanation
    if (
        data.status == TicketStatus.RESOLVED
        and not data.resolution
        and not ticket.resolution
    ):
        raise exceptions.resolution_required()

    if data.title is not None:
        ticket.title = data.title
    if data.description is not None:
        ticket.description = data.description
    if data.status is not None:
        ticket.status = data.status
    if data.resolution is not None:
        ticket.resolution = data.resolution

    ticket.updated = datetime.now()
    return storage.save(ticket)


@router.delete("/{ticket_id}", status_code=204, summary="Delete ticket")
def delete_ticket(ticket_id: str):
    """Removes a ticket permanently."""
    if not storage.delete(ticket_id):
        raise exceptions.not_found(ticket_id)


@router.post("/{ticket_id}/comments", status_code=201, summary="Add comment")
def add_comment(
    ticket_id: str,
    text: str = Query(..., description="Comment text")
) -> Ticket:
    """Adds a comment to the ticket."""
    ticket = storage.get_by_id(ticket_id)
    if not ticket:
        raise exceptions.not_found(ticket_id)

    comment = Comment(id=str(uuid4()), text=text)
    ticket.comments.append(comment)
    ticket.updated = datetime.now()
    return storage.save(ticket)
