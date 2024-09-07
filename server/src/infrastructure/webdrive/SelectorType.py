from enum import Enum
from selenium.webdriver.common.by import By

class SelectorType(str, Enum):
    CLASS_NAME = By.CLASS_NAME
    ID = By.ID
    NAME = By.NAME
    XPATH = By.XPATH
    CSS_SELECTOR = By.CSS_SELECTOR
    TAG_NAME = By.TAG_NAME
    LINK_TEXT = By.LINK_TEXT
    PARTIAL_LINK_TEXT = By.PARTIAL_LINK_TEXT
