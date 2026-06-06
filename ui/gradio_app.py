import gradio as gr
from datetime import datetime
import time


def chat_message(message, system_prompt, history):

    log = (
        f"[{datetime.now().strftime('%H:%M:%S')}]\n"
        f"Received query: {message}"
    )

    workflow = """
🟡 Intent Analysis
⚪ Memory Retrieval
⚪ Planner Agent
⚪ TMDB Search
⚪ IMDb Search
⚪ Reddit Search
⚪ Theatre Search
⚪ Validator
⚪ Recommendation Agent
"""

    yield (
        "",
        history,
        workflow,
        log,
        None,
        None,
        None,
        None
    )

    time.sleep(1)

    workflow = """
🟢 Intent Analysis
🟡 Memory Retrieval
⚪ Planner Agent
⚪ TMDB Search
⚪ IMDb Search
⚪ Reddit Search
⚪ Theatre Search
⚪ Validator
⚪ Recommendation Agent
"""

    log += "\nRetrieved user preferences"

    yield (
        "",
        history,
        workflow,
        log,
        None,
        None,
        None,
        None
    )

    time.sleep(1)

    workflow = """
🟢 Intent Analysis
🟢 Memory Retrieval
🟢 Planner Agent
🟢 TMDB Search
🟢 IMDb Search
🟢 Reddit Search
🟢 Theatre Search
🟢 Validator
🟢 Recommendation Agent
"""

    history = history + [
        {
            "role": "user",
            "content": message
        },
        {
            "role": "assistant",
            "content": f"Searching movies for: {message}"
        }
    ]

    yield (
        "",
        history,
        workflow,
        log,
        None,
        None,
        None,
        None
    )


with gr.Blocks(
    title="Movie Agent",
    css="styles.css"
) as demo:

    gr.Markdown("# 🎬 Movie Agent")

    with gr.Row():

        with gr.Column(scale=3):

            chatbot = gr.Chatbot(
                label="Movie Assistant",
                type="messages",
                height=700
            )

            chat_input = gr.Textbox(
                placeholder="Find me some good movies for this weekend...",
                show_label=False
            )

        with gr.Column(scale=2):

            system_prompt = gr.Textbox(
                label="System Prompt",
                value="You are an helpful movie assistant that provides recommendations based on user preferences. You can search TMDB, IMDb, Reddit, and local theatre listings to find the best movie options for the user.",
                lines=5
            )

            workflow_status = gr.Markdown(
                value="⚪ Waiting..."
            )

            activity_log = gr.Textbox(
                label="Agent Activity",
                lines=12,
                interactive=False
            )

    gr.Markdown("---")

    gr.Markdown("## 🌐 Browser Activity Monitor")

    with gr.Row():

        tmdb_tile = gr.Image(
            label="TMDB Search",
            interactive=False,
            height=250
        )

        imdb_tile = gr.Image(
            label="IMDb Search",
            interactive=False,
            height=250
        )

    with gr.Row():

        reddit_tile = gr.Image(
            label="Reddit Search",
            interactive=False,
            height=250
        )

        theatre_tile = gr.Image(
            label="Theatre Search",
            interactive=False,
            height=250
        )

    chat_input.submit(
        fn=chat_message,
        inputs=[
            chat_input,
            system_prompt,
            chatbot
        ],
        outputs=[
            chat_input,
            chatbot,
            workflow_status,
            activity_log,
            tmdb_tile,
            imdb_tile,
            reddit_tile,
            theatre_tile
        ]
    )