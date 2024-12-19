import gradio as gr
import os
from scripts.generate import generate_response
from scripts.utility import load_session, save_session, delete_session

def create_interface():
    state = gr.State()
    state.value = load_session()

    with gr.Column():
        chat = gr.ChatInterface(
            fn=generate_response,
            additional_inputs=["file"],
            state=state
        )
        
        # Session Management
        with gr.Row():
            save_btn = gr.Button("Save Session")
            load_btn = gr.Button("Load Session")
            new_btn = gr.Button("New Session")
            delete_btn = gr.Button("Delete Session")

        session_status = gr.Textbox(label="Session Status", interactive=False)
        session_list = gr.Dropdown(choices=update_session_list(), label="Choose Session")
        save_btn.click(save_session, inputs=[state], outputs=[session_status, session_list])
        load_btn.click(load_session, inputs=[session_list], outputs=[state, session_status])
        new_btn.click(lambda: {'chat_history': []}, outputs=[state, session_status])
        delete_btn.click(delete_session, inputs=[session_list], outputs=[session_status, session_list])
        
        # File handling feedback
        file_feedback = gr.Textbox(label="File Feedback", interactive=False)
        
        # Chat history display
        chat_history = gr.TextArea(label="Chat History", value="", interactive=False, lines=10)

    return chat, file_feedback, chat_history

def generate_response(state, message, file, file_feedback, chat_history):
    try:
        if file:
            file_content = file.read().decode('utf-8')[:10000]  # Limit file content size
            file_feedback.update(value=f"File '{file.name}' processed.")
            # Here would be the actual Grok interaction with file content
            response = f"Here's Grok's response to '{message}' considering the file '{file.name}':\n{file_content[:50]}..."
        else:
            file_feedback.update(value="No file uploaded.")
            response = f"Grok's response to '{message}'"
        
        state['chat_history'] = state.get('chat_history', []) + [(message, response)]
        new_chat_history = "\n".join([f"User: {m[0]}\nGrok: {m[1]}" for m in state['chat_history']])
        return response, file_feedback, chat_history.update(value=new_chat_history)
    except Exception as e:
        return f"An error occurred: {str(e)}", file_feedback.update(value=f"Error with file: {str(e)}"), chat_history

def update_session_list():
    return [f for f in os.listdir('data/sessions') if f.endswith('.json')]
