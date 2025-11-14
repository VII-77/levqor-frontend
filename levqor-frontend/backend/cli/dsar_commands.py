"""
DSAR CLI Commands
Command-line interface for managing DSAR exports.

Run daily cleanup (via cron/scheduler):
  python -m backend.cli.dsar_commands cleanup
"""

import os
import json
import click
from datetime import datetime, timedelta, timezone

from run import app
from app import db
from backend.services.dsar_exporter import persist_dsar_export
from backend.models.dsar_request import DSARRequest
from backend.config import GDPR_DSAR_EXPORT_RETENTION_DAYS


@click.group()
def dsar():
    """DSAR-related CLI commands."""
    pass


@dsar.command("export")
@click.argument("reference_id")
def export(reference_id):
    """Generate DSAR ZIP for a given GDPR reference ID."""
    with app.app_context():
        result = persist_dsar_export(reference_id)
        click.echo(json.dumps(result, indent=2))


@dsar.command("cleanup")
def cleanup():
    """
    Delete old DSAR export ZIPs that are older than retention window.
    
    Retention policy:
    - Deletes ZIP files older than GDPR_DSAR_EXPORT_RETENTION_DAYS (default 30)
    - Only affects completed DSARs
    - Keeps database rows for audit purposes
    - Only deletes files that exist on disk
    
    This should be run daily via cron or scheduler.
    """
    with app.app_context():
        retention_days = GDPR_DSAR_EXPORT_RETENTION_DAYS
        cutoff = datetime.now(timezone.utc) - timedelta(days=retention_days)

        completed_dsars = DSARRequest.query.filter(
            DSARRequest.status == "completed"
        ).all()

        removed = 0
        checked = 0
        errors = 0

        for req in completed_dsars:
            checked += 1

            ts = req.completed_at or req.requested_at
            if not ts:
                continue

            if ts.replace(tzinfo=timezone.utc) > cutoff:
                continue

            export_root = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "backend", "exports", "dsar"
            )
            
            filename = f"levqor-dsar-{req.gdpr_reference_id}.zip"
            file_path = os.path.join(export_root, filename)

            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                    removed += 1
                    click.echo(f"Deleted: {filename} (age: {(datetime.now(timezone.utc) - ts.replace(tzinfo=timezone.utc)).days} days)")
                except OSError as e:
                    errors += 1
                    click.echo(f"Failed to delete {filename}: {e}", err=True)

        db.session.commit()

        click.echo(f"\n{'='*60}")
        click.echo(f"DSAR Cleanup Summary:")
        click.echo(f"  Checked: {checked} completed DSARs")
        click.echo(f"  Deleted: {removed} files")
        click.echo(f"  Errors: {errors}")
        click.echo(f"  Retention: {retention_days} days")
        click.echo(f"{'='*60}")


if __name__ == "__main__":
    dsar()
