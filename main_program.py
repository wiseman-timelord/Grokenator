import gradio as gr
from scripts.interface import create_interface
from scripts.utility import load_session, save_session

# Global variables for session management
session_data = load_session()

if __name__ == "__main__":
    with gr.Blocks() as demo:
        create_interface()
    demo.queue(concurrency_count=10).launch(server_name="0.0.0.0", server_port=7860, debug=True, share=True)
