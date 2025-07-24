# Market Analysis Agent

A LangGraph-based agent that calculates secret indicators for cryptocurrency market data.

## Features

- **Intent Classification**: Automatically determines if user wants to greet, calculate indicators, or general chat
- **Market Data Fetching**: Retrieves mock market data for supported cryptocurrencies
- **Secret Indicator Calculation**: Computes proprietary trading indicators
- **Chat History**: Maintains conversation context across multiple exchanges
- **Caching**: Stores market data to avoid redundant API calls

## Supported Cryptocurrencies

- SOL (Solana)
- BTC (Bitcoin)
- ETH (Ethereum)
- ADA (Cardano)
- DOT (Polkadot)

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Setup**:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to `.env`:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

3. **Run the Agent**:

   **Command Line Interface**:
   ```bash
   python agent.py
   ```

   **Web API**:
   ```bash
   python api.py
   # or
   uvicorn api:app --reload --host 0.0.0.0 --port 8000
   ```

## Usage Examples

### Command Line
```
You: Hello!
Agent: Hello! I'm your market analysis assistant...

You: Calculate secret indicator for SOL
Agent: 🔍 Secret Indicator Analysis for SOL:
📊 Current Market Data:
• Price: $98.45
• 24h Change: +5.23%
...
```

### API Endpoints

**POST /chat**
```json
{
  "message": "Calculate secret indicator for BTC",
  "session_id": "optional-session-id"
}
```

**Response**:
```json
{
  "response": "🔍 Secret Indicator Analysis for BTC...",
  "session_id": "session-uuid"
}
```

## Architecture

The agent uses LangGraph with the following flow:

1. **Intent Classifier Node**: Determines user intent
2. **Fetch Market Data Node**: Retrieves and caches market data
3. **Calculate Secret Indicator Node**: Computes proprietary indicators
4. **Response Node**: Generates appropriate responses
5. **Error Response Node**: Handles errors gracefully

## Project Structure

```
llm-test/
├── agent.py              # Main agent and chat interface
├── api.py                # FastAPI web service
├── config.py             # Configuration settings
├── nodes.py              # LangGraph nodes implementation
├── state.py              # State management and types
├── tools.py              # Mock tools (market data, indicators)
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
└── README.md            # This file
```

## Development Notes

This project is designed for interview purposes and contains intentional areas where bugs could be introduced for testing candidates' debugging skills.

### Potential Bug Areas

- Market data caching logic
- Symbol extraction from user input
- State management between nodes
- Error handling in tool functions
- Response formatting and data display

## Testing

Example test scenarios:

1. **Greeting**: "Hello", "Hi there"
2. **Indicator Calculation**: "Calculate secret indicator for SOL"
3. **Symbol Variations**: "Analyze BTC", "What's the indicator for ETH?"
4. **Error Cases**: Invalid symbols, network errors
5. **Chat History**: Multi-turn conversations 