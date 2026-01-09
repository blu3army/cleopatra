from datetime import date

import typer

from db.base import Base
from db.engine import engine
from db.models.payment import Payment
from db.repositories.payment_repo import list_payments
from db.services.payment_service import create_payment, delete_payment
from db.session import SessionLocal

app = typer.Typer()
payment_app = typer.Typer()
app.add_typer(payment_app, name="payment")

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

@payment_app.command("add")
def payment_add_cmd(
        dir: str = typer.Option(..., "--dir"),
        ref: str = typer.Option(..., "--ref"),
        amount: int = typer.Option(..., "--amount"),
        due: str = typer.Option(..., "--due", help="YYYY-MM-DD"),
        party: str = typer.Option(..., "--party"),
        type: str = typer.Option(..., "--type"),
):


    if dir not in ["in", "out"]:
        typer.echo("Invalid dir")
        raise typer.Exit()

    try:
        with SessionLocal() as db:
            new_cheque = create_payment(db, {
                "dir": dir, "ref": ref, "amount": amount, "party": party, "due": due, "type": type
            })

    except Exception as err:
        db.rollback()
        raise err


@payment_app.command("rm")
def payment_delete_cmd(
        id: int = typer.Option(None, "--id"),
        ref: str = typer.Option(None, "--ref"),
):

    if (id is None and ref is None) or (id is not None and ref is not None):
        typer.echo("Invalid id/ref, you have to define --id or --ref")
        raise typer.Exit()

    with SessionLocal() as db:
        result = delete_payment(db=db, id=id)
        typer.echo(result)



@payment_app.command("ls")
def payment_list_cmd(
        dir: str = typer.Option(..., "--dir"),
        since: str | None = typer.Option(None, "--from"),
        until: str | None = typer.Option(None, "--to"),
        min_amount: int | None = typer.Option(None, "--min"),
        max_amount: int | None = typer.Option(None, "--max"),
        party: str | None = typer.Option(None, "--party"),
):

    with SessionLocal() as db:

        payments = list_payments(db, {
            "dir": dir,
            "since": since,
            "until": until,
            "min_amount": min_amount,
            "max_amount": max_amount,
            "party": party,
        })

        for payment in payments:
            typer.echo(payment)



if __name__ == "__main__":
    app()