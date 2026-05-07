from pydantic import BaseModel


class LocationSchema(BaseModel):
    id: int
    name: str 
    address: str 
    city: str
    lat: float | None = None
    lon: float | None = None
    venue_type: int 
    surface_type: int

    @classmethod
    def from_location(cls, location):
        return cls(
            id=location.id,
            name=location.name,
            address=location.address,
            city=location.city,
            lat=location.latitude,
            lon=location.longitude,
            venue_type=location.venue_type,
            surface_type=location.surface_type,
        )
    

class LocationShortSchema(BaseModel):
    id: int
    name: str
    address: str | None = None

    @classmethod
    def from_location(cls, location):
        return cls(
            id=location.id,
            name=location.name,
            address=location.address,
        )