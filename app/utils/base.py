from datetime import datetime
from typing import Annotated

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import mapped_column

int_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
created_at = Annotated[datetime, mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)]
updated_at = Annotated[
    datetime, mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]
