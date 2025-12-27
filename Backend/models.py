from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, Boolean, Date, Float,DateTime
from database import Base
from datetime import date, datetime

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(String(255),unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    

    
class EquipmentCategory(Base):
    __tablename__ = "equipment_category"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True) 


class Equipment(Base):
    __tablename__ = "equipment"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    Serial_number: Mapped[str] = mapped_column(unique=True) 
    category_id: Mapped[int] = mapped_column(ForeignKey("equipment_category.id"))
    Company : Mapped[str] = mapped_column(index=True)
    Used_by:Mapped[str] = mapped_column(index=True)
    department: Mapped[str] = mapped_column() 
    Location: Mapped[str] = mapped_column() 
    technician_id: Mapped[int] = mapped_column(ForeignKey("user.id")) 
    Equipment_name : Mapped[str] = mapped_column()
    Purchase_Date : Mapped[date] = mapped_column(Date)
    Assigned_Date : Mapped[date] = mapped_column(Date)
    Warranty_Info : Mapped[str] = mapped_column()
    is_usable: Mapped[bool] = mapped_column(default=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("maintenance_team.id"))
    Description: Mapped[str] = mapped_column()

class MaintenanceTeam(Base):
    __tablename__ = "maintenance_team" 
    id: Mapped[int] = mapped_column(primary_key=True, index=True)    
    team_name: Mapped[str] = mapped_column(unique=True, index=True)
    team_member_name: Mapped[str] = mapped_column()
    workflow_logic: Mapped[str] = mapped_column()

#Test
class RequestForm(Base):
    __tablename__="requestform"
    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    Created_By : Mapped[str] = mapped_column(index=True)
    Maintenance_For : Mapped[str] = mapped_column()     
    Equipment : Mapped[str] = mapped_column()          
    Category : Mapped[str] = mapped_column()
    Request_Date : Mapped[date] = mapped_column(Date)
    Maintenance_Type : Mapped[str] = mapped_column()     
    Team : Mapped[str] = mapped_column()
    Technician : Mapped[str] = mapped_column()
    Scheduled_Date : Mapped[datetime] = mapped_column(DateTime)
    Duration : Mapped[datetime] = mapped_column(DateTime)
    Priority : Mapped[int] = mapped_column()
    Company : Mapped[str] = mapped_column()
    
    Current_Status : Mapped[str] = mapped_column()      
    Notes : Mapped[str] = mapped_column()
    Instruction : Mapped[str] = mapped_column()
    

