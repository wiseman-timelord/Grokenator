import json
import os
import logging

# Setup logging
logging.basicConfig(filename='app.log', level=logging.ERROR)

def save_session(state):
    try:
        if not os.path.exists('data/sessions'):
            os.makedirs('data/sessions')
        session_name = "session_" + str(len(os.listdir('data/sessions')) + 1) + ".json"
        with open(os.path.join('data/sessions', session_name), 'w') as f:
            json.dump(state.value, f)
        return f"Session saved as {session_name}", update_session_list()
    except IOError as e:
        logging.error(f"Error saving session: {str(e)}")
        return f"Error saving session: {str(e)}", []

def load_session(session_name=None):
    try:
        if session_name:
            session_file = os.path.join('data/sessions', session_name)
            if os.path.exists(session_file):
                with open(session_file, 'r') as f:
                    return json.load(f)
        elif os.path.exists('data/sessions/session_1.json'):
            with open('data/sessions/session_1.json', 'r') as f:
                return json.load(f)
        return {'chat_history': []}
    except (IOError, json.JSONDecodeError) as e:
        logging.error(f"Error loading session: {str(e)}")
        return {'chat_history': [], 'error': f"Error loading session: {str(e)}"}

def delete_session(session_name):
    if session_name:
        session_file = os.path.join('data/sessions', session_name)
        if os.path.exists(session_file):
            os.remove(session_file)
            return f"Session {session_name} deleted.", update_session_list()
    return "No session selected or session not found.", update_session_list()

def update_session_list():
    return [f for f in os.listdir('data/sessions') if f.endswith('.json')]
