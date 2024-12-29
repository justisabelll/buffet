import json
from pathlib import Path
from pydantic_ai import Agent, RunContext


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
)


@data_acquisition_agent.system_prompt
def fetch_financial_statements(ticker: RunContext[str]) -> str:
    return f"Retrieve historical financial statements (income statement, balance sheet, cash flow statement) for {ticker.deps}. Obtain data for at least the past 5 years, ideally 10. Prioritize direct API access if available, falling back to web scraping for public filings if necessary."
