from typing import List
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage, BaseMessage

from state import MarketAnalysisState
from nodes import (
    intent_classifier_node,
    fetch_market_data_node,
    calculate_secret_indicator_node,
    response_node,
    error_response_node,
    determine_next_node
)

def create_market_analysis_agent():
    """
    Creates and compiles the market analysis agent with LangGraph.
    """
    
    def initial_state_modifier(state: MarketAnalysisState) -> MarketAnalysisState:
        """Initialize state with default values."""
        return {
            "messages": [],
            "market_data_cache": {},
            "current_symbol": "",
            "secret_indicator_result": 0.0,
            "intent": "",
            "next_node": "",
            "error_message": ""
        }
    
    workflow = StateGraph(MarketAnalysisState)
    
    workflow.add_node("state_modifier", initial_state_modifier)
    workflow.add_node("intent_classifier", intent_classifier_node)
    workflow.add_node("response", response_node)
    workflow.add_node("error_response", error_response_node)
    
    workflow.set_entry_point("state_modifier")
    
    workflow.add_edge("state_modifier", "intent_classifier")
    
    workflow.add_conditional_edges(
        "intent_classifier",
        determine_next_node,
        {
            "response": "response",
            "error_response": "error_response"
        }
    )

    
    workflow.add_edge("response", "__end__")
    workflow.add_edge("error_response", "__end__")
    
    return workflow.compile()

class MarketAnalysisChat:
    """
    Chat interface for the market analysis agent that maintains conversation history.
    """
    
    def __init__(self):
        self.agent = create_market_analysis_agent()
        self.conversation_history: List[BaseMessage] = []
    
    def chat(self, user_input: str) -> str:
        """
        Process user input and return agent response while maintaining chat history.
        """
        user_message = HumanMessage(content=user_input)
        self.conversation_history.append(user_message)
        
        initial_state = {
            "messages": self.conversation_history.copy(),
            "market_data_cache": {},
            "current_symbol": "",
            "secret_indicator_result": 0.0,
            "intent": "",
            "next_node": "",
            "error_message": ""
        }
        
        result = self.agent.invoke(initial_state)
        
        if result["messages"]:
            response_message = result["messages"][-1]
            self.conversation_history.append(response_message)
            return response_message.content
        else:
            return "I apologize, but I couldn't process your request. Please try again."
    
    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_history = []

if __name__ == "__main__":
    chat = MarketAnalysisChat()
    
    print("Market Analysis Agent started! Type 'quit' to exit.")
    print("Try asking: 'Calculate secret indicator for SOL' or 'Hello'")
    print("-" * 50)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break
            
        if user_input:
            response = chat.chat(user_input)
            print(f"\nAgent: {response}") 