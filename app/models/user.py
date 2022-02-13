from datetime import datetime

from typing import NewType
from pydantic import BaseModel, constr

UserID = NewType("UserID", int)
FirstName = constr(max_length=20, strip_whitespace=True, to_lower=True)
Email = constr(max_length=20, strip_whitespace=True, to_lower=True)
Nationality = constr(max_length=20, to_lower=True)


class User(BaseModel):
    user_id: UserID
    first_name: FirstName
    email: Email
    nationality: Nationality
    created_at: datetime
    modified_at: datetime
