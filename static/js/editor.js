import { EditorView, basicSetup } from "codemirror";
import { EditorState } from "@codemirror/state";
import { python } from "@codemirror/lang-python";
import { oneDark } from "@codemirror/theme-one-dark";
import { autocompletion } from "@codemirror/autocomplete";
import { keymap } from "@codemirror/view";
import { indentWithTab } from "@codemirror/commands";

document.querySelectorAll(".code-editor").forEach((textarea) => {

    const editor = new EditorView({
        state: EditorState.create({
            doc: textarea.value,

            extensions: [
                basicSetup,
                python(),
                oneDark,
                keymap.of([indentWithTab]),
                autocompletion({
                    activateOnTyping: false
            
            })
            ]
        }),

        parent: textarea.parentElement
    });

    textarea.style.display = "none";

    textarea.form.addEventListener("submit", () => {
        textarea.value = editor.state.doc.toString();
    });
    
});