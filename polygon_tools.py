import os
from datetime import datetime
from polygon import RESTClient
from pydantic_ai import RunContext
from polygon.rest.models import StockFinancial
from typing import Dict, Any
import asyncio
import dotenv

dotenv.load_dotenv()


client = RESTClient(api_key=os.getenv("POLYGON_API_KEY"))


async def get_financial_statements(ticker: RunContext[str]) -> Dict[str, Any]:
    """Get historical financial statements for a company."""
    print(f"Ticker deps value: {ticker.deps}")

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
