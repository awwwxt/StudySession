from core.models.reader import ExcelReader
from core.akvt.akvt import Parser
from config import TIMETABLES, HTTP_TIMEOUT, MAX_ATTEMPS
from core.tools import xls2xlsx, GenCellName

from openpyxl import Workbook
from openpyxl.styles import Border

from typing import Any, List
from concurrent.futures import ThreadPoolExecutor
from os import rename, remove

class Updater(ExcelReader):
    def __init__(self, path):
        super().__init__(path)
    
    def _DetectBorder(self, *args: Any, **kwargs: Any) -> None:
        ...

async def reupdate() -> None:
    parser = Parser(timeout = HTTP_TIMEOUT)
    for _ in range(MAX_ATTEMPS):
        filenames = await parser.get()
        if filenames:
            with ThreadPoolExecutor(max_workers = 3) as executor:
                for file in filenames:
                    executor.submit(xls2xlsx(file).convert)

            merged_wb = Workbook()
            merged_ws = merged_wb.active

            files: List[Updater] = [Updater(f'{file}x') for file in filenames]

            def copy_sheet(sheet, from_: int) -> None:
                for row in sheet.iter_rows():
                    for cell in row:
                        new_cell = merged_ws[f'{GenCellName(from_ + cell.column)}{cell.row}']
                        new_cell.value = cell.value
                        if cell.border:
                            border: Border = Border( 
                                left=cell.border.left, 
                                right=cell.border.right, 
                                top=cell.border.top, 
                                bottom=cell.border.bottom
                            )
                            new_cell.border = border
                
            for i in range(3):
                from_ = 0
                if i == 1:
                    from_ = len(files[0].groups)   
                elif i == 2:
                    from_ = len(files[1].groups) + len(files[0].groups)  
                copy_sheet(files[i].__sheet__, from_)

            remove(f"{TIMETABLES}lessons-old.xlsx")
            rename(f"{TIMETABLES}lessons.xlsx", f"{TIMETABLES}lessons-old.xlsx")
            merged_wb.save(f"{TIMETABLES}lessons.xlsx")
            return True
        return False