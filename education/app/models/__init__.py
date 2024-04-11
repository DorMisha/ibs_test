from typing import Union, List, Optional

from pydantic import BaseModel, validator, root_validator, conint, constr


class ConverterRequest(BaseModel):
    number: Union[int, str]


class ConverterResponse(BaseModel):
    arabic: int
    roman: str


class User(BaseModel):
    name: str
    age: conint(ge=0, le=100)
    adult: bool
    message: Optional[str] = ""
    
    @root_validator(skip_on_failure=True)
    def check_adult(cls, values):
        proof = values.get("age")
        if proof >= 18:
            values["adult"] = True
        return values

class Mapping(BaseModel):
    list_of_ids: List[Union[str, int]]
    tags: List[str]

class Meta(BaseModel):
    last_modification: constr(pattern=r'\d{2}/\d{2}/\d{4}')
    list_of_skills: Optional[List[str]] = None
    mapping: Mapping

    @validator('list_of_skills', pre=True, always=True)
    def set_default_skills(cls, v):
        return v if v is not None else []

    @validator('mapping', pre=True, always=True)
    def set_default_mapping(cls, v):
        return v if v is not None else Mapping()

class Mapping(BaseModel):
    list_of_ids: List[Union[str, int]]
    tags: List[str]

    @validator('list_of_ids', each_item=True)
    def check_list_of_ids(cls, v):
        if not isinstance(v, int) and not isinstance(v, str):
            raise ValueError('List of ids must contain only integers or strings')
        return v

    @validator('tags')
    def check_tags(cls, v):
        if '' in v:
            v = [tag for tag in v if tag != '']
        return v


class BigJson(BaseModel):
    """Использует модель User."""
    user: User
    meta: Meta


# class UserRequest(BaseModel):
#     name: str
#     message: str
#
#
# class User(BaseModel):
#     name: str
#     age: str
#     is_adult: bool
#     message: str = None
#
#
# class UserResponse(BaseModel):
#     pass
