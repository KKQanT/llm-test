from typing_extensions import Annotated, TypedDict
from typing import List, Dict, Any
from langchain_core.messages import BaseMessage

def merge_lists(left: List, right: List) -> List:
    if left is None:
        left = []
    if right is None:
        right = []
    return left + right

def override_state(left, right):
    if right is None:
        return left
    return right

def merge_cache(left: Dict, right: Dict) -> Dict:
    if left is None:
        left = {}
    if right is None:
        right = {}
    return {**left, **right}

class MarketAnalysisState(TypedDict):
    messages: Annotated[List[BaseMessage], merge_lists]
    market_data_cache: Annotated[Dict[str, Any], merge_cache]
    current_symbol: Annotated[str, override_state]
    secret_indicator_result: Annotated[float, override_state]
    intent: Annotated[str, override_state]  # "greet", "calculate_indicator", "general"
    next_node: Annotated[str, override_state]
    error_message: Annotated[str, override_state] 