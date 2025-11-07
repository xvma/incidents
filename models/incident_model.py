from datetime import datetime
from enum import Enum

# __________________________________________________________________________

class IncidentField(Enum):
    ID = "id"
    DESCRIPTION = "description"
    TYPE = "type"
    STATUS = "status"
    SOURCE = "source"
    CREATEDAT = "created_at"
# __________________________________________________________________________

class IncidentType(Enum):
    ORDINARY = "ordinary"
    IMPORTANT = "important"
    EXCLUSIVE = "exclusive"
    CRITICAL = "critical"
# __________________________________________________________________________

class IncidentStatus(Enum):
    NEW = "new"
    ONGOING = "ongoing"
    RESOLVED = "resolved"
    CLOSED = "closed"
# __________________________________________________________________________

class IncidentSource(Enum):
    OPERATOR = "operator"
    MONITORING = "monitoring"
    PARTNER = "partner"
# __________________________________________________________________________

class Incident:
    def __init__(self, id=None, description="", type=IncidentType.ORDINARY, status=IncidentStatus.NEW, source=IncidentSource.OPERATOR, created_at=None):
        self.id = id
        self.description = description
        self.type = type if isinstance(type, IncidentType) else IncidentType(type)
        self.status = status if isinstance(status, IncidentStatus) else IncidentStatus(status)
        self.source = source if isinstance(source, IncidentSource) else IncidentSource(source)
        self.created_at = created_at or datetime.utcnow().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "type": self.type.value,
            "status": self.status.value,
            "source": self.source.value,
            "created_at": self.created_at
        }

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row[0],
            description=row[1],
            type=IncidentType(row[2]),
            status=IncidentStatus(row[3]),
            source=IncidentSource(row[4]),
            created_at=row[5]
        )

    @classmethod
    def from_dict(cls, dict):
        return cls(
            id=dict[IncidentField.ID.value] if IncidentField.ID.value in dict else None,
            description=dict[IncidentField.DESCRIPTION.value] if IncidentField.DESCRIPTION.value in dict else "",
            type=dict[IncidentField.TYPE.value] if IncidentField.TYPE.value in dict else IncidentType.ORDINARY,
            status=dict[IncidentField.STATUS.value] if IncidentField.STATUS.value in dict else IncidentStatus.NEW,
            source=dict[IncidentField.SOURCE.value] if IncidentField.SOURCE.value in dict else IncidentSource.OPERATOR,
            created_at=dict[IncidentField.CREATEDAT.value] if IncidentField.CREATEDAT.value in dict else None,
        )

