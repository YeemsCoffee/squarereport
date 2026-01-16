"""Square Cafe Report - Main Streamlit Application."""
import streamlit as st
from datetime import datetime, date
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config_loader import load_config, get_square_config, get_locations, get_timezone, get_peak_hours
from square_client import SquareReportClient
from report_processor import ReportProcessor


def init_session_state():
    """Initialize Streamlit session state variables."""
    if 'config' not in st.session_state:
        try:
            st.session_state.config = load_config()
        except FileNotFoundError as e:
            st.error(str(e))
            st.stop()
        except Exception as e:
            st.error(f"Error loading configuration: {e}")
            st.stop()

    if 'client' not in st.session_state:
        square_config = get_square_config(st.session_state.config)
        st.session_state.client = SquareReportClient(
            access_token=square_config['access_token'],
            environment=square_config['environment']
        )

    if 'processor' not in st.session_state:
        timezone = get_timezone(st.session_state.config)
        st.session_state.processor = ReportProcessor(timezone)


def main():
    """Main application entry point."""
    st.set_page_config(
        page_title="Square Cafe Report",
        page_icon="☕",
        layout="wide"
    )

    # Initialize session state
    init_session_state()

    # Header
    st.title("☕ Square Cafe Report")
    st.markdown("---")

    # Sidebar for inputs
    with st.sidebar:
        st.header("Report Settings")

        # Location selector
        locations = get_locations(st.session_state.config)
        location_options = {loc['name']: loc['id'] for loc in locations}

        selected_location_name = st.selectbox(
            "Select Location",
            options=list(location_options.keys())
        )
        selected_location_id = location_options[selected_location_name]

        # Date picker
        selected_date = st.date_input(
            "Select Date",
            value=date.today(),
            max_value=date.today()
        )

        # Generate report button
        generate_button = st.button("Generate Report", type="primary", use_container_width=True)

    # Main content area
    if generate_button:
        with st.spinner("Fetching data from Square..."):
            # Fetch orders
            orders = st.session_state.client.get_orders_for_date(
                location_id=selected_location_id,
                date=selected_date,
                timezone_str=get_timezone(st.session_state.config)
            )

            if not orders:
                st.warning(f"No orders found for {selected_location_name} on {selected_date}")
                return

            # Fetch catalog for drink names
            catalog_map = st.session_state.client.get_catalog_items()

        with st.spinner("Processing data..."):
            processor = st.session_state.processor
            peak_hours = get_peak_hours(st.session_state.config)

            # Calculate metrics
            longest_time, longest_order = processor.get_longest_ticket_time_peak_hours(
                orders,
                start_hour=peak_hours['start'],
                end_hour=peak_hours['end']
            )

            avg_time = processor.get_average_ticket_time(orders)

            total_sales, top_drinks = processor.get_sales_and_top_drinks(
                orders,
                catalog_map,
                top_n=5
            )

        # Display results
        st.subheader(f"Report for {selected_location_name} - {selected_date.strftime('%B %d, %Y')}")

        # Metrics row
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Longest Ticket Time (11am-2pm PST)",
                processor.format_ticket_time(longest_time) if longest_time else "N/A"
            )

        with col2:
            st.metric(
                "Average Ticket Time",
                processor.format_ticket_time(avg_time) if avg_time else "N/A"
            )

        with col3:
            st.metric(
                "Total Sales",
                f"${total_sales:,.2f}"
            )

        st.markdown("---")

        # Top 5 Drinks Section
        st.subheader("Top 5 Drinks")

        if top_drinks:
            # Create DataFrame for better display
            drinks_df = pd.DataFrame(
                top_drinks,
                columns=['Drink Name', 'Quantity Sold', 'Revenue']
            )
            drinks_df['Revenue'] = drinks_df['Revenue'].apply(lambda x: f"${x:.2f}")

            # Display as table
            st.dataframe(
                drinks_df,
                use_container_width=True,
                hide_index=True
            )

            # Visualization - Bar chart for quantities
            fig = px.bar(
                x=[drink[1] for drink in top_drinks],
                y=[drink[0] for drink in top_drinks],
                orientation='h',
                labels={'x': 'Quantity Sold', 'y': 'Drink'},
                title="Top 5 Drinks by Quantity"
            )
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("No drink data available for this date.")

        # Additional stats
        st.markdown("---")
        st.subheader("Additional Statistics")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Orders", len(orders))

        with col2:
            avg_order_value = total_sales / len(orders) if orders else 0
            st.metric("Average Order Value", f"${avg_order_value:.2f}")

    else:
        # Show instructions when no report is generated
        st.info("👈 Select a location and date from the sidebar, then click 'Generate Report'")

        # Show sample instructions
        st.markdown("""
        ### How to Use

        1. **Select Location**: Choose which cafe location you want to generate a report for
        2. **Select Date**: Pick the date for the report
        3. **Generate Report**: Click the button to fetch and analyze the data

        ### Metrics Included

        - **Longest Ticket Time (11am-2pm PST)**: The longest time a customer waited during peak lunch hours
        - **Average Ticket Time**: Average wait time across all orders for the day
        - **Total Sales**: Total revenue for the selected day
        - **Top 5 Drinks**: Best-selling drinks with quantities and revenue breakdown
        """)


if __name__ == "__main__":
    main()
