
from typing import Any, Dict, Generic, TypeVar
from urllib.request import Request

T = TypeVar("T")

class NetworkRequestResponse(Generic[T]):
    def request(self) -> Request:
        raise Exception
    
    def decode(self, json: Dict[str, Any]) -> T:
        raise Exception()