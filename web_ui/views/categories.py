
import streamlit as st


def render(inventory):

    """
    Categories page.
    Allows users to add categories and view existing categories.
    """

    # --------------------------------------------------
    # PAGE HEADER
    # --------------------------------------------------

    st.title("Category Management")

    st.caption(
        "Create and manage your inventory categories."
    )

    st.divider()

    # --------------------------------------------------
    # ADD NEW CATEGORY
    # --------------------------------------------------

    st.subheader("Add New Category")

    with st.form(
        "add_category_form",
        clear_on_submit=True
    ):

        category_name = st.text_input(
            "Category Name",
            placeholder="Enter category name",
            key="category_name_input"
        )

        category_description = st.text_area(
            "Description",
            placeholder="Enter category description (optional)",
            height=100,
            key="category_description_input"
        )

        submitted = st.form_submit_button(
            "Add Category",
            use_container_width=True,
        )

        if submitted:

            # Validate category name
            if not category_name.strip():

                st.error(
                    "Category name is required."
                )

            else:

                try:

                    inventory.add_category(
                        name=category_name.strip(),
                        description=category_description.strip() or None
                    )

                    st.success(
                        "Category created successfully!"
                    )

                    st.rerun()

                except Exception as error:

                    error_message = str(error).lower()

                    # Handle duplicate category names
                    if (
                        "unique constraint failed" in error_message
                        or "duplicate" in error_message
                    ):

                        st.error(
                            "A category with this name already exists. "
                            "Please enter a different category name."
                        )

                    else:

                        st.error(
                            f"Unable to create category: {error}"
                        )

    st.divider()

    # --------------------------------------------------
    # DISPLAY EXISTING CATEGORIES
    # --------------------------------------------------

    st.subheader("Category List")

    try:

        categories = inventory.get_all_categories()

        if not categories:

            st.info(
                "No categories found. Add your first category above."
            )

        else:

            category_data = []

            for category in categories:

                category_data.append({

                    "ID": category.id,

                    "Category Name": category.name,

                    "Description": category.description or "—",

                })

            st.dataframe(
                category_data,
                use_container_width=True,
                hide_index=True,
            )

            # Category count
            st.caption(
                f"Total Categories: {len(categories)}"
            )

    except Exception as error:

        st.error(
            f"Unable to display categories: {error}"
        )
