
import os
from groq import Groq


class GroqAIClient:
    """
    Handles AI interactions through the Groq API.
    Used by StockPilot to generate inventory insights,
    restocking suggestions, and answers to custom questions.
    """

    MODEL = "openai/gpt-oss-120b"

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise EnvironmentError(
                "GROQ_API_KEY not found. Add it to your .env file."
            )

        self.client = Groq(api_key=api_key)

    # -----------------------------------------------------
    # RESTOCK SUGGESTIONS
    # -----------------------------------------------------

    def get_restock_suggestions(self, low_stock_products: list) -> str:
        """
        Generate restocking recommendations for low-stock products.
        """

        if not low_stock_products:
            return "All products are sufficiently stocked. No restock needed."

        product_lines = "\n".join([
            f"- {p['name']} (SKU: {p['sku']}) | "
            f"Current Stock: {p['quantity']} | "
            f"Reorder Level: {p['reorder_level']}"
            for p in low_stock_products
        ])

        prompt = f"""
You are an inventory management assistant.

The following products need attention:

{product_lines}

For each product:
1. Suggest a reasonable restock quantity.
2. Explain the reason for your suggestion.
3. Flag critical items (quantity = 0 or significantly below reorder level).

Keep your response clear and concise. Use bullet points.
"""

        return self._call_api(prompt)

    # -----------------------------------------------------
    # INVENTORY INSIGHTS
    # -----------------------------------------------------

    def get_inventory_insights(self, inventory_summary: dict) -> str:
        """
        Generate an overall inventory health assessment.
        """

        products = inventory_summary.get("products", [])

        product_lines = "\n".join([
            f"- {p['name']} | Qty: {p['quantity']} | "
            f"Price: ${p['price']:.2f} | "
            f"Reorder at: {p['reorder_level']}"
            for p in products[:15]
        ])

        prompt = f"""
You are an inventory management assistant.

CURRENT INVENTORY OVERVIEW:

Total Products: {inventory_summary.get('total_products', 0)}
Total Categories: {inventory_summary.get('total_categories', 0)}
Total Suppliers: {inventory_summary.get('total_suppliers', 0)}
Low Stock Items: {inventory_summary.get('low_stock_count', 0)}
Total Value: ${inventory_summary.get('inventory_value', 0):,.2f}

PRODUCT DETAILS:
{product_lines}

Please provide:
1. An overall inventory health assessment.
2. Key observations about overstocked or understocked items.
3. Two or three actionable recommendations.

Be concise and use clear headings.
"""

        return self._call_api(prompt)

    # -----------------------------------------------------
    # CUSTOM QUESTION / AI CHAT
    # -----------------------------------------------------

    def ask_custom_question(
        self,
        question: str,
        inventory_context: dict,
        conversation_history: list = None
    ) -> str:
        """
        Answer inventory questions using current inventory data
        and previous conversation messages.
        """

        products = inventory_context.get("products", [])

        product_lines = "\n".join([
            f"- {p['name']} (SKU: {p['sku']}) | "
            f"Qty: {p['quantity']} | "
            f"Price: ${p['price']:.2f} | "
            f"Reorder Level: {p['reorder_level']}"
            for p in products[:30]
        ])

        prompt = f"""
You are StockPilot AI, an intelligent inventory management assistant.

CURRENT INVENTORY CONTEXT:

Total Products: {inventory_context.get('total_products', 0)}
Total Categories: {inventory_context.get('total_categories', 0)}
Total Suppliers: {inventory_context.get('total_suppliers', 0)}
Total Inventory Value: ${inventory_context.get('inventory_value', 0):,.2f}
Low Stock Items: {inventory_context.get('low_stock_count', 0)}

PRODUCT DETAILS:
{product_lines}

Answer the user's question based on the inventory information.

Rules:
- Do not invent product details, quantities, or supplier information.
- If information is unavailable, say so clearly.
- Use the previous conversation to understand follow-up questions.
- Prioritize the latest inventory data.
"""

        messages = [
            {
                "role": "system",
                "content": (
                    "You are StockPilot AI, a professional inventory "
                    "management assistant. Remember the conversation "
                    "context and understand follow-up questions. "
                    "Always prioritize the latest inventory data."
                )
            }
        ]

        # Include recent conversation messages.
        if conversation_history:
            messages.extend(conversation_history[-10:])

        # Add the current question.
        messages.append({
            "role": "user",
            "content": prompt + "\n\nCurrent Question: " + question
        })

        try:
            response = self.client.chat.completions.create(
                model=self.MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=1024
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"API Error: {str(e)}"

    # -----------------------------------------------------
    # INTERNAL API CALL
    # -----------------------------------------------------

    def _call_api(self, prompt: str) -> str:
        """
        Send a prompt to Groq and return the generated response.
        """

        try:
            response = self.client.chat.completions.create(
                model=self.MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful inventory management assistant. "
                            "Give clear, practical, and concise responses. "
                            "Always base your answers on the data provided."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1024
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"API Error: {str(e)}"
