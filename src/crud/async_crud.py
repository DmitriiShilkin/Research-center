from constants.crud_types import CreateSchemaType, ModelType, UpdateSchemaType
from crud.crud_mixins import (
    BaseCRUD,
    CreateAsync,
    ReadAsync,
    UpdateAsync,
)


class BaseAsyncCRUD(
    BaseCRUD[ModelType],
    CreateAsync[ModelType, CreateSchemaType],
    ReadAsync[ModelType],
    UpdateAsync[ModelType, UpdateSchemaType],
):
    """
    CRUD object with default methods to Create, Read, Update
    **Parameters**
    * `model`: A SQLAlchemy model class
    * `schema`: A Pydantic model (schema) class
    """

    ...
