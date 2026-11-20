"""Gradio app for the Sidekick. Run with: uv run app.py"""

import html

import gradio as gr
import styles

from sidekick import Sidekick

LAUNCH_STYLE = {"theme": styles.THEME, "css": styles.CSS, "head": styles.JS}

HEADER = """
<div id="header">
    <div>
        <h1>
            <svg class="title-icon" viewBox="0 0 24 24" fill="none"
                 stroke="currentColor" stroke-width="1.75" stroke-linecap="round"
                 stroke-linejoin="round" aria-hidden="true" focusable="false">
                <path d="M12 3v3M9 3h3" />
                <rect x="5" y="6" width="14" height="14" rx="4" />
                <path d="M2 11v4m20-4v4M9 16h6" />
                <circle cx="9" cy="11" r="1" />
                <circle cx="15" cy="11" r="1" />
            </svg>
            Sidekick
        </h1>
        <p class="context-label">Personal co-worker</p>
    </div>
    <button id="theme-toggle" type="button" role="switch"
            aria-label="Dark mode" aria-checked="true">
        <svg class="theme-icon sun-icon" viewBox="0 0 24 24" fill="none"
             stroke="currentColor" stroke-width="1.75" stroke-linecap="round"
             stroke-linejoin="round" aria-hidden="true" focusable="false">
            <circle cx="12" cy="12" r="4" />
            <path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19
                     M5 19l1.5-1.5m11-11L19 5" />
        </svg>
        <svg class="theme-icon moon-icon" viewBox="0 0 24 24" fill="none"
             stroke="currentColor" stroke-width="1.75" stroke-linecap="round"
             stroke-linejoin="round" aria-hidden="true" focusable="false">
            <path d="M20.9 13A9 9 0 0 1 11 3.1 9 9 0 1 0 20.9 13Z" />
        </svg>
    </button>
</div>
"""


def render_todos(todos):
    if not todos:
        items = '<div class="placeholder">The Sidekick will write its plan here as it works</div>'
    else:
        items = (
            "<ul>"
            + "".join(
                f'<li class="{todo["status"]}"><span class="mark"></span>{html.escape(todo["content"])}</li>'
                for todo in todos
            )
            + "</ul>"
        )
    return f"<h3>Plan</h3>{items}"


async def setup():
    sidekick = Sidekick()
    await sidekick.setup()
    return sidekick, gr.update(interactive=True)


async def process_message(sidekick, message, success_criteria, history):
    if (
        sidekick is None
    ):  # the user clicked before setup finished bringing up the MCP servers
        return history, gr.update(visible=False), sidekick
    results = await sidekick.run_turn(message, success_criteria, history)
    return results, gr.update(visible=sidekick.paused), sidekick


async def approve(sidekick, history):
    results = await sidekick.resume(history)
    return results, gr.update(visible=sidekick.paused), sidekick


def watch_todos(sidekick):
    """Called by the timer. The timer is the plan panel's only writer: if a long-running
    event owned the panel as an output, Gradio would lock it as pending and live updates
    would not render while the Sidekick works."""
    return render_todos(sidekick.todos) if sidekick else render_todos([])


async def reset(sidekick):
    if sidekick:
        sidekick.cleanup()
    new_sidekick = Sidekick()
    await new_sidekick.setup()
    return "", "", None, gr.update(visible=False), new_sidekick


def free_resources(sidekick):
    if sidekick:
        sidekick.cleanup()


def main():
    with gr.Blocks(title="Sidekick") as ui:
        gr.HTML(HEADER, elem_id="app-header", js_on_load=styles.THEME_SWITCH_JS)
        sidekick = gr.State(delete_callback=free_resources)

        with gr.Row(elem_id="workspace"):
            chatbot = gr.Chatbot(label="Sidekick", height=320, scale=3, elem_id="chat")
            with gr.Column(scale=1, elem_id="plan-column"):
                todos_panel = gr.HTML(render_todos([]), elem_id="plan-panel")
        with gr.Column(elem_id="ask-panel"):
            with gr.Row():
                message = gr.Textbox(
                    label="Your request",
                    placeholder="Your request to the Sidekick",
                )
            with gr.Row():
                success_criteria = gr.Textbox(
                    label="Success criteria",
                    placeholder="What are your success criteria?",
                )
        with gr.Row(elem_id="actions"):
            reset_button = gr.Button("Reset", elem_id="reset-button")
            approve_button = gr.Button(
                "Approve and continue", visible=False, elem_id="approve-button"
            )
            go_button = gr.Button(
                "Go!", variant="primary", elem_id="go-button", interactive=False
            )

        timer = gr.Timer(1)

        ui.load(setup, [], [sidekick, go_button])
        timer.tick(watch_todos, [sidekick], [todos_panel], show_progress="hidden")
        message.submit(
            process_message,
            [sidekick, message, success_criteria, chatbot],
            [chatbot, approve_button, sidekick],
        )
        success_criteria.submit(
            process_message,
            [sidekick, message, success_criteria, chatbot],
            [chatbot, approve_button, sidekick],
        )
        go_button.click(
            process_message,
            [sidekick, message, success_criteria, chatbot],
            [chatbot, approve_button, sidekick],
        )
        approve_button.click(
            approve, [sidekick, chatbot], [chatbot, approve_button, sidekick]
        )
        reset_button.click(
            reset,
            [sidekick],
            [message, success_criteria, chatbot, approve_button, sidekick],
        )

    ui.launch(inbrowser=True, **LAUNCH_STYLE)


if __name__ == "__main__":
    main()
