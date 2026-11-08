
import html

import streamlit as st
import pandas as pd


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

def header(title, description):

    safe_title = html.escape(str(title))
    safe_description = html.escape(str(description))

    st.markdown(
        f"""
        <div class="page-heading">
            <h1>{safe_title}</h1>
            <p>{safe_description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# SECTION TITLE
# --------------------------------------------------

def section_title(title, description=None):

    safe_title = html.escape(str(title))

    st.markdown(
        f'<div class="section-title">{safe_title}</div>',
        unsafe_allow_html=True,
    )

    if description:

        safe_description = html.escape(str(description))

        st.markdown(
            f'<div class="section-description">{safe_description}</div>',
            unsafe_allow_html=True,
        )


# --------------------------------------------------
# METRIC CARD
# --------------------------------------------------

def metric_card(label, value, note=None):

    safe_label = html.escape(str(label))
    safe_value = html.escape(str(value))

    note_html = ""

    if note:

        safe_note = html.escape(str(note))

        note_html = (
            f'<div class="metric-note">{safe_note}</div>'
        )

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{safe_label}</div>
            <div class="metric-value">{safe_value}</div>
            {note_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# PANEL HELPERS
# --------------------------------------------------

def panel_start(title, description=None):

    safe_title = html.escape(str(title))

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="panel-title">{safe_title}</div>',
        unsafe_allow_html=True,
    )

    if description:

        safe_description = html.escape(str(description))

        st.markdown(
            f'<div class="panel-description">{safe_description}</div>',
            unsafe_allow_html=True,
        )


def panel_end():

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# PRODUCT DATA
# --------------------------------------------------

def products(inventory):

    result = []

    for product in inventory.get_all_products():

        result.append({

            "id": product.id,

            "name": product.name or "",

            "sku": product.sku or "",

            "price": float(product.price or 0),

            "quantity": int(product.quantity or 0),

            "reorder_level": int(product.reorder_level or 0),

            "category_id": product.category_id,

            "supplier_id": product.supplier_id,

            "description": product.description or "",

        })

    return result


# --------------------------------------------------
# CATEGORY DATA
# --------------------------------------------------

def categories(inventory):

    return [

        {

            "id": item.id,

            "name": item.name or "",

            "description": item.description or "",

        }

        for item in inventory.get_all_categories()

    ]


# --------------------------------------------------
# SUPPLIER DATA
# --------------------------------------------------

def suppliers(inventory):

    return [

        {

            "id": item.id,

            "name": item.name or "",

            "contact_name": item.contact_name or "",

            "email": item.email or "",

            "phone": item.phone or "",

            "address": item.address or "",

        }

        for item in inventory.get_all_suppliers()

    ]


# --------------------------------------------------
# STOCK STATUS
# --------------------------------------------------

def status(quantity, reorder_level):

    quantity = int(quantity or 0)

    reorder_level = int(reorder_level or 0)

    if quantity <= 0:

        return "Out of Stock"

    if quantity <= reorder_level:

        return "Low Stock"

    return "Healthy"


# --------------------------------------------------
# CURRENCY FORMATTING
# --------------------------------------------------

def money(value):

    return f"${float(value or 0):,.2f}"


# --------------------------------------------------
# REUSABLE DATA TABLE
# --------------------------------------------------

def show_table(data, empty_message="No records found."):

    if data is None or len(data) == 0:

        st.info(empty_message)

        return

    st.dataframe(
        pd.DataFrame(data),
        use_container_width=True,
        hide_index=True,
    )


# --------------------------------------------------
# PRODUCT NAME LOOKUP
# --------------------------------------------------

def product_name_map(inventory):

    return {

        item["id"]: item["name"]

        for item in products(inventory)

    }


# --------------------------------------------------
# CATEGORY NAME LOOKUP
# --------------------------------------------------

def category_name_map(inventory):

    return {

        item["id"]: item["name"]

        for item in categories(inventory)

    }


# --------------------------------------------------
# SUPPLIER NAME LOOKUP
# --------------------------------------------------

def supplier_name_map(inventory):

    return {

        item["id"]: item["name"]

        for item in suppliers(inventory)

    }


# --------------------------------------------------
# FLASH MESSAGES
# --------------------------------------------------

def flash(message, message_type="success"):

    if message_type == "error":

        st.error(message)

    elif message_type == "warning":

        st.warning(message)

    else:

        st.success(message)
