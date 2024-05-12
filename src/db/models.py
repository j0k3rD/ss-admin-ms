from sqlmodel import Field, SQLModel, Relationship, Column
import sqlalchemy.dialects.postgresql as pg
from pydantic import EmailStr
from enum import Enum
from typing import Dict
from datetime import datetime

# -------------------------------------------------------------------------------------------------#


class Roles(str, Enum):
    admin = "admin"
    user = "user"


# -------------------------------------------------------------------------------------------------#


class Token(SQLModel):
    access_token: str | None
    refresh_token: str | None


# -------------------------------------------------------------------------------------------------#

class ServiceType(str, Enum):
    INTERNET = 'internet'
    AGUA = 'agua'
    LUZ = 'luz'
    GAS = 'gas'
    OTRO = 'otro'


class ServiceBase(SQLModel):
    company_name: str
    service_type: ServiceType | None
    scrapping_type: str
    

class Service(ServiceBase, table=True):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    scrapping_config: Dict = Field(default_factory=dict, sa_column=Column(pg.JSONB))
    crontab: Dict = Field(default_factory=dict, sa_column=Column(pg.JSONB))
    schedule: Dict = Field(default_factory=dict, sa_column=Column(pg.JSONB))
    providers_client: list["ProviderClient"] = Relationship(back_populates="service")

    def to_dict(self):
        return {
            "id": self.id,
            "company_name": self.company_name,
            "service_type": self.service_type,
            "scrapping_type": self.scrapping_type,
            "scrapping_config": self.scrapping_config,
            "crontab": self.crontab,
            "schedule": self.schedule
        }
    
    class Config:
        arbitrary_types_allowed = True

# -------------------------------------------------------------------------------------------------#


class PropertyBase(SQLModel):
    property_type: str

    user_id: int | None = Field(default=None, foreign_key="user.id")


class Property(PropertyBase, table=True):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)

    user: "User" = Relationship(back_populates="properties")


class PropertyWithUser(PropertyBase):
    user: "User" = None


# -------------------------------------------------------------------------------------------------#


class UserBase(SQLModel):
    name: str
    email: EmailStr
    phone: str
    password: str
    role: Roles = Field(default="user")
    disabled: bool | None = None


class UserCreate(UserBase):
    properties: list[PropertyBase] | None = None


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    phone: str = Field(index=True, unique=True)

    properties: list["Property"] = Relationship(back_populates="user")
    providers_client: list["ProviderClient"] = Relationship(back_populates="user")


class UserWithProperties(UserBase):
    properties: list[PropertyWithUser] | None = None


# -------------------------------------------------------------------------------------------------#


class ScrappedDataBase(SQLModel):
    provider_client_id: int | None = Field(default=None, foreign_key="providerclient.id", nullable=True)


class ScrappedData(ScrappedDataBase, table=True):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    bills: Dict = Field(default_factory=dict, sa_column=Column(pg.JSONB))
    consumption_data: Dict = Field(default_factory=dict, sa_column=Column(pg.JSONB))

    provider_client: "ProviderClient" = Relationship(back_populates="scrapped_datas")
    

# -------------------------------------------------------------------------------------------------#


class ProviderClientBase(SQLModel):
    client_code: str

    service_id: int = Field(foreign_key="service.id")
    user_id: int = Field(foreign_key="user.id")


class ProviderClient(ProviderClientBase, table=True):
    id: int = Field(default=None, primary_key=True)

    user: "User" = Relationship(back_populates="providers_client")
    service: "Service" = Relationship(back_populates="providers_client")
    scrapped_datas: list["ScrappedData"] = Relationship(back_populates="provider_client")
    

    def to_dict(self):
        return {
            "id": self.id,
            "client_code": self.client_code,
            "service_id": self.service_id,
            "user_id": self.user_id
        }
    

# -------------------------------------------------------------------------------------------------#
