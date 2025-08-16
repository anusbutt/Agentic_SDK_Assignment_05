from agents import function_tool, RunContextWrapper
from pydantic import BaseModel

class UserContext(BaseModel):
    name: str
    member_id: int | None

BOOK_DB = {
    "1984": 3,
    "Brave New World": 2,
    "Fahrenheit 451": 0,
    "The Great Gatsby": 5
}

@function_tool
def search_book( wrapper: RunContextWrapper[UserContext], title: str):
    if title in BOOK_DB:
        return f"✅ '{title}' is in the library"
    return f"'{title}' is not in the collection"

@function_tool
def check_availability(wrapper: RunContextWrapper[UserContext], title: str):
    user = wrapper.context
    if not user.member_id:
        return f"❌ you must be a registered member to check availability"
    if title not in BOOK_DB:
        return f"'{title}' is not in the collection"
    copies = BOOK_DB[title]
    return f"'{title}' has '{copies}' copies." if copies > 0 else f"'{title}' is out of stock"