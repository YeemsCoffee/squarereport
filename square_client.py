"""Square API client wrapper."""
from square import Client
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import pytz


class SquareReportClient:
    """Client for fetching Square data for reports."""

    def __init__(self, access_token: str, environment: str = "production"):
        """
        Initialize Square client.

        Args:
            access_token: Square API access token
            environment: 'sandbox' or 'production'
        """
        self.client = Client(
            access_token=access_token,
            environment=environment
        )
        self.orders_api = self.client.orders
        self.catalog_api = self.client.catalog

    def get_orders_for_date(
        self,
        location_id: str,
        date: datetime,
        timezone_str: str = "America/Los_Angeles"
    ) -> List[Dict[str, Any]]:
        """
        Fetch all orders for a specific date and location.

        Args:
            location_id: Square location ID
            date: Date to fetch orders for
            timezone_str: Timezone string (e.g., 'America/Los_Angeles')

        Returns:
            List of order dictionaries
        """
        tz = pytz.timezone(timezone_str)

        # Set start of day (midnight) and end of day (11:59:59 PM)
        start_date = tz.localize(datetime.combine(date, datetime.min.time()))
        end_date = start_date + timedelta(days=1) - timedelta(seconds=1)

        # Convert to UTC for API
        start_utc = start_date.astimezone(pytz.UTC)
        end_utc = end_date.astimezone(pytz.UTC)

        orders = []
        cursor = None

        try:
            while True:
                # Build query
                query = {
                    "filter": {
                        "location_ids": [location_id],
                        "date_time_filter": {
                            "created_at": {
                                "start_at": start_utc.isoformat(),
                                "end_at": end_utc.isoformat()
                            }
                        },
                        "state_filter": {
                            "states": ["COMPLETED", "OPEN"]
                        }
                    },
                    "sort": {
                        "sort_field": "CREATED_AT",
                        "sort_order": "ASC"
                    }
                }

                if cursor:
                    result = self.orders_api.search_orders(
                        body={
                            "location_ids": [location_id],
                            "query": query,
                            "cursor": cursor
                        }
                    )
                else:
                    result = self.orders_api.search_orders(
                        body={
                            "location_ids": [location_id],
                            "query": query
                        }
                    )

                if result.is_success():
                    body = result.body
                    if 'orders' in body:
                        orders.extend(body['orders'])

                    # Check for more pages
                    cursor = body.get('cursor')
                    if not cursor:
                        break
                else:
                    print(f"Error fetching orders: {result.errors}")
                    break

        except Exception as e:
            print(f"Exception while fetching orders: {e}")

        return orders

    def get_catalog_items(self) -> Dict[str, str]:
        """
        Fetch catalog items (drinks) from Square.

        Returns:
            Dictionary mapping item variation IDs to item names
        """
        catalog_map = {}
        cursor = None

        try:
            while True:
                if cursor:
                    result = self.catalog_api.list_catalog(
                        cursor=cursor,
                        types="ITEM"
                    )
                else:
                    result = self.catalog_api.list_catalog(types="ITEM")

                if result.is_success():
                    body = result.body

                    if 'objects' in body:
                        for obj in body['objects']:
                            if obj['type'] == 'ITEM':
                                item_name = obj.get('item_data', {}).get('name', 'Unknown Item')

                                # Map each variation to the item name
                                variations = obj.get('item_data', {}).get('variations', [])
                                for variation in variations:
                                    variation_id = variation.get('id')
                                    variation_name = variation.get('item_variation_data', {}).get('name', '')

                                    # Combine item name with variation if it exists
                                    full_name = f"{item_name}"
                                    if variation_name and variation_name.lower() not in ['regular', 'default', '']:
                                        full_name = f"{item_name} ({variation_name})"

                                    catalog_map[variation_id] = full_name

                    cursor = body.get('cursor')
                    if not cursor:
                        break
                else:
                    print(f"Error fetching catalog: {result.errors}")
                    break

        except Exception as e:
            print(f"Exception while fetching catalog: {e}")

        return catalog_map
