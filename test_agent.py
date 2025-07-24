#!/usr/bin/env python3
"""
Test script for the Market Analysis Agent.
This script can be used to test the agent functionality without needing OpenAI API.
"""

import os
from unittest.mock import patch, MagicMock
from agent import MarketAnalysisChat

def test_mock_responses():
    """Test the agent with mocked LLM responses."""
    
    # Mock the OpenAI API call to avoid needing actual API key
    mock_response = MagicMock()
    mock_response.content = "This is a test response from the mock LLM."
    
    with patch('nodes.get_llm_client') as mock_llm:
        mock_llm.return_value.invoke.return_value = mock_response
        
        # Create chat instance
        chat = MarketAnalysisChat()
        
        print("Testing Market Analysis Agent...")
        print("=" * 50)
        
        # Test 1: Greeting
        print("\n1. Testing Greeting:")
        response = chat.chat("Hello!")
        print(f"Input: Hello!")
        print(f"Response: {response}")
        
        # Test 2: Secret indicator calculation
        print("\n2. Testing Secret Indicator Calculation:")
        response = chat.chat("Calculate secret indicator for SOL")
        print(f"Input: Calculate secret indicator for SOL")
        print(f"Response: {response}")
        
        # Test 3: Another symbol
        print("\n3. Testing Another Symbol:")
        response = chat.chat("Analyze BTC indicator")
        print(f"Input: Analyze BTC indicator")
        print(f"Response: {response}")
        
        # Test 4: General question
        print("\n4. Testing General Question:")
        response = chat.chat("What is cryptocurrency?")
        print(f"Input: What is cryptocurrency?")
        print(f"Response: {response}")
        
        print("\n" + "=" * 50)
        print("All tests completed!")

def test_tools_directly():
    """Test the mock tools directly."""
    from tools import fetch_mock_marketdata, secret_indicator
    
    print("\nTesting Tools Directly:")
    print("=" * 30)
    
    # Test market data fetching
    print("\n1. Testing Market Data Fetching:")
    symbols = ["SOL", "BTC", "ETH"]
    
    for symbol in symbols:
        data = fetch_mock_marketdata(symbol)
        print(f"\n{symbol} Data:")
        for key, value in data.items():
            print(f"  {key}: {value}")
    
    # Test secret indicator calculation
    print("\n2. Testing Secret Indicator Calculation:")
    sol_data = fetch_mock_marketdata("SOL")
    indicator_score = secret_indicator(sol_data)
    print(f"\nSOL Secret Indicator Score: {indicator_score}/100")

if __name__ == "__main__":
    print("Market Analysis Agent Test Suite")
    print("This script tests the agent without requiring OpenAI API key")
    print("For full functionality, set up your .env file with OPENAI_API_KEY")
    print()
    
    # Test tools first
    test_tools_directly()
    
    # Test agent with mocked LLM
    test_mock_responses() 