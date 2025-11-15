"""
Support Ticket Management
Creates and manages support tickets (JSON-based storage)
"""

import os
import json
import logging
from datetime import datetime
from uuid import uuid4

logger = logging.getLogger(__name__)

TICKETS_FILE = "data/support_tickets.json"


def _ensure_data_dir():
    """Ensure data directory exists"""
    os.makedirs("data", exist_ok=True)


def _load_tickets():
    """Load all tickets from JSON file"""
    _ensure_data_dir()
    
    if not os.path.exists(TICKETS_FILE):
        return []
    
    try:
        with open(TICKETS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"support_tickets.load_error error={str(e)}")
        return []


def _save_tickets(tickets):
    """Save tickets to JSON file"""
    _ensure_data_dir()
    
    try:
        with open(TICKETS_FILE, 'w') as f:
            json.dump(tickets, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"support_tickets.save_error error={str(e)}")
        return False


def create_ticket(email, message, context=None):
    """
    Create a new support ticket
    
    Args:
        email: Customer email
        message: Support message/issue
        context: Optional dict with additional context
    
    Returns:
        dict: Created ticket object with id
    """
    tickets = _load_tickets()
    
    ticket = {
        "id": str(uuid4())[:8],  # Short ID like "a1b2c3d4"
        "email": email,
        "message": message,
        "context": context or {},
        "status": "open",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "assigned_to": None,
        "notes": []
    }
    
    tickets.append(ticket)
    
    if _save_tickets(tickets):
        logger.info(f"support_tickets.created id={ticket['id']} email={email}")
        return ticket
    else:
        logger.error(f"support_tickets.create_failed email={email}")
        return None


def list_tickets(limit=50, status=None):
    """
    List recent support tickets
    
    Args:
        limit: Maximum number of tickets to return
        status: Filter by status ('open', 'closed', None for all)
    
    Returns:
        list: List of ticket dicts
    """
    tickets = _load_tickets()
    
    # Filter by status if specified
    if status:
        tickets = [t for t in tickets if t.get("status") == status]
    
    # Sort by created_at descending (newest first)
    tickets.sort(key=lambda t: t.get("created_at", ""), reverse=True)
    
    # Limit results
    return tickets[:limit]


def get_ticket(ticket_id):
    """
    Get a specific ticket by ID
    
    Args:
        ticket_id: Ticket ID
    
    Returns:
        dict: Ticket object or None
    """
    tickets = _load_tickets()
    
    for ticket in tickets:
        if ticket.get("id") == ticket_id:
            return ticket
    
    return None


def update_ticket(ticket_id, updates):
    """
    Update a ticket
    
    Args:
        ticket_id: Ticket ID
        updates: Dict with fields to update
    
    Returns:
        dict: Updated ticket or None
    """
    tickets = _load_tickets()
    
    for i, ticket in enumerate(tickets):
        if ticket.get("id") == ticket_id:
            ticket.update(updates)
            ticket["updated_at"] = datetime.utcnow().isoformat()
            tickets[i] = ticket
            
            if _save_tickets(tickets):
                logger.info(f"support_tickets.updated id={ticket_id}")
                return ticket
            break
    
    return None


def close_ticket(ticket_id, resolution=None):
    """
    Close a ticket
    
    Args:
        ticket_id: Ticket ID
        resolution: Optional resolution note
    
    Returns:
        dict: Updated ticket or None
    """
    updates = {"status": "closed"}
    
    if resolution:
        updates["resolution"] = resolution
    
    return update_ticket(ticket_id, updates)


def add_ticket_note(ticket_id, note, author="system"):
    """
    Add a note to a ticket
    
    Args:
        ticket_id: Ticket ID
        note: Note text
        author: Who added the note
    
    Returns:
        bool: Success status
    """
    ticket = get_ticket(ticket_id)
    
    if not ticket:
        return False
    
    note_entry = {
        "author": author,
        "note": note,
        "created_at": datetime.utcnow().isoformat()
    }
    
    if "notes" not in ticket:
        ticket["notes"] = []
    
    ticket["notes"].append(note_entry)
    
    updated = update_ticket(ticket_id, {"notes": ticket["notes"]})
    return updated is not None


def get_ticket_stats():
    """
    Get ticket statistics
    
    Returns:
        dict: Stats including total, open, closed counts
    """
    tickets = _load_tickets()
    
    stats = {
        "total": len(tickets),
        "open": len([t for t in tickets if t.get("status") == "open"]),
        "closed": len([t for t in tickets if t.get("status") == "closed"]),
        "avg_response_time_hours": 0  # TODO: Calculate if we track response times
    }
    
    return stats
