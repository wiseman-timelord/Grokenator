# Assuming a `GrokAPI` for interaction with Grok
from grok_api import GrokAPI

def generate_response(state, message, file):
    grok = GrokAPI()  # This would need to be implemented or mocked
    try:
        if file:
            file_content = file.read().decode('utf-8')  # Real implementation might not need size limit if handled by Grok
            response = grok.query(message, context=file_content)
        else:
            response = grok.query(message)
        
        state['chat_history'] = state.get('chat_history', []) + [(message, response)]
        return response
    except Exception as e:
        return f"Error in generating response: {str(e)}"
