from sqlalchemy.orm import Session

from app import models, schemas


def create_author(db: Session, author: schemas.AuthorBase) -> models.Author:
    """
    Create a new author in the database.

    Attributes:
        db (Session): The database session.
        author (schemas.AuthorBase): The author data to create.

    Returns:
        models.Author: The created author model with database-populated fields.
    """
    new_author = models.Author(**author.model_dump())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


def get_author_by_id(db: Session, author_id: int) -> models.Author | None:
    """
    Retrieve an author from the database by their ID.

    Attributes:
        db (Session): The database session.
        author_id (int): The ID of the author to retrieve.

    Returns:
        models.Author | None: The author model if found, None otherwise.
    """
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_authors_with_pagination(
    db: Session, page: int, per_page: int
) -> tuple[list, int, int]:
    """
    Retrieve a paginated list of authors from the database.

    Attributes:
        db (Session): The database session.
        page (int): The page number (1-based).
        per_page (int): Number of records per page.

    Returns: tuple[list, int, int]: A tuple containing:
        - List of Author models for the current page.
        - Total number of authors in the database.
        - Total number of pages.
    """
    query = db.query(models.Author)

    total_items = query.count()
    total_pages = (total_items + per_page - 1) // per_page

    offset = (page - 1) * per_page
    authors = query.offset(offset).limit(per_page).all()

    return authors, total_items, total_pages
