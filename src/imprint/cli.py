from __future__ import annotations

import typer

app = typer.Typer(help="Imprint identity and expression profile compiler.")


@app.command()
def version() -> None:
    """Print the Imprint version."""
    from imprint import __version__

    typer.echo(__version__)
