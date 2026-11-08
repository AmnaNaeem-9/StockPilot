
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
        "Products",
        "Manage your products and monitor their stock levels."
    )

    # --------------------------------------------------
    # FETCH DATA
    # --------------------------------------------------

    product_list = products(inventory)
    category_list = categories(inventory)
    supplier_list = suppliers(inventory)

    category_map = {
        c["id"]: c["name"] for c in category_list
    }

    supplier_map = {
        s["id"]: s["name"] for s in supplier_list
    }

    # --------------------------------------------------
    # PRODUCT OVERVIEW
    # --------------------------------------------------

    section_title("Product Overview")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Products",
        len(product_list)
    )

    c2.metric(
        "Total Units",
        sum(p["quantity"] for p in product_list)
    )

    c3.metric(
        "Inventory Value",
        money(
            sum(p["price"] * p["quantity"] for p in product_list)
        )
    )

    # --------------------------------------------------
    # PRODUCT TABS
    # --------------------------------------------------

    tab_list, tab_add, tab_edit = st.tabs([
        "Product List",
        "Add Product",
        "Edit / Delete Product",
    ])

    # ==================================================
    # TAB 1: PRODUCT LIST
    # ==================================================

    with tab_list:

        section_title("All Products")

        search = st.text_input(
            "Search products",
            placeholder="Search by name or SKU...",
            key="products_search_input"
        )

        filtered = [
            p for p in product_list
            if search.lower() in p["name"].lower()
            or search.lower() in p["sku"].lower()
        ]

        if filtered:

            st.dataframe(
                pd.DataFrame([
                    {
                        "ID": p["id"],
                        "Product": p["name"],
                        "SKU": p["sku"],
                        "Category": category_map.get(
                            p["category_id"], "Unknown"
                        ),
                        "Supplier": supplier_map.get(
                            p["supplier_id"], "Not assigned"
                        ),
                        "Price": money(p["price"]),
                        "Quantity": p["quantity"],
                        "Reorder Level": p["reorder_level"],
                        "Status": status(
                            p["quantity"],
                            p["reorder_level"]
                        ),
                    }
                    for p in filtered
                ]),
                use_container_width=True,
                hide_index=True,
            )

        else:
            st.info("No matching products found.")

    # ==================================================
    # TAB 2: ADD PRODUCT
    # ==================================================

    with tab_add:

        section_title("Add New Product")

        if not category_list:

            st.warning(
                "Create at least one category before adding a product."
            )

        else:

            with st.form(
                "add_product_form",
                clear_on_submit=True
            ):

                name = st.text_input(
                    "Product Name",
                    key="products_add_name"
                )

                sku = st.text_input(
                    "SKU",
                    key="products_add_sku"
                )

                description = st.text_area(
                    "Description",
                    key="products_add_description"
                )

                col1, col2 = st.columns(2)

                with col1:

                    price = st.number_input(
                        "Unit Price",
                        min_value=0.0,
                        step=1.0,
                        key="products_add_price"
                    )

                    quantity = st.number_input(
                        "Initial Quantity",
                        min_value=0,
                        step=1,
                        key="products_add_quantity"
                    )

                with col2:

                    reorder = st.number_input(
                        "Reorder Level",
                        min_value=0,
                        value=10,
                        step=1,
                        key="products_add_reorder"
                    )

                    category_options = {
                        c["name"]: c["id"]
                        for c in category_list
                    }

                    selected_category = st.selectbox(
                        "Category",
                        list(category_options.keys()),
                        key="products_add_category"
                    )

                    supplier_options = {
                        "No supplier": None,
                        **{
                            s["name"]: s["id"]
                            for s in supplier_list
                        },
                    }

                    selected_supplier = st.selectbox(
                        "Supplier",
                        list(supplier_options.keys()),
                        key="products_add_supplier"
                    )

                submitted = st.form_submit_button(
                    "Add Product",
                    use_container_width=True,
                    key="products_add_submit"
                )

                if submitted:

                    if not name.strip() or not sku.strip():

                        st.error(
                            "Product name and SKU are required."
                        )

                    else:

                        try:

                            inventory.add_product(
                                name=name.strip(),
                                sku=sku.strip(),
                                price=price,
                                quantity=int(quantity),
                                reorder_level=int(reorder),
                                category_id=category_options[
                                    selected_category
                                ],
                                supplier_id=supplier_options[
                                    selected_supplier
                                ],
                                description=description.strip() or None,
                            )

                            st.success(
                                "Product added successfully."
                            )

                            st.rerun()

                        except Exception as error:

                            error_message = str(error).lower()

                            if "unique constraint failed" in error_message:
                                st.error(
                                    "A product with this SKU already exists."
                                )
                            else:
                                st.error(
                                    f"Unable to add product: {error}"
                                )

    # ==================================================
    # TAB 3: EDIT / DELETE PRODUCT
    # ==================================================

    with tab_edit:

        section_title("Edit or Delete Product")

        if not product_list:

            st.info("There are no products to edit.")

        else:

            product_options = {
                f'{p["name"]} ({p["sku"]}) — ID {p["id"]}': p
                for p in product_list
            }

            selected_label = st.selectbox(
                "Select Product",
                list(product_options.keys()),
                key="products_edit_selector"
            )

            selected = product_options[selected_label]

            # Dynamic widget keys prevent conflicts when
            # switching between different products.

            product_id = selected["id"]

            with st.form(
                f"edit_product_form_{product_id}"
            ):

                name = st.text_input(
                    "Product Name",
                    value=selected["name"],
                    key=f"products_edit_name_{product_id}"
                )

                sku = st.text_input(
                    "SKU",
                    value=selected["sku"],
                    key=f"products_edit_sku_{product_id}"
                )

                description = st.text_area(
                    "Description",
                    value=selected["description"] or "",
                    key=f"products_edit_description_{product_id}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    price = st.number_input(
                        "Unit Price",
                        min_value=0.0,
                        value=float(selected["price"]),
                        step=1.0,
                        key=f"products_edit_price_{product_id}"
                    )

                    quantity = st.number_input(
                        "Quantity",
                        min_value=0,
                        value=int(selected["quantity"]),
                        step=1,
                        key=f"products_edit_quantity_{product_id}"
                    )

                with col2:

                    reorder = st.number_input(
                        "Reorder Level",
                        min_value=0,
                        value=int(selected["reorder_level"]),
                        step=1,
                        key=f"products_edit_reorder_{product_id}"
                    )

                    category_options = {
                        c["name"]: c["id"]
                        for c in category_list
                    }

                    current_category = category_map.get(
                        selected["category_id"],
                        list(category_options.keys())[0]
                    )

                    category = st.selectbox(
                        "Category",
                        list(category_options.keys()),
                        index=list(category_options.keys()).index(
                            current_category
                        ),
                        key=f"products_edit_category_{product_id}"
                    )

                    supplier_options = {
                        "No supplier": None,
                        **{
                            s["name"]: s["id"]
                            for s in supplier_list
                        },
                    }

                    current_supplier = supplier_map.get(
                        selected["supplier_id"],
                        "No supplier"
                    )

                    if current_supplier not in supplier_options:
                        current_supplier = "No supplier"

                    supplier = st.selectbox(
                        "Supplier",
                        list(supplier_options.keys()),
                        index=list(supplier_options.keys()).index(
                            current_supplier
                        ),
                        key=f"products_edit_supplier_{product_id}"
                    )

                update = st.form_submit_button(
                    "Save Changes",
                    use_container_width=True,
                    key=f"products_edit_submit_{product_id}"
                )

                if update:

                    if not name.strip() or not sku.strip():

                        st.error(
                            "Product name and SKU are required."
                        )

                    else:

                        try:

                            inventory.update_product(
                                selected["id"],
                                name=name.strip(),
                                sku=sku.strip(),
                                description=description.strip() or None,
                                price=price,
                                quantity=int(quantity),
                                reorder_level=int(reorder),
                                category_id=category_options[category],
                                supplier_id=supplier_options[supplier],
                            )

                            st.success(
                                "Product updated successfully."
                            )

                            st.rerun()

                        except Exception as error:

                            error_message = str(error).lower()

                            if "unique constraint failed" in error_message:
                                st.error(
                                    "This SKU is already assigned to another product."
                                )
                            else:
                                st.error(
                                    f"Unable to update product: {error}"
                                )

            # --------------------------------------------------
            # DELETE PRODUCT
            # --------------------------------------------------

            st.divider()

            st.warning(
                "Deleting a product may fail if it has existing stock transactions."
            )

            if st.button(
                "Delete Selected Product",
                type="secondary",
                key=f"products_delete_{product_id}"
            ):

                try:

                    inventory.delete_product(selected["id"])

                    st.success(
                        "Product deleted successfully."
                    )

                    st.rerun()

                except Exception as error:

                    st.error(
                        f"Unable to delete product: {error}"
                    )
