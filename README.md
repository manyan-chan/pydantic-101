# Pydantic 101 - Streamlit Showcase 🚀

## Overview

This project is an interactive Streamlit application designed to demonstrate the fundamental features and common use cases of the Pydantic library. It provides hands-on examples for understanding data validation, type coercion, model definition, error handling, and more within a web interface.

This application is ideal for anyone learning Pydantic or wanting a quick reference for its core concepts.

## Features Showcased

The app interactively demonstrates the following Pydantic features:

*   **Basic Validation:** Required fields, optional fields (`Optional`), default values, and simple constraints (`Field`, `gt`, `ge`).
*   **Type Coercion:** How Pydantic automatically converts input data (e.g., strings to numbers) where possible.
*   **Nested Models:** Defining models that contain other Pydantic models for structured data.
*   **Custom Validators:** Using `@model_validator` for validation logic involving multiple fields (e.g., checking date ranges).
*   **Computed Fields:** Dynamically calculating field values using `@computed_field`.
*   **Field Aliases:** Parsing data from sources with different naming conventions (e.g., `camelCase` to `snake_case`).
*   **Strict Types:** Using types like `StrictInt` to disable type coercion.
*   **Special String Types:** Built-in validation for common formats like `EmailStr` and `HttpUrl`.
*   **Enum Validation:** Restricting field values to members of a Python `Enum`.
*   **Model Configuration:** Using `ConfigDict` (Pydantic v2) to modify model behavior (e.g., `extra='forbid'`).
*   **Error Handling:** Clear display of `ValidationError` details when validation fails.
*   **JSON Schema Generation:** Viewing the JSON Schema automatically generated from the Pydantic models.


## Requirements

*   Python (Version 3.8 or higher recommended)
*   pip (Python package installer)

## Installation

1.  **Clone the repository or download the source code.**
2.  **Navigate to the project directory** in your terminal:
    ```bash
    cd path/to/your/pydantic-101
    ```
3.  **Install the required Python packages:**
    ```bash
    pip install streamlit 'pydantic[email]'
    ```
    *(Note: The quotes around `'pydantic[email]'` are important in some shells like Zsh to handle the square brackets correctly).*

## Usage

1.  Make sure you are in the project directory in your terminal.
2.  Run the Streamlit application using the following command:
    ```bash
    streamlit run app.py
    ```
3.  Streamlit will start the application and provide a local URL (usually `http://localhost:8501`) to open in your web browser.
4.  Interact with the different sections (expanders) in the web app to test various Pydantic features with valid and invalid inputs.

## Code Structure

*   `app.py` (or your script name): Contains the main Streamlit application code, including Pydantic model definitions and Streamlit UI elements.
