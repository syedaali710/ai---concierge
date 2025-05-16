# tools.py

# This is a simple tool for doing math
def calculator_tool(input_text: str) -> str:
    try:
        # Eval is dangerous in real apps; here we use it for simplicity
        result = eval(input_text)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"
