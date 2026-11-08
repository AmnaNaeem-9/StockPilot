
import streamlit as st

from dotenv import load_dotenv

from ai.groq_client import GroqAIClient

from web_ui.components.common import (
    header,
    section_title,
    products,
    status,
)


# --------------------------------------------------
# ENVIRONMENT CONFIGURATION
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# AI CLIENT
# --------------------------------------------------

@st.cache_resource
def get_ai_client():
    return GroqAIClient()


# --------------------------------------------------
# AI INSIGHTS PAGE
# --------------------------------------------------

def render(inventory):

    # --------------------------------------------------
    # PAGE HEADER
    # --------------------------------------------------

    header(
        "AI Insights",
        "Use AI to understand stock risks and ask questions about your inventory.",
    )

    # --------------------------------------------------
    # FETCH INVENTORY DATA
    # --------------------------------------------------

    product_list = products(inventory)

    total_products = len(product_list)

    total_value = sum(
        p["price"] * p["quantity"]
        for p in product_list
    )

    low_stock = [
        p for p in product_list
        if 0 < p["quantity"] <= p["reorder_level"]
    ]

    out_of_stock = [
        p for p in product_list
        if p["quantity"] <= 0
    ]

    # --------------------------------------------------
    # INVENTORY OVERVIEW
    # --------------------------------------------------

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Products",
        total_products
    )

    c2.metric(
        "Low Stock",
        len(low_stock)
    )

    c3.metric(
        "Out of Stock",
        len(out_of_stock)
    )

    # --------------------------------------------------
    # INVENTORY SUMMARY FOR AI
    # --------------------------------------------------

    inventory_summary = {
        "total_products": total_products,
        "inventory_value": total_value,
        "low_stock_count": len(low_stock),
        "out_of_stock_count": len(out_of_stock),
        "low_stock_products": low_stock,
        "out_of_stock_products": out_of_stock,
    }

    # ==================================================
    # SECTION 1: INVENTORY RISK OVERVIEW
    # ==================================================

    section_title("Inventory Risk Overview")

    if out_of_stock:

        st.error(
            f"{len(out_of_stock)} product(s) are currently out of stock."
        )

    elif low_stock:

        st.warning(
            f"{len(low_stock)} product(s) are below or at their reorder level."
        )

    else:

        st.success(
            "No low-stock or out-of-stock products detected."
        )

    # Display products requiring attention

    if low_stock or out_of_stock:

        attention = out_of_stock + low_stock

        attention_data = []

        for p in attention:

            attention_data.append({

                "Product": p["name"],

                "SKU": p["sku"],

                "Quantity": p["quantity"],

                "Reorder Level": p["reorder_level"],

                "Status": status(
                    p["quantity"],
                    p["reorder_level"]
                ),

            })

        st.dataframe(
            attention_data,
            use_container_width=True,
            hide_index=True,
        )

    # ==================================================
    # SECTION 2: AI INVENTORY RECOMMENDATIONS
    # ==================================================

    section_title("AI Recommendations")

    # -----------------------------------------------
    # GENERATE INVENTORY INSIGHTS
    # -----------------------------------------------

    if st.button(
        "Generate Inventory Insights",
        use_container_width=True,
        key="ai_generate_inventory_insights",
    ):

        try:

            with st.spinner("Analyzing your inventory..."):

                client = get_ai_client()

                insights = client.get_inventory_insights(
                    inventory_summary
                )

                st.session_state[
                    "stockpilot_inventory_insights"
                ] = insights

        except Exception as error:

            st.error(
                f"Unable to generate inventory insights: {error}"
            )

    # Display generated insights

    insights = st.session_state.get(
        "stockpilot_inventory_insights"
    )

    if insights:

        st.markdown(insights)

    # -----------------------------------------------
    # GENERATE RESTOCK SUGGESTIONS
    # -----------------------------------------------

    if st.button(
        "Generate Restock Suggestions",
        use_container_width=True,
        key="ai_generate_restock_suggestions",
    ):

        if not low_stock and not out_of_stock:

            st.success(
                "All products have sufficient stock. "
                "No restocking is currently required."
            )

        else:

            try:

                with st.spinner("Preparing restock suggestions..."):

                    client = get_ai_client()

                    suggestions = client.get_restock_suggestions(
                        low_stock + out_of_stock
                    )

                    st.session_state[
                        "stockpilot_restock_suggestions"
                    ] = suggestions

            except Exception as error:

                st.error(
                    f"Unable to generate restock suggestions: {error}"
                )

    # Display generated restock suggestions

    suggestions = st.session_state.get(
        "stockpilot_restock_suggestions"
    )

    if suggestions:

        st.markdown(suggestions)

    # ==================================================
    # SECTION 3: INVENTORY AI CHATBOT
    # ==================================================

    st.divider()

    section_title("Ask Your Inventory Assistant")

    # -----------------------------------------------
    # INITIALIZE CHAT HISTORY
    # -----------------------------------------------

    if "stockpilot_chat_history" not in st.session_state:

        st.session_state.stockpilot_chat_history = []

    # -----------------------------------------------
    # DISPLAY PREVIOUS MESSAGES
    # -----------------------------------------------

    for message in st.session_state.stockpilot_chat_history:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # -----------------------------------------------
    # CHAT INPUT
    # -----------------------------------------------

    question = st.chat_input(
        "Ask a question about your inventory...",
        key="stockpilot_inventory_chat_input",
    )

    if question:

        # Save user message

        st.session_state.stockpilot_chat_history.append({

            "role": "user",

            "content": question,

        })

        with st.chat_message("user"):

            st.markdown(question)

        # -------------------------------------------
        # GET AI RESPONSE
        # -------------------------------------------

        try:

            with st.chat_message("assistant"):

                with st.spinner("Thinking..."):

                    client = get_ai_client()

                    answer = client.ask_custom_question(
                        question=question,
                        inventory_context=inventory_summary,
                        conversation_history=(
                            st.session_state.stockpilot_chat_history[-10:]
                        ),
                    )

                    st.markdown(answer)

            # Save assistant response

            st.session_state.stockpilot_chat_history.append({

                "role": "assistant",

                "content": answer,

            })

        except Exception as error:

            st.error(
                f"Unable to contact the AI assistant: {error}"
            )
