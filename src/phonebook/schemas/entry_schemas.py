from typing import Optional

from pydantic import BaseModel, Field


class EntryBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    organization: Optional[str]
    work_phone: Optional[str]
    personal_phone: Optional[str]


class Entry(EntryBase):
    entry_id: Optional[int] = Field(primary_key=True)

    def to_dict(self):
        return {
            self.entry_id: {
                "first_name": self.first_name,
                "last_name": self.last_name,
                "middle_name": self.middle_name,
                "organization": self.organization,
                "work_phone": self.work_phone,
                "personal_phone": self.personal_phone
            }
        }


class EntryCreate(EntryBase):
    pass
