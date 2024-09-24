from core.tools import GenCellName
from config import logger, BordersCache

from functools import lru_cache
from abc import ABC, abstractmethod
from typing import Any, Union, Dict

from openpyxl import load_workbook

class ExcelReader(ABC):
    def __init__(self, file: str):
        self._groups = dict()
        self.__workbook__ = load_workbook(file)
        self.__sheet__ = self.__workbook__.active
        counter: int = 3
        counter_down: int = 9
        while True:
            cell_name = GenCellName(counter)
            counter += 1
            group = self._GetRow(cell_name, counter_down).value
            
            if group is None:
                if self._DetectBorder(cell_name, counter_down):
                    break
                else:
                    counter_down += 1; counter = 3            
            else:
                group = group.strip().upper()
                if not group in ("ЧАСЫ", "ДНИ"):
                    self._groups[group] = cell_name
        logger.success(f"{self.__class__.__name__}: loaded {len(self.groups)} groups from {file}")

    def _GetRow(self, column: Union[str, int], row: int) -> Any:
        if isinstance(column, int):
            column = GenCellName(column)
        return self.__sheet__[f"{column}{row}"] 

    @abstractmethod
    @lru_cache(maxsize=BordersCache)
    def _DetectBorder(self, column: Union[str, int], row: int) -> bool:
            return True if not self._GetRow(column, row).border.bottom.style \
                                                 is None else False

    @property
    def groups(self) -> Dict[str, str]:
        return self._groups