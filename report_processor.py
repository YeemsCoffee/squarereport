"""Process Square orders data to generate reports."""
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple, Optional
import pytz
from collections import defaultdict


class ReportProcessor:
    """Process Square orders to generate cafe metrics."""

    def __init__(self, timezone_str: str = "America/Los_Angeles"):
        """
        Initialize the report processor.

        Args:
            timezone_str: Timezone string for time-based calculations
        """
        self.timezone = pytz.timezone(timezone_str)

    def calculate_ticket_time(self, order: Dict[str, Any]) -> Optional[float]:
        """
        Calculate the time taken for a ticket (order) in minutes.

        Args:
            order: Square order dictionary

        Returns:
            Time in minutes, or None if cannot be calculated
        """
        try:
            created_at = order.get('created_at')
            closed_at = order.get('closed_at') or order.get('updated_at')

            if not created_at or not closed_at:
                return None

            created_time = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            closed_time = datetime.fromisoformat(closed_at.replace('Z', '+00:00'))

            # Convert to local timezone
            created_local = created_time.astimezone(self.timezone)
            closed_local = closed_time.astimezone(self.timezone)

            # Calculate difference in minutes
            diff = (closed_local - created_local).total_seconds() / 60.0

            return diff if diff >= 0 else None

        except Exception as e:
            print(f"Error calculating ticket time: {e}")
            return None

    def get_order_hour(self, order: Dict[str, Any]) -> Optional[int]:
        """
        Get the hour of day when the order was created (in local timezone).

        Args:
            order: Square order dictionary

        Returns:
            Hour (0-23) or None
        """
        try:
            created_at = order.get('created_at')
            if not created_at:
                return None

            created_time = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            created_local = created_time.astimezone(self.timezone)

            return created_local.hour

        except Exception as e:
            print(f"Error getting order hour: {e}")
            return None

    def get_longest_ticket_time_peak_hours(
        self,
        orders: List[Dict[str, Any]],
        start_hour: int = 11,
        end_hour: int = 14
    ) -> Tuple[Optional[float], Optional[Dict[str, Any]]]:
        """
        Find the longest ticket time during peak hours.

        Args:
            orders: List of Square orders
            start_hour: Start hour for peak period (inclusive)
            end_hour: End hour for peak period (exclusive)

        Returns:
            Tuple of (longest_time_in_minutes, order_details)
        """
        longest_time = None
        longest_order = None

        for order in orders:
            hour = self.get_order_hour(order)

            # Check if order is within peak hours
            if hour is not None and start_hour <= hour < end_hour:
                ticket_time = self.calculate_ticket_time(order)

                if ticket_time is not None:
                    if longest_time is None or ticket_time > longest_time:
                        longest_time = ticket_time
                        longest_order = order

        return longest_time, longest_order

    def get_average_ticket_time(self, orders: List[Dict[str, Any]]) -> Optional[float]:
        """
        Calculate average ticket time for all orders.

        Args:
            orders: List of Square orders

        Returns:
            Average time in minutes, or None if no valid orders
        """
        times = []

        for order in orders:
            ticket_time = self.calculate_ticket_time(order)
            if ticket_time is not None:
                times.append(ticket_time)

        if not times:
            return None

        return sum(times) / len(times)

    def get_sales_and_top_drinks(
        self,
        orders: List[Dict[str, Any]],
        catalog_map: Dict[str, str],
        top_n: int = 5
    ) -> Tuple[float, List[Tuple[str, int, float]]]:
        """
        Calculate total sales and identify top drinks.

        Args:
            orders: List of Square orders
            catalog_map: Mapping of item variation IDs to item names
            top_n: Number of top drinks to return

        Returns:
            Tuple of (total_sales, top_drinks_list)
            where top_drinks_list is [(drink_name, quantity, revenue), ...]
        """
        total_sales = 0.0
        drink_stats = defaultdict(lambda: {'quantity': 0, 'revenue': 0.0})

        for order in orders:
            # Add to total sales
            total_money = order.get('total_money', {})
            amount = total_money.get('amount', 0)
            # Amount is in cents, convert to dollars
            order_total = amount / 100.0
            total_sales += order_total

            # Process line items to track drinks
            line_items = order.get('line_items', [])
            for item in line_items:
                variation_id = item.get('catalog_object_id')
                quantity = int(item.get('quantity', 1))
                item_total = item.get('total_money', {}).get('amount', 0) / 100.0

                # Get item name from catalog
                item_name = catalog_map.get(variation_id, 'Unknown Item')

                drink_stats[item_name]['quantity'] += quantity
                drink_stats[item_name]['revenue'] += item_total

        # Sort by quantity and get top N
        top_drinks = sorted(
            [(name, stats['quantity'], stats['revenue'])
             for name, stats in drink_stats.items()],
            key=lambda x: x[1],  # Sort by quantity
            reverse=True
        )[:top_n]

        return total_sales, top_drinks

    def format_ticket_time(self, minutes: Optional[float]) -> str:
        """
        Format ticket time for display.

        Args:
            minutes: Time in minutes

        Returns:
            Formatted string
        """
        if minutes is None:
            return "N/A"

        if minutes < 1:
            return f"{int(minutes * 60)} seconds"
        elif minutes < 60:
            return f"{minutes:.1f} minutes"
        else:
            hours = int(minutes // 60)
            mins = int(minutes % 60)
            return f"{hours}h {mins}m"
