from web.web import SocketRoute, dispatcher
from core.models import WeekSearch
from core.tools import GetWeek

from typing import Dict

@SocketRoute.on_message(target="WeekSearch")
async def handle_get_week(message: Dict[str, str], params: WeekSearch) -> str:
    return dispatcher.generate_answer(result = GetWeek(
        day = params.day,
        month = params.month,
        year = params.year
    ))