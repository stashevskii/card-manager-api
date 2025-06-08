import typer
from src.app.models import User
from src.app.core.db import get_db
from src.app.core.utils import hash_password, UserRole

cli = typer.Typer()


@cli.command()
def create_admin(username: str, password: str):
    db = get_db()
    try:
        admin = User(
            username=username,
            email="admin@example.com",
            password=hash_password(password),
            role=UserRole.ADMIN
        )
        db.add(admin)
        db.commit()
        print(f"Admin user created successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error creating admin: {e}")


if __name__ == "__main__":
    cli()
