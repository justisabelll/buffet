import json
import asyncio
from pathlib import Path
from pydantic_ai import Agent, RunContext
from dotenv import load_dotenv
from polygon_tools import get_financial_statements


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
    tools=[get_financial_statements],
)


@data_acquisition_agent.system_prompt
def fetch_financial_statements(ticker: RunContext[str]) -> dict:
    return f"Retrieve historical financial statements (income statement, balance sheet, cash flow statement) for {ticker.deps}. Present this data in a structured format, including key metrics and trends and other interesting information. Use the get_financial_statements tool to fetch the data."


async def main():
    print("Running...")
    ticker = "AAPL"
    print(f"Requesting data for ticker: {ticker}")
    results = await data_acquisition_agent.run("Get financial statements for this ticker", deps=ticker)
    print("Results Analysis:")
    print(results.data)


if __name__ == "__main__":
    asyncio.run(main())
