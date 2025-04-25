from sqlalchemy import (
    Column, Integer, String, Float, Table, ForeignKey
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

stop_route = Table(
    'stop_route',
    Base.metadata,
    Column('stop_id', ForeignKey('stops.id'), primary_key=True),
    Column('route_id', ForeignKey('routes.id'), primary_key=True)
)


class Stop(Base):
    """Model for a stop."""
    __tablename__ = "stops"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    routes = relationship(
        "Route",
        secondary=stop_route,
        back_populates="stops",
        cascade="all"
    )


class Route(Base):
    """Model for a transport route."""
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    transport_type = Column(String(50), nullable=False)

    stops = relationship(
        "Stop",
        secondary=stop_route,
        back_populates="routes"
    )
