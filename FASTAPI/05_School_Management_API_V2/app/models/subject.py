from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SubjectModel(Base):

    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        index=True,
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )