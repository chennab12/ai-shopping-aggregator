import streamlit as st
import pandas as pd
from pydantic import BaseModel, Field
from typing import List, Optional

# --- Pydantic Schema for Structured Deal Extraction ---
class DealItem(BaseModel):
    title: str = Field(description="Product title and variant description")
    source_site: str = Field(description="Retailer or marketplace e.g., Amazon, eBay, Best Buy, Walmart")
    condition: str = Field(description="Condition: Brand New, Certified Refurbished, Open Box, Used")
    current_price: float = Field(description="Current listed price in USD")
    historical_low: float = Field(description="Lowest recorded historical price")
    historical_high: float = Field(description="Highest recorded historical price")
    deal_rating: str = Field(description="Verdict: 🔥 Absolute Steal, 🟡 Fair Value, ❌ Overpriced")
    roi_score: float = Field(description="Calculated value score out of 100 based on discount off historical average")
    direct_link: str = Field(description="Product link URL")

# --- Streamlit Configuration ---
st.set_page_config(
    page_title="Agentic Shopping & Price Intelligence Aggregator",
    page_icon="🛍️",
    layout="wide"
)

st.title("🛍️ Agentic Multi-Site Shopping & Deal Intelligence Aggregator")
st.markdown("Search across multiple retail marketplaces from one central hub. Filter by condition and maximum budget, view historical price benchmarks, and see instant AI deal evaluations.")

# --- Sidebar Search & Dynamic Criteria ---
st.sidebar.header("Search & Filtering Criteria")
search_query = st.sidebar.text_input("Search Item (e.g., Sony WH-1000XM5, M2 MacBook Air)", "Sony WH-1000XM5")

max_budget = st.sidebar.slider("Maximum Budget ($ USD)", min_value=50, max_value=2000, value=400, step=25)

selected_conditions = st.sidebar.multiselect(
    "Accepted Item Conditions",
    ["Brand New", "Certified Refurbished", "Open Box", "Used"],
    default=["Brand New", "Certified Refurbished", "Open Box"]
)

selected_sources = st.sidebar.multiselect(
    "Retailers / Marketplaces",
    ["Amazon", "eBay", "Best Buy", "Walmart", "Back Market"],
    default=["Amazon", "eBay", "Best Buy", "Walmart", "Back Market"]
)

sort_by = st.sidebar.selectbox(
    "Sort Results By",
    ["Highest ROI / Best Deal Score", "Lowest Current Price", "Highest User Rating"]
)

if st.button("Run Multi-Site Deal Aggregator", type="primary"):
    with st.spinner(f"Agents querying marketplaces for '{search_query}' under ${max_budget}..."):
        
        # Simulated multi-site aggregated database response (In production, replace with API calls / scraping agents)
        mock_deals = [
            DealItem(
                title="Sony WH-1000XM5 Wireless Noise Canceling Headphones (Black)",
                source_site="Amazon",
                condition="Brand New",
                current_price=328.00,
                historical_low=298.00,
                historical_high=399.99,
                deal_rating="🟡 Fair Value",
                roi_score=78.5,
                direct_link="https://amazon.com"
            ),
            DealItem(
                title="Sony WH-1000XM5 Wireless Headphones - Certified Refurbished",
                source_site="eBay",
                condition="Certified Refurbished",
                current_price=229.00,
                historical_low=210.00,
                historical_high=350.00,
                deal_rating="🔥 Absolute Steal",
                roi_score=94.2,
                direct_link="https://ebay.com"
            ),
            DealItem(
                title="Sony WH-1000XM5 Over-Ear Noise Canceling - Open Box Excellent",
                source_site="Best Buy",
                condition="Open Box",
                current_price=279.99,
                historical_low=260.00,
                historical_high=399.99,
                deal_rating="🔥 Absolute Steal",
                roi_score=88.0,
                direct_link="https://bestbuy.com"
            ),
            DealItem(
                title="Sony WH-1000XM5 Headphones (Silver) - Lightly Used",
                source_site="Back Market",
                condition="Used",
                current_price=199.00,
                historical_low=185.00,
                historical_high=320.00,
                deal_rating="🔥 Absolute Steal",
                roi_score=96.1,
                direct_link="https://backmarket.com"
            ),
            DealItem(
                title="Sony WH-1000XM5 Brand New Retail Box",
                source_site="Walmart",
                current_price=348.00,
                historical_low=310.00,
                historical_high=399.99,
                deal_rating="❌ Overpriced",
                roi_score=62.0,
                direct_link="https://walmart.com"
            )
        ]
        
        df = pd.DataFrame([deal.dict() for deal in mock_deals])
        
        # Apply dynamic user filters
        filtered_df = df[
            (df["current_price"] <= max_budget) &
            (df["condition"].isin(selected_conditions)) &
            (df["source_site"].isin(selected_sources))
        ]
        
        if sort_by == "Highest ROI / Best Deal Score":
            filtered_df = filtered_df.sort_values(by="roi_score", ascending=False)
        elif sort_by == "Lowest Current Price":
            filtered_df = filtered_df.sort_values(by="current_price", ascending=True)
            
        st.success(f"Aggregated {len(filtered_df)} top-tier deals matching your criteria!")
        
        # --- Top Summary Metrics ---
        col1, col2, col3 = st.columns(3)
        if not filtered_df.empty:
            best_price = filtered_df["current_price"].min()
            avg_price = filtered_df["current_price"].mean()
            col1.metric("Lowest Price Found", f"${best_price:.2f}")
            col2.metric("Market Average Price", f"${avg_price:.2f}")
            col3.metric("Markets Queried", len(selected_sources))
        
        # --- Main Tabular Display ---
        st.subheader("📊 Aggregated Deal Intelligence & Price Comparison")
        
        if not filtered_df.empty:
            # Format display table
            display_df = filtered_df[["title", "source_site", "condition", "current_price", "historical_low", "historical_high", "deal_rating", "roi_score"]].copy()
            display_df.columns = ["Product Title", "Retailer", "Condition", "Current Price ($)", "Hist. Low ($)", "Hist. High ($)", "Deal Verdict", "ROI Score"]
            
            st.dataframe(display_df, use_container_width=True)
            
            st.markdown("### 🛒 Direct Retailer Links & Price Breakdown")
            for _, row in filtered_df.iterrows():
                with st.expander(f"[{row['source_site']}] {row['title']} — ${row['current_price']} ({row['deal_rating']})"):
                    col_a, col_b = st.columns([2, 1])
                    with col_a:
                        st.markdown(f"* **Retailer:** {row['source_site']}")
                        st.markdown(f"* **Condition:** {row['condition']}")
                        st.markdown(f"* **Historical Price Range:** ${row['historical_low']} (Low) to ${row['historical_high']} (High)")
                        st.markdown(f"* **Worth It Analysis:** Compared to historical pricing, current price is rated as **{row['deal_rating']}** with an ROI Value Score of **{row['roi_score']}/100**.")
                    with col_b:
                        st.link_button("🔗 View Live Deal", row["direct_link"])
        else:
            st.warning("No products matched your exact budget and condition filters. Try increasing your max budget or selecting more retailer sources.")
else:
    st.info("Configure your search query and filters in the sidebar, then click **Run Multi-Site Deal Aggregator** to view live deals.")
