
import streamlit as st
import pandas as pd

from web_ui.components.common import (
    header,
    section_title,
    products,
    status,
)


def render(inventory):

    # --------------------------------------------------
    # PAGE HEADER
    # --------------------------------------------------

    header(
        "Stock Management",
        "Record stock movements and monitor available quantities."
    )

    # --------------------------------------------------
    # FETCH PRODUCTS
    # --------------------------------------------------

    product_list = products(inventory)

    # --------------------------------------------------
    # STOCK OVERVIEW
    # --------------------------------------------------

    total_units = sum(
        p["quantity"] for p in product_list
    )

    low_stock = sum(
        1 for p in product_list
        if 0 < p["quantity"] <= p["reorder_level"]
    )

    out_of_stock = sum(
        1 for p in product_list
        if p["quantity"] <= 0
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Units",
        total_units
    )

    c2.metric(
        "Low Stock Products",
        low_stock
    )

    c3.metric(
        "Out of Stock Products",
        out_of_stock
    )

    # --------------------------------------------------
    # CHECK PRODUCT AVAILABILITY
    # --------------------------------------------------

    if not product_list:

        st.info(
            "Add products before recording stock movements."
        )

        return

    # --------------------------------------------------
    # STOCK MANAGEMENT TABS
    # --------------------------------------------------

    tab_movement, tab_current, tab_history = st.tabs([
        "Record Movement",
        "Current Stock",
        "Transaction History",
    ])

    # Product selection dictionary
    product_options = {
        f'{p["name"]} ({p["sku"]})': p
        for p in product_list
    }

    # ==================================================
    # TAB 1: RECORD STOCK MOVEMENT
    # ==================================================

    with tab_movement:

        section_title("Record Stock Movement")

        selected_label = st.selectbox(
            "Select Product",
            list(product_options.keys()),
            key="stock_product_selector"
        )

        selected = product_options[selected_label]

        st.caption(
            f'Available quantity: {selected["quantity"]} units'
        )

        movement = st.radio(
            "Movement Type",
            ["Stock In", "Stock Out"],
            horizontal=True,
            key="stock_movement_type"
        )

        with st.form(
            "stock_movement_form",
            clear_on_submit=True
        ):

            quantity = st.number_input(
                "Quantity",
                min_value=1,
                value=1,
                step=1,
                key="stock_movement_quantity"
            )

            notes = st.text_area(
                "Notes",
                placeholder="Optional notes...",
                key="stock_movement_notes"
            )

            submitted = st.form_submit_button(
                "Record Movement",
                use_container_width=True,
            )

            if submitted:

                try:

                    # ----------------------------------
                    # STOCK IN
                    # ----------------------------------

                    if movement == "Stock In":

                        inventory.stock_in(
                            selected["id"],
                            int(quantity),
                            notes.strip() or None,
                        )

                    # ----------------------------------
                    # STOCK OUT
                    # ----------------------------------

                    else:

                        if quantity > selected["quantity"]:

                            st.error(
                                "Insufficient stock. "
                                f'Only {selected["quantity"]} units are available.'
                            )

                            st.stop()

                        inventory.stock_out(
                            selected["id"],
                            int(quantity),
                            notes.strip() or None,
                        )

                    st.success(
                        f"{movement} recorded successfully."
                    )

                    st.rerun()

                except Exception as error:

                    st.error(
                        f"Unable to record movement: {error}"
                    )

    # ==================================================
    # TAB 2: CURRENT STOCK
    # ==================================================

    with tab_current:

        section_title("Current Stock Levels")

        stock_data = []

        for p in product_list:

            stock_data.append({

                "Product": p["name"],

                "SKU": p["sku"],

                "Available": p["quantity"],

                "Reorder Level": p["reorder_level"],

                "Status": status(
                    p["quantity"],
                    p["reorder_level"]
                ),

            })

        st.dataframe(
            pd.DataFrame(stock_data),
            use_container_width=True,
            hide_index=True,
        )

    # ==================================================
    # TAB 3: TRANSACTION HISTORY
    # ==================================================

    with tab_history:

        section_title("Transaction History")

        try:

            transactions = inventory.get_transaction_history()

            if transactions:

                product_names = {
                    p["id"]: p["name"]
                    for p in product_list
                }

                history = []

                for transaction in transactions:

                    history.append({

                        "Product": product_names.get(
                            transaction.product_id,
                            "Unknown product",
                        ),

                        "Type": transaction.transaction_type,

                        "Quantity": transaction.quantity,

                        "Date": transaction.transaction_date,

                        "Notes": transaction.notes or "—",

                    })

                history.sort(
                    key=lambda row: (
                        pd.Timestamp(row["Date"])
                        if row["Date"] is not None
                        else pd.Timestamp.min
                    ),
                    reverse=True,
                )

                st.dataframe(
                    pd.DataFrame(history),
                    use_container_width=True,
                    hide_index=True,
                )

                st.caption(
                    f"Total Transactions: {len(history)}"
                )

            else:

                st.info(
                    "No stock transactions have been recorded."
                )

        except Exception as error:

            st.error(
                f"Unable to load transaction history: {error}"
            )
