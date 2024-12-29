import json
import asyncio
from pathlib import Path
from pydantic_ai import Agent, RunContext
from dotenv import load_dotenv
from polygon_tools import get_financial_statements, get_historical_prices


load_dotenv()


# load config
config_path = Path(__file__).parent / "config.json"
with open(config_path, "r") as f:
    config = json.load(f)

# agents

data_acquisition_agent = Agent(
    name="data_acquisition_agent",
    deps_type=str,
    model="claude-3-5-haiku-latest",
    system_prompt=config["data_acquisition_agent"]["system_prompt"],
    tools=[get_financial_statements, get_historical_prices],
)


@data_acquisition_agent.system_prompt
def fetch_financial_statements(ticker: RunContext[str]) -> dict:
    return f"Retrieve historical financial statements (income statement, balance sheet, cash flow statement) for {ticker.deps}. Present this data in a structured format. Do not make any assumptions, commentary, or comments. Your job is only to fetch the data and present it in the cleanest format possible. Use the get_financial_statements tool to fetch the data."


@data_acquisition_agent.system_prompt
def fetch_historical_prices(ticker: RunContext[str]) -> dict:
    return f"Gather historical stock prices for {ticker.deps}, including daily open, high, low, close, and volume. Do not make any assumptions, commentary, or comments. Your job is only to fetch the data and present it in the cleanest format possible. Use the get_historical_prices tool to fetch the data."


async def main():
    print("Running...")
    ticker = "NVDA"
    results = await data_acquisition_agent.run(
        "Gather data for this ticker: " + ticker, deps=ticker
    )
    print("Results Analysis:")
    print("-" * 100)
    print(results)
    print("-" * 100)
    print(results.data)


if __name__ == "__main__":
    asyncio.run(main())
