from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


if TYPE_CHECKING:
    from app.models.school_class import SchoolClassModel


class TeacherModel(Base):

    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    first_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    last_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    staff_code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        index=True,
        nullable=False
    )

    classes: Mapped[list["SchoolClassModel"]] = relationship(
        back_populates="teacher"
    )