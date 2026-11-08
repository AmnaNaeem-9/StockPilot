
import pandas as pd
import streamlit as st

from web_ui.components.common import (
    header,
    metric_card,
    section_title,
    products,
    categories,
    suppliers,
    status,
    money,
)


def render(inventory):

    # --------------------------------------------------
    # PAGE HEADER
    # --------------------------------------------------

    header(
        "Dashboard",
        "Monitor your inventory performance and stock activity.",
    )

    # --------------------------------------------------
    # FETCH INVENTORY DATA
    # --------------------------------------------------

    product_list = products(inventory)
    category_list = categories(inventory)
    supplier_list = suppliers(inventory)

    stats = inventory.get_dashboard_stats()

    total_products = stats["total_products"]
    total_categories = stats["total_categories"]
    total_suppliers = stats["total_suppliers"]
    inventory_value = stats["inventory_value"]

    # --------------------------------------------------
    # CALCULATE STOCK STATUS
    # --------------------------------------------------

    healthy_products = [
        p for p in product_list
        if status(p["quantity"], p["reorder_level"]) == "Healthy"
    ]

    low_stock = [
        p for p in product_list
        if status(p["quantity"], p["reorder_level"]) == "Low Stock"
    ]

    out_of_stock = [
        p for p in product_list
        if p["quantity"] <= 0
    ]

    # Count every product requiring attention only once.
    needs_attention = len(low_stock) + len(out_of_stock)

    # --------------------------------------------------
    # DASHBOARD METRIC CARDS
    # --------------------------------------------------

    columns = st.columns(5)

    metrics = [
        (
            "Inventory Value",
            money(inventory_value),
            "Current stock valuation",
        ),
        (
            "Total Products",
            total_products,
            "Registered products",
        ),
        (
            "Categories",
            total_categories,
            "Product categories",
        ),
        (
            "Suppliers",
            total_suppliers,
            "Registered suppliers",
        ),
        (
            "Needs Attention",
            needs_attention,
            "Low or out of stock",
        ),
    ]

    for column, metric in zip(columns, metrics):
        with column:
            metric_card(*metric)

    # --------------------------------------------------
    # INVENTORY OVERVIEW
    # --------------------------------------------------

    section_title(
        "Inventory Overview",
        "A breakdown of your current stock.",
    )

    left, right = st.columns([1.5, 1])

    # --------------------------------------------------
    # STOCK DISTRIBUTION
    # --------------------------------------------------

    with left:

        st.markdown(
            '<div class="panel">',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="panel-title">Stock Distribution</div>',
            unsafe_allow_html=True,
        )

        distribution = pd.DataFrame({
            "Stock Status": [
                "Healthy",
                "Low Stock",
                "Out of Stock",
            ],
            "Products": [
                len(healthy_products),
                len(low_stock),
                len(out_of_stock),
            ],
        })

        if not product_list:

            st.info(
                "Add products to see stock distribution."
            )

        else:

            st.bar_chart(
                distribution.set_index("Stock Status"),
                color="#ed3158",
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    # --------------------------------------------------
    # CATEGORY DISTRIBUTION
    # --------------------------------------------------

    with right:

        st.markdown(
            '<div class="panel">',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="panel-title">Category Distribution</div>',
            unsafe_allow_html=True,
        )

        category_counts = []

        for category in category_list:

            count = sum(
                1
                for p in product_list
                if p["category_id"] == category["id"]
            )

            category_counts.append({
                "Category": category["name"],
                "Products": count,
            })

        category_df = pd.DataFrame(category_counts)

        if (
            not category_df.empty
            and category_df["Products"].sum() > 0
        ):

            st.bar_chart(
                category_df.set_index("Category"),
                color="#ed3158",
            )

        else:

            st.info(
                "No category data available."
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    # --------------------------------------------------
    # PRODUCTS REQUIRING ATTENTION
    # --------------------------------------------------

    section_title("Products Requiring Attention")

    attention_data = []

    for p in product_list:

        product_status = status(
            p["quantity"],
            p["reorder_level"],
        )

        if product_status != "Healthy":

            attention_data.append({
                "Product": p["name"],
                "SKU": p["sku"],
                "Quantity": p["quantity"],
                "Reorder Level": p["reorder_level"],
                "Status": product_status,
            })

    if attention_data:

        st.dataframe(
            pd.DataFrame(attention_data),
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.success(
            "All products are currently above their reorder levels."
        )

    # --------------------------------------------------
    # RECENT INVENTORY
    # --------------------------------------------------

    section_title("Recent Inventory")

    recent_products = sorted(
        product_list,
        key=lambda p: p["id"],
        reverse=True,
    )[:8]

    if recent_products:

        recent_data = []

        for p in recent_products:

            recent_data.append({
                "Product": p["name"],
                "SKU": p["sku"],
                "Price": money(p["price"]),
                "Quantity": p["quantity"],
                "Stock Value": money(
                    p["price"] * p["quantity"]
                ),
                "Status": status(
                    p["quantity"],
                    p["reorder_level"],
                ),
            })

        st.dataframe(
            pd.DataFrame(recent_data),
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No products have been added yet."
        )

    # --------------------------------------------------
    # RECENT STOCK ACTIVITY
    # --------------------------------------------------

    section_title("Recent Stock Activity")

    try:

        transactions = inventory.get_transaction_history()

        if transactions:

            product_names = {
                p["id"]: p["name"]
                for p in product_list
            }

            transaction_data = []

            for transaction in transactions:

                transaction_data.append({

                    "Product": product_names.get(
                        transaction.product_id,
                        "Unknown product",
                    ),

                    "Type": transaction.transaction_type,

                    "Quantity": transaction.quantity,

                    "Date": transaction.transaction_date,

                    "Notes": transaction.notes or "",
                })

            # Sort newest transactions first.
            transaction_data.sort(
                key=lambda item: (
                    item["Date"] is not None,
                    item["Date"]
                ),
                reverse=True,
            )

            st.dataframe(
                pd.DataFrame(transaction_data[:8]),
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.info(
                "No stock transactions recorded yet."
            )

    except Exception as error:

        st.error(
            f"Unable to display stock activity: {error}"
        )
