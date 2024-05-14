from sqlmodel import select
from src.db.models import Property, Service
from src.db.main import get_session


async def get_client_services(session, id: int):
    result = await session.execute(select(Property.client_services).where(Property.user_id == id))
    if result is None:
        return 'Client services not found'

    rows = result.all()
    if rows is None:
        return 'No client services found'

    client_services = [dict(row) for row in rows]
    print('client_services', client_services)
    return client_services
