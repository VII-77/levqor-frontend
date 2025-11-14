"""
DSAR CLI Commands
Command-line interface for managing DSAR exports.
"""

import click
from run import app
from backend.services.dsar_exporter import persist_dsar_export


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


if __name__ == "__main__":
    import json
    dsar()
