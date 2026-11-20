#!/usr/bin/env python3
"""Tkinter interface for the encryption and decryption helpers."""
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

if __package__:
    from .crypto_tool import (
        decrypt_file,
        decrypt_text,
        encrypt_file,
        encrypt_text,
        generate_key,
        load_key,
    )
else:
    from crypto_tool import (
        decrypt_file,
        decrypt_text,
        encrypt_file,
        encrypt_text,
        generate_key,
        load_key,
    )


class EncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Encryption / Decryption Tool")
        self.root.geometry("820x700")
        self.root.minsize(680, 560)

        self.key_path = tk.StringVar(value="output/secret.key")
        self.input_file = tk.StringVar()
        self.status = tk.StringVar(value="Choose a key file or generate a new one.")

        self._build_interface()

    def _build_interface(self):
        container = ttk.Frame(self.root, padding=18)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)

        ttk.Label(
            container,
            text="Encryption / Decryption Tool",
            font=("TkDefaultFont", 18, "bold"),
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(
            container,
            text="Protect text and files with authenticated Fernet encryption.",
        ).grid(row=1, column=0, sticky="w", pady=(4, 14))

        key_frame = ttk.LabelFrame(container, text="Encryption key", padding=10)
        key_frame.grid(row=2, column=0, sticky="new")
        key_frame.columnconfigure(1, weight=1)
        ttk.Label(key_frame, text="Key file").grid(row=0, column=0, sticky="w", padx=(0, 8))
        ttk.Entry(key_frame, textvariable=self.key_path).grid(
            row=0, column=1, sticky="ew"
        )
        ttk.Button(key_frame, text="Browse...", command=self._browse_key).grid(
            row=0, column=2, padx=(8, 0)
        )
        ttk.Button(
            key_frame, text="Generate key", command=self._generate_key
        ).grid(row=0, column=3, padx=(8, 0))
        ttk.Label(
            key_frame,
            text="Keep this key private. You need the same key to decrypt your data.",
        ).grid(row=1, column=0, columnspan=4, sticky="w", pady=(8, 0))

        self.notebook = ttk.Notebook(container)
        self.notebook.grid(row=3, column=0, sticky="nsew", pady=(14, 10))
        container.rowconfigure(3, weight=1)
        self._build_text_tabs()
        self._build_file_tab()

        ttk.Label(container, textvariable=self.status, relief="sunken", anchor="w").grid(
            row=4, column=0, sticky="ew"
        )

    def _build_text_tabs(self):
        self.encrypt_input, self.encrypt_output = self._create_text_tab(
            "Encrypt Text",
            "Plaintext input",
            "Encrypted token",
            "Enter the text you want to encrypt.",
            "Encrypt text",
            True,
        )
        self.decrypt_input, self.decrypt_output = self._create_text_tab(
            "Decrypt Text",
            "Encrypted token input",
            "Decrypted text",
            "Paste the complete token and use the same key that encrypted it.",
            "Decrypt text",
            False,
        )

    def _create_text_tab(
        self, title, input_label, output_label, hint, button_label, encrypt
    ):
        tab = ttk.Frame(self.notebook, padding=12)
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(2, weight=1)
        tab.rowconfigure(4, weight=1)
        self.notebook.add(tab, text=title)

        ttk.Label(tab, text=hint, wraplength=680).grid(
            row=0, column=0, sticky="w", pady=(0, 10)
        )
        ttk.Label(tab, text=input_label).grid(
            row=1, column=0, sticky="w", pady=(0, 5)
        )
        input_widget = tk.Text(tab, height=8, wrap="word")
        input_widget.grid(row=2, column=0, sticky="nsew")

        ttk.Label(tab, text=output_label).grid(
            row=3, column=0, sticky="w", pady=(12, 5)
        )
        output_widget = tk.Text(tab, height=8, wrap="word", state="disabled")
        output_widget.grid(row=4, column=0, sticky="nsew")

        buttons = ttk.Frame(tab)
        buttons.grid(row=5, column=0, sticky="e", pady=(10, 0))
        ttk.Button(
            buttons,
            text=button_label,
            command=lambda: self._process_text(
                encrypt, input_widget, output_widget
            ),
        ).pack(side="left")
        return input_widget, output_widget

    def _build_file_tab(self):
        tab = ttk.Frame(self.notebook, padding=12)
        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(2, weight=1)
        self.notebook.add(tab, text="Files")

        ttk.Label(tab, text="Input file").grid(row=0, column=0, sticky="w", padx=(0, 8))
        ttk.Entry(tab, textvariable=self.input_file).grid(
            row=0, column=1, sticky="ew"
        )
        ttk.Button(tab, text="Browse...", command=self._browse_input_file).grid(
            row=0, column=2, padx=(8, 0)
        )

        ttk.Label(
            tab,
            text=(
                "Choose a file, then encrypt or decrypt it. "
                "You will be asked where to save the result."
            ),
            wraplength=650,
        ).grid(row=1, column=0, columnspan=3, sticky="w", pady=(12, 0))

        buttons = ttk.Frame(tab)
        buttons.grid(row=2, column=0, columnspan=3, sticky="nsew")
        ttk.Button(
            buttons,
            text="Encrypt file...",
            command=lambda: self._process_file(True),
        ).pack(side="left", padx=(0, 8), pady=12)
        ttk.Button(
            buttons,
            text="Decrypt file...",
            command=lambda: self._process_file(False),
        ).pack(side="left", pady=12)

    def _browse_key(self):
        selected = filedialog.askopenfilename(
            parent=self.root,
            title="Select Fernet key",
            filetypes=(("Key files", "*.key"), ("All files", "*")),
        )
        if selected:
            self.key_path.set(selected)
            self.status.set("Key file selected.")

    def _generate_key(self):
        key_path = self.key_path.get().strip()
        if not key_path:
            messagebox.showerror("Missing key path", "Enter a key file path first.", parent=self.root)
            return

        if Path(key_path).exists() and not messagebox.askyesno(
            "Replace key?",
            "This file already exists. Replacing it may make data encrypted "
            "with the old key unrecoverable. Continue?",
            parent=self.root,
        ):
            return

        try:
            generated_path = generate_key(key_path)
        except OSError as exc:
            messagebox.showerror("Key generation failed", str(exc), parent=self.root)
            return

        self.key_path.set(str(generated_path))
        self.status.set(f"New key generated: {generated_path}")

    def _browse_input_file(self):
        selected = filedialog.askopenfilename(parent=self.root, title="Select a file")
        if selected:
            self.input_file.set(selected)
            self.status.set("Input file selected.")

    def _process_text(self, encrypt, input_widget, output_widget):
        content = input_widget.get("1.0", "end-1c")
        if not encrypt:
            content = content.strip()

        try:
            key = load_key(self.key_path.get().strip())
            result = encrypt_text(content, key) if encrypt else decrypt_text(content, key)
        except (OSError, ValueError) as exc:
            error = str(exc)
            if not encrypt and error.startswith("Decryption failed:"):
                error = (
                    "Check that you pasted the complete encrypted token and selected "
                    "the same key used to encrypt it.\n\n" + error
                )
            messagebox.showerror("Text operation failed", error, parent=self.root)
            return

        output_widget.configure(state="normal")
        output_widget.delete("1.0", "end")
        output_widget.insert("1.0", result)
        output_widget.configure(state="disabled")
        self.status.set("Text encrypted." if encrypt else "Text decrypted.")

    def _process_file(self, encrypt):
        source_text = self.input_file.get().strip()
        if not source_text:
            messagebox.showerror(
                "Missing input file", "Select an input file first.", parent=self.root
            )
            return

        source = Path(source_text)
        if not source.is_file():
            messagebox.showerror(
                "Input file not found",
                f"The selected file does not exist:\n{source}",
                parent=self.root,
            )
            return

        if encrypt:
            output_name = source.name + ".enc"
            title = "Save encrypted file"
        else:
            output_name = (
                source.stem + ".restored"
                if source.suffix.lower() == ".enc"
                else source.name + ".restored"
            )
            title = "Save decrypted file"

        destination_text = filedialog.asksaveasfilename(
            parent=self.root,
            title=title,
            initialdir=str(source.parent),
            initialfile=output_name,
            confirmoverwrite=True,
        )
        if not destination_text:
            return

        destination = Path(destination_text)
        if source.resolve() == destination.resolve():
            messagebox.showerror(
                "Invalid output file",
                "The output file must be different from the input file.",
                parent=self.root,
            )
            return

        try:
            key = load_key(self.key_path.get().strip())
            result_path = (
                encrypt_file(source, destination, key)
                if encrypt
                else decrypt_file(source, destination, key)
            )
        except (OSError, ValueError) as exc:
            messagebox.showerror("File operation failed", str(exc), parent=self.root)
            return

        self.status.set(f"{'Encrypted' if encrypt else 'Decrypted'} file: {result_path}")
        messagebox.showinfo(
            "Operation complete",
            f"File saved to:\n{result_path}",
            parent=self.root,
        )


def launch_gui():
    root = tk.Tk()
    EncryptionApp(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
