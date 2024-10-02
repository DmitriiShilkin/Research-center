from constants.crud_types import CreateSchemaType, ModelType, UpdateSchemaType
from crud.crud_mixins import (
    BaseCRUD,
    CreateAsync,
    ReadAsync,
    UpdateAsync,
    DeleteAsync,
)


class BaseAsyncCRUD(
    BaseCRUD[ModelType],
    CreateAsync[ModelType, CreateSchemaType],
    ReadAsync[ModelType],
    UpdateAsync[ModelType, UpdateSchemaType],
    DeleteAsync[ModelType],

):
    """
    CRUD object with default methods to Create, Read, Update, Delete
    **Parameters**
    * `model`: A SQLAlchemy model class
    * `schema`: A Pydantic model (schema) class
    """

    ...
