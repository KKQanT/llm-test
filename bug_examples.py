"""
This file contains examples of bugs that could be introduced 
for testing candidates' debugging skills.

IMPORTANT: These are examples - don't actually introduce these bugs 
into the main code. Use these as reference for creating interview scenarios.
"""

# BUG EXAMPLE 1: State Management Issue
def buggy_fetch_market_data_node(state):
    """
    BUG: Not properly checking if market_data_cache exists in state
    This could cause KeyError when accessing cache
    """
    symbol = state.get("current_symbol", "SOL")
    
    # BUG: Assumes market_data_cache always exists
    if symbol in state["market_data_cache"]:  # KeyError if cache doesn't exist
        return {"next_node": "calculate_secret_indicator"}
    
    # Rest of implementation...

# BUG EXAMPLE 2: Symbol Extraction Logic
def buggy_intent_classifier(state):
    """
    BUG: Regex doesn't account for case sensitivity properly
    """
    user_input = state["messages"][-1].content
    
    # BUG: Regex is case sensitive but input might be lowercase
    symbol_match = re.search(r'\b(SOL|BTC|ETH|ADA|DOT)\b', user_input)  # Won't match "sol"
    symbol = symbol_match.group(1) if symbol_match else "SOL"
    
    return {"current_symbol": symbol}

# BUG EXAMPLE 3: Market Data Caching Issue
def buggy_cache_logic(state):
    """
    BUG: Cache is not being properly updated/merged
    """
    new_data = {"SOL": {"price": 100}}
    
    # BUG: This overwrites the entire cache instead of merging
    return {"market_data_cache": new_data}  # Loses previous cache entries

# BUG EXAMPLE 4: Response Formatting
def buggy_response_formatting(state):
    """
    BUG: Division by zero or missing data checks
    """
    indicator_result = state.get("secret_indicator_result")
    market_data = state["market_data_cache"]["SOL"]
    
    # BUG: No check if indicator_result is None or 0
    percentage = 100 / indicator_result  # ZeroDivisionError possible
    
    # BUG: Assumes market_data always has expected keys
    price_change = market_data["24h_change"]  # KeyError if key missing
    
    return f"Result: {percentage}% with change {price_change}"

# BUG EXAMPLE 5: Tool Error Handling
def buggy_secret_indicator(market_data):
    """
    BUG: Insufficient input validation
    """
    # BUG: Doesn't check if market_data is a dict
    price = market_data["price"]  # TypeError if market_data is None/string
    
    # BUG: No validation of numeric values
    volume = market_data.get("volume", 0)
    factor = volume / 1000000  # Could be problematic if volume is not numeric
    
    return factor * 10

# BUG EXAMPLE 6: Conversation History Issue
def buggy_chat_history(self, user_input):
    """
    BUG: Conversation history grows without bounds
    """
    # BUG: No limit on conversation history - memory leak
    user_message = HumanMessage(content=user_input)
    self.conversation_history.append(user_message)
    
    # If this runs for a long time, conversation_history becomes huge
    result = self.agent.invoke({"messages": self.conversation_history})

# BUG EXAMPLE 7: API Response Handling
def buggy_api_endpoint(request):
    """
    BUG: No proper error handling in API
    """
    session_id = request.session_id
    
    # BUG: Assumes session_id is always valid UUID format
    chat_agent = chat_sessions[session_id]  # KeyError if session doesn't exist
    
    # BUG: No timeout or error handling for agent processing
    response = chat_agent.chat(request.message)  # Could hang indefinitely
    
    return {"response": response}

# BUG EXAMPLE 8: Environment Configuration
def buggy_config():
    """
    BUG: Missing environment variable handling
    """
    # BUG: Will crash if OPENAI_API_KEY is not set
    api_key = os.environ["OPENAI_API_KEY"]  # KeyError if not set
    
    # Should use os.getenv() with default value instead

# BUG EXAMPLE 9: Mock Data Generation
def buggy_mock_data(symbol):
    """
    BUG: Mock data has inconsistent types
    """
    base_price = {"SOL": "100.0", "BTC": 45000}  # Mixed string/int types
    
    # BUG: String arithmetic will fail
    price = base_price[symbol] * 1.1  # TypeError if base_price is string
    
    return {"price": price}

# BUG EXAMPLE 10: Node Routing Logic
def buggy_determine_next_node(state):
    """
    BUG: Missing edge cases in routing logic
    """
    next_node = state.get("next_node")
    
    # BUG: No handling for unexpected next_node values
    valid_nodes = ["response", "error_response", "fetch_market_data"]
    
    # Should validate that next_node is in valid_nodes
    return next_node  # Could return invalid node name

"""
How to use these examples for interviews:

1. Introduce one or more of these bugs into the actual code
2. Give the candidate a scenario where the bug manifests
3. Ask them to:
   - Identify the bug
   - Explain why it happens
   - Fix the bug
   - Suggest improvements to prevent similar bugs

Example interview scenarios:
- "The agent crashes when user asks about an unknown cryptocurrency"
- "The cache seems to lose data between requests"
- "The API returns 500 errors randomly"
- "Memory usage keeps growing over time"
- "Symbol extraction doesn't work for lowercase input"
""" 