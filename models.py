from sqlmodel import Field, SQLModel, Relationship


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
    user_id: int | None = Field(foreign_key="user.id")


class Property(PropertyBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user: "User" = Relationship(back_populates="properties")


# -------------------------------------------------------------------------------------------------#


class UserBase(SQLModel):
    name: str
    email: str
    phone: str
    password: str
    role: str


class UserCreate(UserBase):
    properties: list[PropertyBase] | None = None


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    phone: str = Field(index=True, unique=True)
    properties: list[Property] = Relationship(back_populates="user")


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
