from datetime import date

import typer

app = typer.Typer()
cheque_app = typer.Typer()
app.add_typer(cheque_app, name="cheque")


@cheque_app.command("add")
def cheque_add(
        dir: str = typer.Option(..., "--dir"),
        amount: int = typer.Option(..., "--amount"),
        due: str = typer.Option(..., "--due", help="YYYY-MM-DD"),
        party: str = typer.Option(..., "--party"),
):

    if dir not in ["in", "out"]:
        typer.echo("Invalid dir")
        raise typer.Exit()

    print(f"dir: {dir}")
    print(f"amount: {amount}")
    print(f"due: {due}")
    print(f"party: {party}")

    typer.echo("Cheque added")


if __name__ == "__main__":
    app()