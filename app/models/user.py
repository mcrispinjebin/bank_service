from datetime import datetime

from typing import NewType
from pydantic import BaseModel, constr

UserID = NewType("UserID", str)
FirstName = constr(max_length=30, strip_whitespace=True, to_lower=True)
Email = constr(max_length=30, strip_whitespace=True, to_lower=True,
               regex="^[a-zA-Z0-9]+([\-\.\_+]*[\w])*\@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,4}[\.]?$")
Nationality = constr(max_length=20, to_lower=True)


class User(BaseModel):
    user_id: UserID
    first_name: FirstName
    email: Email
    nationality: Nationality
    created_at: datetime
    modified_at: datetime
