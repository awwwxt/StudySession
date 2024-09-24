from core.tools import DrawPNG, GetMarkdown

from typing import Union, Optional, Dict, Any
from abc import ABC, abstractmethod

class BaseBuilder(ABC):
    MARKDOWN_TEMPLATE = '`{}`'

    def __init__(self, data: Dict[Union[int, str], Any], user_id: Optional[int] = None):
        for key, value in data.items():
            self.__setattr__(key, value)
        self.user_id = user_id
        
    @abstractmethod
    def _toText(self) -> None:
        ...        

    def toMarkDown(self) -> str:
        return self.MARKDOWN_TEMPLATE.format(GetMarkdown(self._toText()))

    async def toBytes(self) -> bytes:
        return await DrawPNG(self._toText(), self.user_id) 