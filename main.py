import streamlit as st
import google.generativeai as genai

# Embedded CSS
CSS = """
<style>
    /* Base styling */
    .stApp {
        background: linear-gradient(45deg, #1a1a2e 0%, #16213e 100%);
        min-height: 100vh;
        padding: 2rem;
    }

    /* Main container */
    .main {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(16px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        margin: 0 auto;
        max-width: 800px;
    }

    /* Title styling */
    h1 {
        color: #fff !important;
        font-family: 'Segoe UI', system-ui;
        text-align: center;
        font-size: 2.5rem !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        margin-bottom: 2rem !important;
    }

   /* Select boxes */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: #fff !important;
        padding: 20px !important; /* Increased padding for larger size */
        transition: all 0.3s ease;
        text-align: left !important;
        display: flex !important;
        align-items: center !important;
    }



    .stSelectbox > div > div:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        transform: translateY(-2px);
    }

    /* Number input */
    .stNumberInput input {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: #fff !important;
        padding: 14px !important;
        font-size: 1.1rem !important;
    }

    .stNumberInput input:focus {
        box-shadow: 0 0 0 2px rgba(100, 150, 255, 0.5) !important;
        border-color: #6496ff !important;
    }

    /* Convert button */
    .stButton > button {
        background: linear-gradient(135deg, #6496ff 0%, #7b61ff 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        color: #fff !important;
        font-weight: 600 !important;
        padding: 16px 32px !important;
        font-size: 1.1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin: 1.5rem 0 !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(100, 150, 255, 0.3) !important;
        background: linear-gradient(135deg, #7b61ff 0%, #6496ff 100%) !important;
    }

    /* Result display */
    .stAlert {
        background: rgba(40, 167, 69, 0.15) !important;
        border: 1px solid rgba(40, 167, 69, 0.3) !important;
        border-radius: 12px !important;
        color: #fff !important;
        font-size: 1.2rem !important;
        backdrop-filter: blur(4px);
    }

    .stAlert [data-testid="stMarkdownContainer"] {
        color: #fff !important;
    }

    /* Error message */
    .stAlert.error {
        background: rgba(220, 53, 69, 0.15) !important;
        border: 1px solid rgba(220, 53, 69, 0.3) !important;
    }

    /* Category selector */
    .st-bd {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 4px;
    }
</style>
"""


st.markdown(CSS, unsafe_allow_html=True)

# Removed duplicate convert_units function

def ai_assistant(prompt):
    genai.configure(api_key="AIzaSyApB27mnq96xXGUYNv39IJs1sC7PDqvcjk")
    model = genai.GenerativeModel('gemini-2.0-flash')
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"

def convert_units(value, from_unit, to_unit, unit_type):
    conversion_factors = {
        'length': {
            'meter': 1,
            'kilometer': 1000,
            'centimeter': 0.01,
            'millimeter': 0.001,
            'mile': 1609.34,
            'yard': 0.9144,
            'foot': 0.3048,
            'inch': 0.0254
        },
        'weight': {
            'kilogram': 1,
            'gram': 0.001,
            'milligram': 1e-6,
            'pound': 0.453592,
            'ounce': 0.0283495,
            'tonne': 1000
        },
        'temperature': {
            'celsius': {'offset': 0, 'ratio': 1},
            'fahrenheit': {'offset': 32, 'ratio': 5/9},
            'kelvin': {'offset': 273.15, 'ratio': 1}
        },
        'area': {
            'square meter': 1,
            'square kilometer': 1e6,
            'square mile': 2589988.11,
            'square foot': 0.092903,
            'acre': 4046.86,
            'hectare': 10000
        },
        'volume': {
            'liter': 1,
            'milliliter': 0.001,
            'cubic meter': 1000,
            'gallon': 3.78541,
            'quart': 0.946353,
            'pint': 0.473176,
            'cup': 0.24
        },
        'time': {
            'second': 1,
            'minute': 60,
            'hour': 3600,
            'day': 86400,
            'week': 604800,
            'month': 2629746,
            'year': 31556952
        }
    }

    if unit_type == 'temperature':
        # Temperature conversion logic
        if from_unit == 'celsius':
            kelvin = value + 273.15
        elif from_unit == 'fahrenheit':
            kelvin = (value - 32) * 5/9 + 273.15
        else:
            kelvin = value

        if to_unit == 'celsius':
            return kelvin - 273.15
        elif to_unit == 'fahrenheit':
            return (kelvin - 273.15) * 9/5 + 32
        else:
            return kelvin
    else:
        # Standard conversion logic
        factor = conversion_factors[unit_type]
        base_value = value * factor[from_unit]
        return base_value / factor[to_unit]

def main():
    st.title("📏 Universal Unit Converter with Ai Assistant")
    st.markdown("---")

    unit_categories = {
        "📏 Length": "length",
        "⚖️ Weight": "weight",
        "🌡️ Temperature": "temperature",
        "🏞️ Area": "area",
        "🧪 Volume": "volume",
        "⏰ Time": "time"
    }

    selected_category = st.selectbox(
        "Select Category",
        list(unit_categories.keys()),
        index=0
    )
    unit_type = unit_categories[selected_category]

    unit_options = {
        'length': ['meter', 'kilometer', 'centimeter', 'millimeter', 'mile', 'yard', 'foot', 'inch'],
        'weight': ['kilogram', 'gram', 'milligram', 'pound', 'ounce', 'tonne'],
        'temperature': ['celsius', 'fahrenheit', 'kelvin'],
        'area': ['square meter', 'square kilometer', 'square mile', 'square foot', 'acre', 'hectare'],
        'volume': ['liter', 'milliliter', 'cubic meter', 'gallon', 'quart', 'pint', 'cup'],
        'time': ['second', 'minute', 'hour', 'day', 'week', 'month', 'year']
    }

    col1, col2 = st.columns([1, 1])
    with col1:
        from_unit = st.selectbox("From", unit_options[unit_type])
    with col2:
        to_unit = st.selectbox("To", unit_options[unit_type])

    value = st.number_input(
        "Enter Value",
        min_value=0.0,
        value=1.0,
        step=0.1,
        format="%.2f"
    )

    if st.button("Convert Units"):
        try:
            result = convert_units(value, from_unit, to_unit, unit_type)
            st.success(f"""
                **Conversion Result:**\n
                {value:.2f} {from_unit} = **{result:.4f}** {to_unit}
            """)
        except Exception as e:
            st.error(f"Error in conversion: {str(e)}")

    
    user_query = st.text_input("Ask AI Assistant anything about unit conversions:")
    if st.button("Ask AI") and user_query:
        response = ai_assistant(user_query)
        st.info(response)

if __name__ == "__main__":
    main()
