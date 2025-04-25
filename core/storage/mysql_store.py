from contextlib import contextmanager
from typing import List, Dict, Tuple, Type

from sqlalchemy import delete, text
from sqlalchemy.orm import Session

from storage.base import Store
from storage.db import SessionLocal, init_db
from storage.models import Stop, Route, stop_route


@contextmanager
def session_scope():
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class MySQLStore(Store):
    def __init__(self):
        init_db()

    def save(self, stops: List[Dict]) -> None:
        """
        Atomically delete all stops/routes and re-insert fresh data.
        Resets auto-increment IDs after deletion.
        """
        with session_scope() as session:
            print(f"Deleting the previous data...")
            session.execute(delete(stop_route))
            session.query(Stop).delete(synchronize_session=False)
            session.query(Route).delete(synchronize_session=False)

            session.execute(text("ALTER TABLE stops AUTO_INCREMENT = 1"))
            session.execute(text("ALTER TABLE routes AUTO_INCREMENT = 1"))
            print(f"Successfully deleted previous data.")

            print(f"Starting insertion of {len(stops)} new stops...")
            route_cache: Dict[Tuple[str, str], Type[Route] | Route] = {}

            for stop in stops:
                stop_obj = Stop(
                    title=stop["title"],
                    latitude=stop["latitude"],
                    longitude=stop["longitude"],
                )

                for route in stop["routes"]:
                    key = (route["name"], route["transport_type"])
                    if key not in route_cache:
                        existing = (
                            session.query(Route)
                            .filter_by(name=key[0], transport_type=key[1])
                            .one_or_none()
                        )
                        if existing:
                            route_cache[key] = existing
                        else:
                            route_cache[key] = Route(name=key[0], transport_type=key[1])
                            session.add(route_cache[key])

                    stop_obj.routes.append(route_cache[key])

                session.add(stop_obj)

            print(f"All new records prepared for insertion")
