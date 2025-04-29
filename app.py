from datetime import date
from enum import Enum

# from pydantic import FieldValidationInfo # No longer needed
from typing import List, Optional

import streamlit as st
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    HttpUrl,
    StrictInt,
    ValidationError,
    computed_field,
    # field_validator, # No longer needed as Event class is removed
    model_validator,  # Used in EventImproved
)

# --- App Setup ---
st.set_page_config(page_title="Pydantic 101", layout="wide")
st.title("🚀 Pydantic 101: Feature Showcase")
st.caption("Exploring core Pydantic concepts with interactive examples.")

# --- Introduction ---
st.markdown("""
Pydantic enforces type hints at runtime, providing user-friendly errors when data is invalid.
It's widely used for data validation, serialization/deserialization, and settings management.

This app demonstrates several key features:
*   Basic Validation & Type Coercion
*   Nested Models
*   Custom Field Validators (`@model_validator` for cross-field checks)
*   Computed Fields
*   Field Aliases
*   Strict Types & Special String Types (Email, URL)
*   Enum Validation
*   Model Configuration (e.g., forbidding extra fields)
""")
st.markdown("---")


# --- Helper Function for Displaying Results ---
def display_validation_results(input_data, model_class):
    """Helper function to validate data and display results in Streamlit."""
    st.write("Raw Input Data:")
    st.json(input_data)
    try:
        # --- THE CORE PYDANTIC STEP ---
        validated_obj = model_class(**input_data)
        # -----------------------------
        st.success("✅ Validation Successful!")
        st.balloons()
        st.write("Validated Pydantic Object:")
        st.json(validated_obj.model_dump())

        # --- FIX: Removed the nested expander ---
        # Display JSON Schema directly if validation succeeds
        st.write("JSON Schema for this model:")
        # Use model_json_schema for Pydantic V2 (use .schema() for V1)
        st.json(model_class.model_json_schema())
        # --- End Fix ---

        return True

    except ValidationError as e:
        st.error("❌ Validation Failed!")
        st.write("Pydantic Validation Errors:")
        # e.errors() provides structured error details
        st.json(e.errors())
        return False
    except Exception as ex:
        # This reports unexpected errors during the Pydantic validation step itself
        st.error(f"An unexpected error occurred during validation/processing: {ex}")
        return False  # Indicate failure


# --- 1. Basic Validation ---
with st.expander("1. Basic Validation, Defaults & Optional Fields", expanded=True):
    st.markdown("""
    Demonstrates required fields (`name`, `price`), optional fields (`description`),
    default values (`quantity`, `tags`), type coercion (text input for numbers),
    and simple constraints (`gt=0`, `ge=0`).
    """)

    # Model Definition
    class Item(BaseModel):
        name: str
        description: Optional[str] = None
        price: float = Field(..., gt=0)
        quantity: int = Field(default=1, ge=0)
        tags: List[str] = []

    st.code(
        """
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0) # ... means required, gt=0 means > 0
    quantity: int = Field(default=1, ge=0) # ge=0 means >= 0
    tags: List[str] = []
    """,
        language="python",
    )

    # Input Form
    col1, col2 = st.columns(2)
    with col1:
        basic_name = st.text_input(
            "Name (string, required)", "Gadget", key="basic_name"
        )
        basic_price = st.text_input(
            "Price (float, required, > 0)", "19.99", key="basic_price"
        )
        basic_desc = st.text_area(
            "Description (string, optional)", "A cool gadget.", key="basic_desc"
        )
    with col2:
        basic_qty = st.text_input(
            "Quantity (integer, default=1, >= 0)", "1", key="basic_qty"
        )
        basic_tags = st.text_input(
            "Tags (comma-separated strings)", "tech, cool", key="basic_tags"
        )

    if st.button("Validate Basic Item", key="basic_validate"):
        tags_list = [tag.strip() for tag in basic_tags.split(",") if tag.strip()]
        input_data = {
            "name": basic_name,
            "description": basic_desc if basic_desc else None,
            "price": basic_price,
            "quantity": basic_qty,
            "tags": tags_list,
        }
        display_validation_results(input_data, Item)

st.markdown("---")

# --- 2. Nested Models ---
with st.expander("2. Nested Models"):
    st.markdown("""
    Pydantic models can contain other Pydantic models, allowing for complex, structured data validation.
    Here, `User` contains an `Address` object.
    """)

    # Model Definitions
    class Address(BaseModel):
        street: str
        city: str
        # FIX: Use raw string for regex pattern
        zip_code: str = Field(..., pattern=r"^\d{5}(-\d{4})?$")

    class User(BaseModel):
        username: str
        email: EmailStr  # Requires 'email-validator' package
        address: Address
        hobbies: List[str] = []

    st.code(
        r"""
from pydantic import BaseModel, Field, EmailStr

class Address(BaseModel):
    street: str
    city: str
    # Use raw string r"..." for regex patterns
    zip_code: str = Field(..., pattern=r"^\d{5}(-\d{4})?$") # US Zip code regex

class User(BaseModel):
    username: str
    email: EmailStr # Requires 'email-validator' package
    address: Address # Nested Pydantic model
    hobbies: List[str] = []
    """,
        language="python",
    )

    # Input Form
    col1, col2 = st.columns(2)
    with col1:
        nested_user = st.text_input("Username", "john_doe", key="nested_user")
        nested_email = st.text_input(
            "Email", "john.doe@example.com", key="nested_email"
        )
        nested_hobbies = st.text_input(
            "Hobbies (comma-separated)", "coding, hiking", key="nested_hobbies"
        )
    with col2:
        nested_street = st.text_input("Street", "123 Main St", key="nested_street")
        nested_city = st.text_input("City", "Anytown", key="nested_city")
        nested_zip = st.text_input(
            "Zip Code (e.g., 12345 or 12345-6789)", "98765", key="nested_zip"
        )

    if st.button("Validate Nested User", key="nested_validate"):
        hobbies_list = [h.strip() for h in nested_hobbies.split(",") if h.strip()]
        input_data = {
            "username": nested_user,
            "email": nested_email,
            "hobbies": hobbies_list,
            "address": {
                "street": nested_street,
                "city": nested_city,
                "zip_code": nested_zip,
            },
        }
        display_validation_results(input_data, User)

st.markdown("---")

# --- 3. Custom Validators ---
with st.expander(
    "3. Custom Model Validators (`@model_validator`)"
):  # Updated title slightly
    st.markdown("""
    Use `@model_validator` (Pydantic v2) for validation logic involving multiple fields.
    Here, we ensure `end_date` is not before `start_date`. This is often preferred over
    `@field_validator` for cross-field checks.
    """)

    # Model Definition (Using the improved version directly)
    class EventImproved(BaseModel):
        name: str
        start_date: date
        end_date: date

        @model_validator(mode="after")
        def check_dates_model(self) -> "EventImproved":
            if self.start_date and self.end_date and self.end_date < self.start_date:
                raise ValueError("End date cannot be before start date")
            return self

    st.code(
        """
from datetime import date
from pydantic import BaseModel, model_validator

class EventImproved(BaseModel):
    name: str
    start_date: date
    end_date: date

    @model_validator(mode='after') # Runs after individual field validation
    def check_dates_model(self) -> 'EventImproved':
        # 'self' has access to all validated fields here
        if self.start_date and self.end_date and self.end_date < self.start_date:
                raise ValueError('End date cannot be before start date')
        return self
        """,
        language="python",
    )

    # Input Form
    col1, col2, col3 = st.columns(3)
    with col1:
        validator_name = st.text_input("Event Name", "Conference", key="validator_name")
    with col2:
        validator_start = st.date_input(
            "Start Date", date.today(), key="validator_start"
        )
    with col3:
        validator_end = st.date_input("End Date", date.today(), key="validator_end")

    if st.button("Validate Event Dates", key="validator_validate"):
        input_data = {
            "name": validator_name,
            "start_date": validator_start,
            "end_date": validator_end,
        }
        display_validation_results(input_data, EventImproved)  # Use the improved model

st.markdown("---")


# --- 4. Computed Fields ---
with st.expander("4. Computed Fields (`@computed_field`)"):
    st.markdown("""
    Define fields that are calculated dynamically from other fields using `@computed_field` (Pydantic v2).
    The `total_cost` is computed based on `price` and `quantity`.
    """)

    # Model Definition
    class OrderItem(BaseModel):
        item_name: str
        price: float = Field(..., gt=0)
        quantity: int = Field(..., ge=1)

        @computed_field
        @property
        def total_cost(self) -> float:
            return self.price * self.quantity

    st.code(
        """
from pydantic import BaseModel, Field, computed_field

class OrderItem(BaseModel):
    item_name: str
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=1)

    @computed_field
    @property # Remember to include @property with @computed_field
    def total_cost(self) -> float:
        return self.price * self.quantity
    """,
        language="python",
    )

    # Input Form
    col1, col2, col3 = st.columns(3)
    with col1:
        computed_name = st.text_input("Item Name", "Laptop", key="computed_name")
    with col2:
        computed_price = st.number_input(
            "Price", min_value=0.01, value=1200.0, step=10.0, key="computed_price"
        )
    with col3:
        computed_qty = st.number_input(
            "Quantity", min_value=1, value=1, step=1, key="computed_qty"
        )

    if st.button("Validate Order Item & Compute Total", key="computed_validate"):
        input_data = {
            "item_name": computed_name,
            "price": computed_price,
            "quantity": computed_qty,
        }
        st.write("Raw Input Data:")
        st.json(input_data)
        try:
            validated_obj = OrderItem(**input_data)
            st.success("✅ Validation Successful!")
            st.balloons()
            st.write("Validated Pydantic Object (includes `total_cost`):")
            st.json(validated_obj.model_dump())
        except ValidationError as e:
            st.error("❌ Validation Failed!")
            st.write("Pydantic Validation Errors:")
            st.json(e.errors())
        except Exception as ex:
            st.error(f"An unexpected error occurred: {ex}")


st.markdown("---")


# --- 5. Field Aliases ---
with st.expander("5. Field Aliases (`Field(alias=...)`)"):
    st.markdown("""
    Pydantic can parse data from fields with different names than your model attributes using `alias`.
    This is useful when dealing with APIs or data sources using `camelCase` or other conventions.
    Input uses `productId` and `itemName`, model uses `product_id` and `item_name`.
    """)

    # Model Definition
    class Product(BaseModel):
        product_id: int = Field(..., alias="productId")
        item_name: str = Field(..., alias="itemName")
        stock_count: int = Field(..., alias="stockCount", ge=0)

    st.code(
        """
from pydantic import BaseModel, Field

class Product(BaseModel):
    # Python uses snake_case, input might use camelCase
    product_id: int = Field(..., alias='productId')
    item_name: str = Field(..., alias='itemName')
    stock_count: int = Field(..., alias='stockCount', ge=0)
    """,
        language="python",
    )

    # Input Form
    col1, col2, col3 = st.columns(3)
    with col1:
        alias_id = st.text_input("productId (Input uses alias)", "101", key="alias_id")
    with col2:
        alias_name = st.text_input(
            "itemName (Input uses alias)", "Wireless Mouse", key="alias_name"
        )
    with col3:
        alias_stock = st.text_input(
            "stockCount (Input uses alias)", "50", key="alias_stock"
        )

    if st.button("Validate Product with Aliases", key="alias_validate"):
        input_data = {
            "productId": alias_id,
            "itemName": alias_name,
            "stockCount": alias_stock,
        }
        was_valid = display_validation_results(input_data, Product)

        if was_valid:
            try:
                validated_obj = Product(**input_data)
                st.write(
                    "Object serialized back using aliases (`model_dump(by_alias=True)`):"
                )
                st.json(validated_obj.model_dump(by_alias=True))
            except Exception:
                pass


st.markdown("---")


# --- 6. Strict Types & Special Strings ---
with st.expander("6. Strict Types & Special String Types"):
    st.markdown("""
    Pydantic offers `StrictInt`, `StrictFloat`, `StrictStr`, `StrictBool` which disable type coercion.
    It also provides special types like `EmailStr` (validates email format) and `HttpUrl` (validates URL format).
    Try entering `"123"` (string) for `Strict User ID` - it will fail.
    """)

    # Model Definition
    class StrictData(BaseModel):
        strict_user_id: StrictInt  # No coercion from "123" allowed
        user_email: EmailStr  # Validates email format
        website: Optional[HttpUrl] = None  # Validates URL, optional

    st.code(
        """
from pydantic import BaseModel, StrictInt, EmailStr, HttpUrl
from typing import Optional

class StrictData(BaseModel):
    strict_user_id: StrictInt # No coercion from "123" allowed
    user_email: EmailStr       # Validates email format (requires 'email-validator')
    website: Optional[HttpUrl] = None # Validates URL, optional
    """,
        language="python",
    )

    # Input Form
    col1, col2, col3 = st.columns(3)
    with col1:
        strict_id_input = st.text_input(
            "Strict User ID (StrictInt)", "123", key="strict_id"
        )
    with col2:
        strict_email = st.text_input(
            "User Email (EmailStr)", "test@example.com", key="strict_email"
        )
    with col3:
        strict_url = st.text_input(
            "Website (HttpUrl, Optional)", "https://pydantic.dev", key="strict_url"
        )

    if st.button("Validate Strict/Special Types", key="strict_validate"):
        try:
            strict_id_value = int(strict_id_input)
        except ValueError:
            strict_id_value = strict_id_input  # Keep as string if conversion fails

        input_data = {
            "strict_user_id": strict_id_value,
            "user_email": strict_email,
            "website": strict_url if strict_url else None,
        }
        display_validation_results(input_data, StrictData)


st.markdown("---")


# --- 7. Enum Validation ---
with st.expander("7. Enum Validation"):
    st.markdown("""
    Restrict field values to a predefined set using Python's standard `Enum`.
    Pydantic validates that the input matches one of the enum members.
    """)

    # Enum Definition
    class TaskStatus(str, Enum):
        PENDING = "pending"
        RUNNING = "running"
        COMPLETED = "completed"
        FAILED = "failed"

    # Model Definition
    class Task(BaseModel):
        task_id: str
        status: TaskStatus

    st.code(
        """
from enum import Enum
from pydantic import BaseModel

class TaskStatus(str, Enum): # Inheriting from str is common
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class Task(BaseModel):
    task_id: str
    status: TaskStatus # Field type is the Enum
    """,
        language="python",
    )

    # Input Form
    col1, col2 = st.columns(2)
    with col1:
        enum_task_id = st.text_input("Task ID", "task-abc-123", key="enum_id")
    with col2:
        enum_status_options = [status.value for status in TaskStatus]
        enum_status = st.selectbox(
            "Status (Enum)", options=enum_status_options, key="enum_status"
        )
        enum_allow_invalid = st.checkbox(
            "Try invalid status ('unknown')?", key="enum_invalid_toggle"
        )
        if enum_allow_invalid:
            enum_status = "unknown"
            st.warning("Attempting validation with invalid status 'unknown'")

    if st.button("Validate Task Status (Enum)", key="enum_validate"):
        input_data = {
            "task_id": enum_task_id,
            "status": enum_status,
        }
        display_validation_results(input_data, Task)


st.markdown("---")


# --- 8. Model Configuration ---
with st.expander("8. Model Configuration (`ConfigDict`, `extra='forbid'`)"):
    st.markdown("""
    Configure model behavior using `ConfigDict` (Pydantic v2) or `class Config` (Pydantic v1).
    `extra='forbid'` prevents unexpected fields from being passed during validation.
    """)

    # Model Definition
    class ConfiguredModel(BaseModel):
        model_config = ConfigDict(extra="forbid")

        expected_field: str
        optional_field: Optional[int] = None

    st.code(
        """
from pydantic import BaseModel, ConfigDict
from typing import Optional

class ConfiguredModel(BaseModel):
    model_config = ConfigDict(extra='forbid') # Pydantic v2 config

    expected_field: str
    optional_field: Optional[int] = None

# Pydantic v1 equivalent:
# class ConfiguredModelV1(BaseModel):
#     expected_field: str
#     optional_field: Optional[int] = None
#
#     class Config:
#         extra = 'forbid'
    """,
        language="python",
    )

    # Input Form
    config_expected = st.text_input(
        "Expected Field", "some value", key="config_expected"
    )
    config_optional = st.number_input(
        "Optional Field (int)", value=None, step=1, key="config_optional"
    )
    config_add_extra = st.checkbox(
        "Add an unexpected 'extra_field'?", key="config_extra_toggle"
    )

    if st.button("Validate with Model Config", key="config_validate"):
        input_data = {
            "expected_field": config_expected,
            "optional_field": config_optional,
        }
        if config_add_extra:
            input_data["extra_field"] = "this should not be allowed"
            st.warning("Attempting validation with an extra field.")

        display_validation_results(input_data, ConfiguredModel)


st.markdown("---")
st.info(
    "Explore the code and try different inputs (valid and invalid) to see Pydantic in action!"
)
