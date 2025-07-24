from typing import Literal
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from state import MarketAnalysisState
from tools import fetch_mock_marketdata, secret_indicator
from config import settings
import re

def get_llm_client(temperature: float = 0.7) -> ChatOpenAI:
    """Get LLM client with specified temperature."""
    return ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,
        model=settings.DEFAULT_MODEL,
        temperature=temperature,
        base_url=settings.OPENAI_BASE_URL
    )

def intent_classifier_node(state: MarketAnalysisState) -> MarketAnalysisState:
    """
    Classifies user intent from the latest message.
    Determines if user wants to greet, calculate indicator, or general chat.
    """
    if not state["messages"]:
        return {"intent": "greet", "next_node": "response"}
    
    last_message = state["messages"][-1]
    if isinstance(last_message, HumanMessage):
        user_input = last_message.content.lower()
        
        greet_patterns = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
        if any(pattern in user_input for pattern in greet_patterns):
            return {"intent": "greet", "next_node": "response"}
        
        indicator_patterns = ["secret indicator", "calculate", "analyze", "indicator"]
        crypto_patterns = ["sol", "btc", "eth", "ada", "dot", "crypto", "coin", "token"]
        
        if (any(pattern in user_input for pattern in indicator_patterns) and 
            any(pattern in user_input for pattern in crypto_patterns)):
            
            symbol_match = re.search(r'\b(SOL|BTC|ETH|ADA|DOT)\b', user_input.upper())
            symbol = symbol_match.group(1) if symbol_match else "SOL"
            
            return {
                "intent": "calculate_indicator", 
                "current_symbol": symbol,
                "next_node": "fetch_market_data"
            }
        
        return {"intent": "general", "next_node": "response"}
    
    return {"intent": "general", "next_node": "response"}

def fetch_market_data_node(state: MarketAnalysisState) -> MarketAnalysisState:
    """
    Fetches market data for the specified symbol and caches it.
    """
    symbol = state.get("current_symbol", "SOL")
    
    try:
        if symbol in state.get("market_data_cache", {}):
            return {"next_node": "calculate_secret_indicator"}
        
        market_data = fetch_mock_marketdata(symbol)
        
        cache_update = {symbol: market_data}
        
        return {
            "market_data_cache": cache_update,
            "next_node": "calculate_secret_indicator"
        }
        
    except Exception as e:
        return {
            "error_message": f"Failed to fetch market data for {symbol}: {str(e)}",
            "next_node": "error_response"
        }

def calculate_secret_indicator_node(state: MarketAnalysisState) -> MarketAnalysisState:
    """
    Calculates the secret indicator using cached market data.
    """
    symbol = state.get("current_symbol", "SOL")
    market_data_cache = state.get("market_data_cache", {})
    
    try:
        if symbol not in market_data_cache:
            return {
                "error_message": f"No market data found for {symbol}",
                "next_node": "error_response"
            }
        
        market_data = market_data_cache[symbol]
        indicator_result = secret_indicator(market_data)
        
        return {
            "secret_indicator_result": indicator_result,
            "next_node": "response"
        }
        
    except Exception as e:
        return {
            "error_message": f"Failed to calculate secret indicator: {str(e)}",
            "next_node": "error_response"
        }

def response_node(state: MarketAnalysisState) -> MarketAnalysisState:
    """
    Generates appropriate response based on intent and available data.
    """
    intent = state.get("intent", "general")
    
    if intent == "greet":
        response = "Hello! I'm your market analysis assistant. I can help you calculate secret indicators for cryptocurrencies like SOL, BTC, ETH, ADA, and DOT. Just ask me to analyze any of these symbols!"
        
    elif intent == "calculate_indicator":
        symbol = state.get("current_symbol", "SOL")
        indicator_result = state.get("secret_indicator_result")
        market_data_cache = state.get("market_data_cache", {})
        
        if indicator_result is not None and symbol in market_data_cache:
            market_data = market_data_cache[symbol]
            response = f"""🔍 Secret Indicator Analysis for {symbol}:

📊 Current Market Data:
• Price: ${market_data['price']:,.2f}
• 24h Change: {market_data['24h_change']:+.2f}%
• Volume: {market_data['volume']:,}
• Market Cap: ${market_data['market_cap']:,}

🎯 Secret Indicator Score: {indicator_result}/100

💡 Interpretation:
• Score 0-30: Weak signal
• Score 31-60: Moderate signal  
• Score 61-80: Strong signal
• Score 81-100: Very strong signal

Current signal strength: {"Very strong" if indicator_result > 80 else "Strong" if indicator_result > 60 else "Moderate" if indicator_result > 30 else "Weak"}
"""
        else:
            response = f"I apologize, but I couldn't complete the analysis for {symbol}. Please try again."
            
    else:
        # General response using LLM
        llm = get_llm_client(temperature=0.7)
        last_message = state["messages"][-1] if state["messages"] else None
        
        if last_message:
            llm_response = llm.invoke([
                {"role": "system", "content": "You are a helpful market analysis assistant. Respond conversationally and guide users to ask about secret indicator calculations for cryptocurrencies."},
                {"role": "user", "content": last_message.content}
            ])
            response = llm_response.content
        else:
            response = "How can I help you with market analysis today?"
    
    return {"messages": [AIMessage(content=response)]}

def error_response_node(state: MarketAnalysisState) -> MarketAnalysisState:
    """
    Handles error cases and provides helpful error messages.
    """
    error_message = state.get("error_message", "An unknown error occurred")
    
    response = f"❌ Error: {error_message}\n\nPlease try again or ask me to analyze a different cryptocurrency (SOL, BTC, ETH, ADA, DOT)."
    
    return {"messages": [AIMessage(content=response)]}

def determine_next_node(state: MarketAnalysisState) -> Literal["response", "error_response"]:
    """
    Determines the next node based on the current state.
    """
    return state.get("next_node", "response") 