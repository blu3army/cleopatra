from datetime import date

import typer

from db.base import Base
from db.engine import engine
from db.models.payment import Payment
from db.services.payment_service import create_payment, get_payments
from db.session import SessionLocal

app = typer.Typer()
payment_app = typer.Typer()
app.add_typer(payment_app, name="payment")

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

@payment_app.command("add")
def cheque_add(
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






@payment_app.command("ls")
def cheque_list(
        dir: str = typer.Option(..., "--dir"),
        since: str | None = typer.Option(None, "--from"),
        until: str | None = typer.Option(None, "--to"),
        min_amount: int | None = typer.Option(None, "--min"),
        max_amount: int | None = typer.Option(None, "--max"),
        party: str | None = typer.Option(None, "--party"),
):

    with SessionLocal() as db:

        cheques = get_payments(db, {
            "dir": dir,
            "since": since,
            "until": until,
            "min_amount": min_amount,
            "max_amount": max_amount,
            "party": party,
        })

        for cheque in cheques:
            typer.echo(cheque)



if __name__ == "__main__":
    app()