from mbm.cli import pass_environment

import click


@click.command("purge", short_help="Purge server blocklists.")
@click.argument("path", required=False, type=click.Path(resolve_path=True))
@pass_environment
def cli(ctx, path):
    """Purge server blocklists."""
    ctx.log(f"This option is not yet implemented.")