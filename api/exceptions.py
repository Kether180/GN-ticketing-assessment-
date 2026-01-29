from fastapi import HTTPException


def not_found(ticket_id: str) -> HTTPException:
    return HTTPException(
        status_code=404,
        detail={"error": "not_found", "message": f"Ticket '{ticket_id}' not_found"},
    )


def invalid_status(status: str) -> HTTPException:
    return HTTPException(
        status_code=422,
        detail={
            "error": "invalid_status",
            "message": f"Status '{status}' is not valid",
            "valid_options": ["OPEN", "RESOLVED", "CLOSED"],
        },
    )


def resolution_required() -> HTTPException:
    return HTTPException(
        status_code=422,
        detail={
            "error": "resolution_required",
            "message": "Resolution notes are required when setting status to RESOLVED",
        },
    )
