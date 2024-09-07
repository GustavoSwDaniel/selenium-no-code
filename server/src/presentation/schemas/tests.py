from typing import List, Optional
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import List
from enum import Enum

class type(str, Enum):
    CLASS_NAME = 'class_name'
    ID = 'id'
    NAME = 'name'
    XPATH = 'xpath'
    CSS_SELECTOR = 'css_selector'
    TAG_NAME = 'tag_name'
    LINK_TEXT = 'link_text'
    PARTIAL_LINK_TEXT = 'partial_link_text'

class ValidationField(BaseModel): 
    message: str = None

class Steps(BaseModel):
    type: str
    element: str
    value: str
    validations_field: Optional[ValidationField] = None
    action_type: str


    @field_validator('type')
    def convert_to_enum_name(cls, v):
        try:
            return type(v).name
        except ValueError:
            raise ValueError(f"Invalid selector type: {v}")

class Cases(BaseModel):
    name: str
    steps: List[Steps]


class Test(BaseModel):
    url: str
    cases: List[Cases]


class ImageTestResponseSchema(BaseModel):
    url: str


class TestReponseSchema(BaseModel):
    id: int
    url: str
    case_name: str
    status: str
    message: Optional[str]
    note: Optional[str]
    image_tests: List[ImageTestResponseSchema]


class PaginateTestReponseSchema(BaseModel):
    total: int
    offset: int
    count: int
    data: List[TestReponseSchema]