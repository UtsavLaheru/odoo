from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class User(Base):
    __tablename__ = "users"

    # Mapped and mapped_column provide better type hinting
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True, index=True)

class MaintenanceTeam(Base):
    __tablename__="Maintance Team Table"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)    
    team_name: Mapped[str] = mapped_column(unique=True, index=True)
    team_member_name: Mapped[str] = mapped_column()
    workflow_logic: Mapped[str] = mapped_column()
        