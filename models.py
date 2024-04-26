from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr
from enum import Enum

# -------------------------------------------------------------------------------------------------#


class Roles(str, Enum):
    admin = "admin"
    user = "user"


# -------------------------------------------------------------------------------------------------#


class Token(SQLModel):
    access_token: str | None
    refresh_token: str | None


# -------------------------------------------------------------------------------------------------#


class ServiceBase(SQLModel):
    date: str
    name: str
    company_id: int = Field(default=None, foreign_key="company.id")
    service_type: str
    scrapping_type: str
    scrapping_config: str


class Service(ServiceBase, table=True):
    id: int = Field(default=None, primary_key=True)


# -------------------------------------------------------------------------------------------------#


class PropertyBase(SQLModel):
    created_at: str
    property_type: str

    user_id: int | None = Field(default=None, foreign_key="user.id")


class Property(PropertyBase, table=True):
    id: int = Field(default=None, primary_key=True)

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


class UserWithProperties(UserBase):
    properties: list[Property] = []


# -------------------------------------------------------------------------------------------------#


class CompanyBase(SQLModel):
    created_at: str
    name: str
    service_type: str


class Company(CompanyBase, table=True):
    id: int = Field(default=None, primary_key=True)


# -------------------------------------------------------------------------------------------------#


class ProviderClientBase(SQLModel):
    client_code: str
    service_id: int = Field(foreign_key="service.id")
    user_id: int = Field(foreign_key="user.id")


class ProviderClient(ProviderClientBase, table=True):
    id: int = Field(default=None, primary_key=True)


# -------------------------------------------------------------------------------------------------#


class ScrappedDataBase(SQLModel):
    date: str
    bills: str
    consumption_data: str
    provider_client_id: int = Field(foreign_key="providerclient.id")


class ScrappedData(ScrappedDataBase, table=True):
    id: int = Field(default=None, primary_key=True)


# -------------------------------------------------------------------------------------------------#
