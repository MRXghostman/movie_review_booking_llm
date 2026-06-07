import gradio as gr
from src.graph.graph import app

def chat_message(message, system_prompt, history):

    logs = []

    for update in app.stream(
        {
            "query": message,
            "messages": history,
            "system_prompt": system_prompt,
            "status": "",
            "plan": "",
            "search_result": "",
            "response": ""
        },
        stream_mode="updates"
    ):
        for node_name, node_update in update.items():
            if "status" in node_update:
                logs.append(node_update["status"])
                yield (
                    gr.update(),
                    history,
                    node_update["status"],
                    "\n".join(logs),
                    None,
                    None,
                    None,
                    None
                )        

    result = app.invoke(
        {
            "query": message,
            "messages": history,
            "system_prompt": system_prompt,
            "status": "",
            "plan": "",
            "search_result": "",
            "response": ""
        }
    )

    history = history or []

    history.append({
        "role": "user",
        "content": message
    })

    history.append({
        "role": "assistant",
        "content": result["response"]
    })


    yield ("", history, result["status"], "\n".join(logs), None, None, None, None)


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