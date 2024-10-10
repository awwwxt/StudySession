from core.models.reader import ExcelReader
from core.akvt.akvt import Parser
from config import (
    TIMETABLES, 
    HTTP_TIMEOUT, 
    NAMES_TIMETABLE_SOURCE, 
    logger
)
from core.errors import ClientError
from core.tools import GenCellName

from openpyxl import Workbook
from openpyxl.styles import Border
from xls2xlsx import XLS2XLSX

from re import sub
from typing import Any, List 
from concurrent.futures import ThreadPoolExecutor
from os import rename, remove

class Reader(ExcelReader):
    def __init__(self, path):
        super().__init__(path)
        logger.info(f"Reading data from {path}")

    def _DetectBorder(self, *args: Any, **kwargs: Any) -> None:
        ...

class Updater:
    def __init__(self):
        self.merged_wb = Workbook()
        self.merged_ws = self.merged_wb.active
    
    async def start(self) -> bool:
        parser = Parser(timeout = HTTP_TIMEOUT)
        try:
            filenames = await parser.get()
        except ClientError:
            return False
        if filenames:
            with ThreadPoolExecutor(max_workers = len(filenames)) as executor:
                for file in filenames:
                    executor.submit(XLS2XLSX(file).to_xlsx, f"{file}x")
        else:
            return False
        files: List[Reader] = [Reader(f'{file}x') for file in filenames]
        for i in range(len(NAMES_TIMETABLE_SOURCE.keys())):
            start_from = 0
            if i == 1:
                start_from = len(files[0].groups) + 3
            elif i == 2:
                start_from = len(files[1].groups) + len(files[0].groups) + 6
            self.copy_sheet(files[i].__sheet__, start_from)

        self.update_names()
        self.merged_wb.save(f"{TIMETABLES}lessons.xlsx")
        return True
    
    def copy_sheet(self, sheet, start_from: int) -> None:
        for row in sheet.iter_rows():
            for cell in row:
                new_cell = self.merged_ws[f'{GenCellName(start_from + cell.column)}{cell.row}']
                new_cell.value = sub(r'\s+', ' ', cell.value) if not cell.value is None else None
                if cell.border:
                    border = Border( 
                        left=cell.border.left, 
                        right=cell.border.right, 
                        top=cell.border.top, 
                        bottom=cell.border.bottom
                )
                    new_cell.border = border
    
    @staticmethod
    def update_names() -> None:
        remove(f"{TIMETABLES}lessons-old.xlsx")
        rename(f"{TIMETABLES}lessons.xlsx", f"{TIMETABLES}lessons-old.xlsx")
