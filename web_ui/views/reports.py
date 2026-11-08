
import streamlit as st
import pandas as pd

from web_ui.components.common import (
    header,
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
        "Reports",
        "Review inventory valuation, stock health and operational activity."
    )

    # --------------------------------------------------
    # FETCH DATA
    # --------------------------------------------------

    product_list = products(inventory)
    category_list = categories(inventory)
    supplier_list = suppliers(inventory)

    # --------------------------------------------------
    # INVENTORY CALCULATIONS
    # --------------------------------------------------

    total_units = sum(
        p["quantity"] for p in product_list
    )

    total_value = sum(
        p["price"] * p["quantity"]
        for p in product_list
    )

    low_stock = sum(
        1 for p in product_list
        if 0 < p["quantity"] <= p["reorder_level"]
    )

    out_of_stock = sum(
        1 for p in product_list
        if p["quantity"] <= 0
    )

    healthy_stock = sum(
        1 for p in product_list
        if p["quantity"] > p["reorder_level"]
    )

    # --------------------------------------------------
    # REPORT OVERVIEW
    # --------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Inventory Value",
        money(total_value)
    )

    c2.metric(
        "Total Units",
        total_units
    )

    c3.metric(
        "Low Stock",
        low_stock
    )

    c4.metric(
        "Out of Stock",
        out_of_stock
    )

    # ==================================================
    # SECTION 1: INVENTORY VALUATION
    # ==================================================

    section_title("Inventory Valuation")

    valuation = []

    for p in product_list:

        stock_value = p["price"] * p["quantity"]

        valuation.append({

            "Product": p["name"],

            "SKU": p["sku"],

            "Quantity": p["quantity"],

            "Unit Price": p["price"],

            "Stock Value": stock_value,

            "Status": status(
                p["quantity"],
                p["reorder_level"]
            ),

        })

    if valuation:

        valuation_df = pd.DataFrame(valuation)

        st.dataframe(
            valuation_df.style.format({
                "Unit Price": "${:,.2f}",
                "Stock Value": "${:,.2f}",
            }),
            use_container_width=True,
            hide_index=True,
        )

        # CSV EXPORT

        csv = valuation_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download Valuation CSV",
            data=csv,
            file_name="stockpilot_inventory_valuation.csv",
            mime="text/csv",
            key="reports_valuation_download",
        )

        st.caption(
            f"Total products included: {len(valuation)}"
        )

    else:

        st.info(
            "No inventory data available for reporting."
        )

    # ==================================================
    # SECTION 2: STOCK HEALTH
    # ==================================================

    section_title("Stock Health")

    health_data = [
        {
            "Status": "Healthy",
            "Products": healthy_stock,
        },
        {
            "Status": "Low Stock",
            "Products": low_stock,
        },
        {
            "Status": "Out of Stock",
            "Products": out_of_stock,
        },
    ]

    health_df = pd.DataFrame(
        health_data
    ).set_index("Status")

    st.bar_chart(
        health_df,
        color="#ed3158",
    )

    # ==================================================
    # SECTION 3: CATEGORY SUMMARY
    # ==================================================

    section_title("Category Summary")

    category_summary = []

    for category in category_list:

        matching = [
            p for p in product_list
            if p["category_id"] == category["id"]
        ]

        category_summary.append({

            "Category": category["name"],

            "Products": len(matching),

            "Units": sum(
                p["quantity"] for p in matching
            ),

            "Value": sum(
                p["price"] * p["quantity"]
                for p in matching
            ),

        })

    if category_summary:

        category_df = pd.DataFrame(
            category_summary
        )

        st.dataframe(
            category_df.style.format({
                "Value": "${:,.2f}",
            }),
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No categories available."
        )

    # ==================================================
    # SECTION 4: SUPPLIER SUMMARY
    # ==================================================

    section_title("Supplier Summary")

    supplier_summary = []

    for supplier in supplier_list:

        matching = [
            p for p in product_list
            if p["supplier_id"] == supplier["id"]
        ]

        supplier_summary.append({

            "Supplier": supplier["name"],

            "Products": len(matching),

            "Units": sum(
                p["quantity"] for p in matching
            ),

        })

    if supplier_summary:

        supplier_df = pd.DataFrame(
            supplier_summary
        )

        st.dataframe(
            supplier_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No suppliers available."
        )

    # ==================================================
    # SECTION 5: TRANSACTION SUMMARY
    # ==================================================

    section_title("Transaction Summary")

    try:

        transactions = inventory.get_transaction_history()

        if transactions:

            stock_in = sum(
                t.quantity for t in transactions
                if t.transaction_type == "STOCK_IN"
            )

            stock_out = sum(
                t.quantity for t in transactions
                if t.transaction_type == "STOCK_OUT"
            )

            a, b, c = st.columns(3)

            a.metric(
                "Total Transactions",
                len(transactions)
            )

            b.metric(
                "Units Received",
                stock_in
            )

            c.metric(
                "Units Dispatched",
                stock_out
            )

        else:

            st.info(
                "No stock transactions available."
            )

    except Exception as error:

        st.error(
            f"Unable to load transaction summary: {error}"
        )
