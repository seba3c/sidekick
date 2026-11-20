"""Shared light/dark styling and browser-only theme controls for Sidekick.

Gradio 6 receives app-level theme, CSS, and head content through launch().
"""

import gradio as gr

THEME = gr.themes.Base(
    primary_hue="blue",
    secondary_hue="blue",
    neutral_hue="gray",
    font=["ui-sans-serif", "system-ui", "sans-serif"],
    font_mono=["ui-monospace", "SFMono-Regular", "Consolas", "monospace"],
).set(
    body_background_fill="#f7f8fa",
    body_background_fill_dark="#111315",
    body_text_color="#20242a",
    body_text_color_dark="#e8eaed",
    body_text_color_subdued="#596371",
    body_text_color_subdued_dark="#a1aab6",
    background_fill_primary="#ffffff",
    background_fill_primary_dark="#1a1d21",
    background_fill_secondary="#f0f2f5",
    background_fill_secondary_dark="#24282e",
    border_color_primary="#d9dee5",
    border_color_primary_dark="#3b424c",
    border_color_accent="#2563eb",
    border_color_accent_dark="#60a5fa",
    link_text_color="#1d4ed8",
    link_text_color_dark="#93c5fd",
    link_text_color_hover="#1e40af",
    link_text_color_hover_dark="#bfdbfe",
    block_background_fill="*background_fill_primary",
    block_background_fill_dark="*background_fill_primary",
    block_border_color="*border_color_primary",
    block_border_color_dark="*border_color_primary",
    block_border_width="1px",
    block_radius="12px",
    block_shadow="none",
    block_shadow_dark="none",
    block_label_background_fill="*background_fill_primary",
    block_label_background_fill_dark="*background_fill_primary",
    block_label_text_color="*body_text_color_subdued",
    block_label_text_color_dark="*body_text_color_subdued",
    block_title_text_color="*body_text_color",
    block_title_text_color_dark="*body_text_color",
    input_background_fill="*background_fill_primary",
    input_background_fill_dark="*background_fill_primary",
    input_border_color="#89929e",
    input_border_color_dark="#687382",
    input_border_color_focus="*border_color_accent",
    input_border_color_focus_dark="*border_color_accent",
    input_placeholder_color="*body_text_color_subdued",
    input_placeholder_color_dark="*body_text_color_subdued",
    input_radius="8px",
    input_shadow="none",
    input_shadow_dark="none",
    input_shadow_focus="none",
    input_shadow_focus_dark="none",
    button_large_radius="8px",
    button_small_radius="8px",
    button_border_width="1px",
    button_transition="none",
    button_primary_background_fill="#2563eb",
    button_primary_background_fill_dark="#60a5fa",
    button_primary_background_fill_hover="#1d4ed8",
    button_primary_background_fill_hover_dark="#93c5fd",
    button_primary_border_color="transparent",
    button_primary_border_color_dark="transparent",
    button_primary_border_color_hover="transparent",
    button_primary_border_color_hover_dark="transparent",
    button_primary_text_color="#ffffff",
    button_primary_text_color_dark="#111315",
    button_primary_text_color_hover="#ffffff",
    button_primary_text_color_hover_dark="#111315",
    button_primary_shadow="none",
    button_primary_shadow_dark="none",
    button_primary_shadow_hover="none",
    button_primary_shadow_hover_dark="none",
    button_primary_shadow_active="none",
    button_primary_shadow_active_dark="none",
    button_secondary_background_fill="*background_fill_primary",
    button_secondary_background_fill_dark="*background_fill_primary",
    button_secondary_background_fill_hover="*background_fill_secondary",
    button_secondary_background_fill_hover_dark="*background_fill_secondary",
    button_secondary_border_color="*border_color_primary",
    button_secondary_border_color_dark="*border_color_primary",
    button_secondary_text_color="*body_text_color",
    button_secondary_text_color_dark="*body_text_color",
    button_secondary_shadow="none",
    button_secondary_shadow_dark="none",
    button_secondary_shadow_hover="none",
    button_secondary_shadow_hover_dark="none",
    button_secondary_shadow_active="none",
    button_secondary_shadow_active_dark="none",
)

CSS = """
.gradio-container {
    --sidekick-success: #15803d;
    --sidekick-approval-bg: #fef3c7;
    --sidekick-approval-hover: #fde68a;
    --sidekick-approval-text: #854d0e;
    --sidekick-approval-border: #ca8a04;
    padding: 0 !important;
    background: var(--body-background-fill);
    color: var(--body-text-color);
}
.gradio-container > .main {
    max-width: 1200px !important;
    padding: clamp(20px, 2vw, 28px) clamp(16px, 3vw, 24px);
    margin: 0 auto;
}
.dark .gradio-container {
    --sidekick-success: #86efac;
    --sidekick-approval-bg: #362b17;
    --sidekick-approval-hover: #49391d;
    --sidekick-approval-text: #fde68a;
    --sidekick-approval-border: #a17d35;
}
.gradio-container ::selection {
    color: var(--button-primary-text-color);
    background: var(--button-primary-background-fill);
}
.gradio-container :is(textarea, input) { caret-color: var(--border-color-accent); }
.gradio-container * {
    scrollbar-color: var(--input-border-color) var(--background-fill-primary);
    scrollbar-width: thin;
}
.gradio-container :is(button, a):focus-visible {
    outline: 2px solid var(--border-color-accent);
    outline-offset: 3px;
}
.gradio-container a { text-underline-offset: 3px; }

#header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    padding: 0 0 12px;
}
#app-header .html-container, #plan-panel .html-container {
    padding: 0;
    transition: none;
}
#header h1 {
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--body-text-color);
    font-size: 28px;
    font-weight: 600;
    line-height: 1.2;
    margin: 0;
}
#header .title-icon {
    width: 28px;
    height: 28px;
    flex: none;
    color: var(--border-color-accent);
}
#header .context-label {
    color: var(--body-text-color-subdued);
    font-size: 14px;
    line-height: 1.5;
    margin: 6px 0 0;
}
#theme-toggle {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    width: 44px;
    min-height: 44px;
    padding: 10px;
    border: 1px solid var(--border-color-primary);
    border-radius: 8px;
    background: var(--background-fill-primary);
    color: var(--body-text-color);
    font: inherit;
    font-size: 14px;
    cursor: pointer;
    transition: none;
}
#theme-toggle:hover { background: var(--background-fill-secondary); }
#theme-toggle .theme-icon {
    display: none;
    width: 20px;
    height: 20px;
    flex: none;
}
#theme-toggle[aria-checked="true"] .sun-icon,
#theme-toggle[aria-checked="false"] .moon-icon {
    display: block;
}

#workspace { gap: 16px; }
#chat, #plan-panel, #ask-panel {
    background: var(--background-fill-primary);
    border: 1px solid var(--border-color-primary);
    border-radius: 12px;
    box-shadow: none;
}
#chat .message { font-size: 15px; }
#chat .message, #plan-panel li { overflow-wrap: anywhere; }
#plan-column { min-width: 240px; }
#plan-panel { padding: 20px; }
#plan-panel h3 {
    color: var(--body-text-color);
    font-size: 15px;
    font-weight: 600;
    margin: 0 0 14px;
}
#plan-panel .placeholder {
    color: var(--body-text-color-subdued);
    font-size: 14px;
    line-height: 1.6;
}
#plan-panel ul { list-style: none; padding: 0; margin: 0; }
#plan-panel li {
    color: var(--body-text-color);
    font-size: 14px;
    line-height: 1.6;
    margin: 12px 0;
    display: flex;
    align-items: flex-start;
    gap: 10px;
}
#plan-panel li:last-child { margin-bottom: 0; }
#plan-panel .mark {
    flex: none;
    width: 12px;
    height: 12px;
    border: 1px solid var(--input-border-color);
    border-radius: 50%;
    margin-top: 5px;
}
#plan-panel li.in_progress .mark {
    border: 3px solid var(--border-color-accent);
}
#plan-panel li.completed .mark {
    border-color: var(--sidekick-success);
    background: var(--sidekick-success);
}
#plan-panel li.completed { color: var(--body-text-color-subdued); }

#ask-panel { padding: 12px; }
#ask-panel textarea { font-size: 15px; }
#actions { gap: 12px; }
#actions button { min-height: 44px; font-weight: 600; }
#approve-button {
    background: var(--sidekick-approval-bg);
    color: var(--sidekick-approval-text);
    border-color: var(--sidekick-approval-border);
}
#approve-button:hover { background: var(--sidekick-approval-hover); }
#actions button:disabled { opacity: 0.5; cursor: not-allowed; }

@media (max-width: 700px) {
    #header { gap: 12px; }
    #header h1 { font-size: 24px; }
    #workspace { flex-direction: column; }
    #workspace > *, #plan-column {
        min-width: 0 !important;
        width: 100%;
        flex: none;
    }
    #chat { height: 320px; }
    #plan-panel { padding: 16px; }
    #actions { flex-wrap: wrap; }
}
"""

# Gradio injects head content before mounting the app's components. Applying the
# saved mode here avoids redirecting or restarting the session when themes change.
JS = """
<script>
(() => {
    if (window.sidekickTheme) return;
    const storageKey = 'sidekick.theme';
    const validTheme = value => value === 'dark' || value === 'light';
    const requested = new URL(window.location.href).searchParams.get('__theme');
    let saved;
    try { saved = localStorage.getItem(storageKey); } catch {}
    let mode = validTheme(requested) ? requested : validTheme(saved) ? saved : 'dark';
    let button;

    function syncAppearance() {
        const dark = mode === 'dark';
        document.body.classList.toggle('dark', dark);
        document.documentElement.style.colorScheme = mode;
        document.body.style.backgroundColor = dark ? 'var(--bg-dark)' : 'var(--bg)';
        document.body.style.color = dark ? 'var(--col-dark)' : 'var(--col)';
        if (button) button.setAttribute('aria-checked', String(dark));
    }

    function apply(next, remember = false) {
        mode = next;
        syncAppearance();
        const url = new URL(window.location.href);
        url.searchParams.set('__theme', mode);
        history.replaceState(history.state, '', url);
        if (remember) {
            try { localStorage.setItem(storageKey, mode); } catch {}
        }
    }

    window.sidekickTheme = {
        bind(control) {
            button = control;
            button.addEventListener('click', () => {
                apply(mode === 'dark' ? 'light' : 'dark', true);
            });
            syncAppearance();
        }
    };
    apply(mode);
    // Gradio may have subscribed to OS theme changes before loading this head.
    // Keep our explicit choice authoritative if that listener changes the class.
    new MutationObserver(() => {
        if (document.body.classList.contains('dark') !== (mode === 'dark')) {
            syncAppearance();
        }
    }).observe(document.body, { attributes: true, attributeFilter: ['class'] });
})();
</script>
"""

THEME_SWITCH_JS = """
window.sidekickTheme.bind(element.querySelector('#theme-toggle'));
"""
