
import streamlit as st
import pandas as pd

from web_ui.components.common import (
    header,
    section_title,
    suppliers,
    products,
)


def render(inventory):

    # --------------------------------------------------
    # PAGE HEADER
    # --------------------------------------------------

    header(
        "Suppliers",
        "Manage supplier information and product relationships."
    )

    # --------------------------------------------------
    # FETCH DATA
    # --------------------------------------------------

    supplier_list = suppliers(inventory)
    product_list = products(inventory)

    # --------------------------------------------------
    # SUPPLIER OVERVIEW
    # --------------------------------------------------

    section_title("Supplier Overview")

    col1, col2 = st.columns(2)

    col1.metric(
        "Total Suppliers",
        len(supplier_list)
    )

    col2.metric(
        "Products Linked to Suppliers",
        sum(
            1 for p in product_list
            if p["supplier_id"] is not None
        )
    )

    # --------------------------------------------------
    # SUPPLIER TABS
    # --------------------------------------------------

    tab_list, tab_add = st.tabs([
        "Supplier Directory",
        "Add Supplier"
    ])

    # ==================================================
    # TAB 1: SUPPLIER DIRECTORY
    # ==================================================

    with tab_list:

        section_title("Supplier Directory")

        search = st.text_input(
            "Search suppliers",
            placeholder="Search by supplier or contact name...",
            key="suppliers_search_input"
        )

        search_term = search.strip().lower()

        filtered = [
            s for s in supplier_list
            if (
                search_term in (s["name"] or "").lower()
                or search_term in (s["contact_name"] or "").lower()
            )
        ]

        if filtered:

            supplier_data = []

            for supplier in filtered:

                linked_count = sum(
                    1 for p in product_list
                    if p["supplier_id"] == supplier["id"]
                )

                supplier_data.append({

                    "ID": supplier["id"],

                    "Supplier": supplier["name"],

                    "Contact": supplier["contact_name"] or "—",

                    "Email": supplier["email"] or "—",

                    "Phone": supplier["phone"] or "—",

                    "Products": linked_count,

                })

            st.dataframe(
                pd.DataFrame(supplier_data),
                use_container_width=True,
                hide_index=True,
            )

            st.caption(
                f"Showing {len(filtered)} of {len(supplier_list)} suppliers"
            )

        else:

            if supplier_list:
                st.info("No matching suppliers found.")
            else:
                st.info(
                    "No suppliers registered yet. Add your first supplier."
                )

    # ==================================================
    # TAB 2: ADD SUPPLIER
    # ==================================================

    with tab_add:

        section_title("Register Supplier")

        with st.form(
            "add_supplier_form",
            clear_on_submit=True
        ):

            name = st.text_input(
                "Supplier Name",
                placeholder="Enter supplier name",
                key="supplier_add_name"
            )

            contact = st.text_input(
                "Contact Person",
                placeholder="Enter contact person's name",
                key="supplier_add_contact"
            )

            email = st.text_input(
                "Email Address",
                placeholder="Enter email address",
                key="supplier_add_email"
            )

            phone = st.text_input(
                "Phone Number",
                placeholder="Enter phone number",
                key="supplier_add_phone"
            )

            address = st.text_area(
                "Address",
                placeholder="Enter supplier address",
                key="supplier_add_address"
            )

            submitted = st.form_submit_button(
                "Add Supplier",
                use_container_width=True,
            )

            if submitted:

                # Validate supplier name
                if not name.strip():

                    st.error(
                        "Supplier name is required."
                    )

                else:

                    try:

                        inventory.add_supplier(
                            name=name.strip(),
                            contact_name=contact.strip() or None,
                            email=email.strip() or None,
                            phone=phone.strip() or None,
                            address=address.strip() or None,
                        )

                        st.success(
                            "Supplier added successfully."
                        )

                        st.rerun()

                    except Exception as error:

                        error_message = str(error).lower()

                        if (
                            "unique constraint failed" in error_message
                            or "duplicate" in error_message
                        ):

                            st.error(
                                "A supplier with this information already exists."
                            )

                        else:

                            st.error(
                                f"Unable to add supplier: {error}"
                            )
