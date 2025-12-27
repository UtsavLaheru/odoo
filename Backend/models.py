from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from datetime import date
from sqlalchemy import Date
from database import Base

class User(Base):
    __tablename__ = "user"

    # Mapped and mapped_column provide better type hinting
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(String(255),unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    


class MaintenanceTeam(Base):
    __tablename__="Maintance Team"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)    
    team_name: Mapped[str] = mapped_column(unique=True, index=True)
    team_member_name: Mapped[str] = mapped_column()
    workflow_logic: Mapped[str] = mapped_column()
    

class Equipment(Base):
    __tablename__ = "equipment"
    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    Equipment_name : Mapped[str] = mapped_column()
    Serial_Number : Mapped[str] = mapped_column(unique=True,index=True)
    Company : Mapped[str] = mapped_column(index=True)
    Purchase_Date : Mapped[date] = mapped_column(Date)
    Warranty_Info : Mapped[str] = mapped_column()
    Location : Mapped[str] = mapped_column()
    
