import os
from datetime import datetime
from polygon import RESTClient
from pydantic_ai import RunContext
from typing import Dict, Any
import asyncio
import dotenv

dotenv.load_dotenv()


client = RESTClient(api_key=os.getenv("POLYGON_API_KEY"))

TEST_MODE = True


async def get_financial_statements(ticker: RunContext[str]) -> Dict[str, Any]:
    """Get historical financial statements for a company."""
    print(f"Getting financial statements for {ticker.deps}")

    if not ticker.deps:
        return {
            "status": "error",
            "message": "No ticker symbol provided"
        }

    try:
        statements = client.vx.list_stock_financials(
            ticker=ticker.deps,
            timeframe="quarterly",
            period_of_report_date_gte=f"{datetime.now().year - 2}-01-01",
            period_of_report_date_lte=f"{datetime.now().year}-12-31",
            limit=100,
        )

        # Process the generator into a list with rate limit handling
        financial_data = []
        for statement in statements:
            financial_data.append(statement)
            await asyncio.sleep(0.2)  # Add delay between requests

        return {
            "status": "success",
            "data": financial_data
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


async def get_historical_prices(ticker: RunContext[str]) -> Dict[str, Any]:
    """Get historical prices for a company."""
    print(f"Getting historical prices for {ticker.deps}")
    if not ticker.deps:
        return {
            "status": "error",
            "message": "No ticker symbol provided"
        }

    try:
        if TEST_MODE:
            historical_prices = client.get_aggs(
                ticker=ticker.deps,
                multiplier=1,
                timespan="day",
                # Just current year in test mode
                from_=f"{datetime.now().year}-01-01",
                to=f"{datetime.now().year}-12-31",
                adjusted=True,
                sort="desc",
                limit=100  # Smaller limit in test mode
            )
        else:
            historical_prices = client.get_aggs(
                ticker=ticker.deps,
                multiplier=1,
                timespan="day",
                from_=f"{datetime.now().year - 2}-01-01",
                to=f"{datetime.now().year}-12-31",
                adjusted=True,
                sort="desc",
                limit=5000
            )

        data = []
        for price in historical_prices:
            data.append(price)

        return {
            "status": "success",
            "data": data
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
