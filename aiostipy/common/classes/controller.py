from abc import ABC
from typing import List, Optional


class Controller(ABC):

    prefix: Optional[str] = "/"
    tags: Optional[List[str]] = None
