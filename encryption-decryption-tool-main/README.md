# Encryption / Decryption Tool — Internship Project 3

A Python command-line utility demonstrating secure symmetric encryption and decryption of text and files using Fernet from the `cryptography` package.

## Features
- Desktop GUI for text and file encryption/decryption
- Secure Fernet key generation
- Text encryption/decryption
- File encryption/decryption
- Authenticated encryption: tampering or a wrong key causes decryption failure
- Basic automated tests
- Clear CLI commands suitable for an internship demonstration

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
Launch the graphical interface:
```bash
python src/gui.py
# Or use the CLI entry point:
python src/main.py gui
```

In the GUI, select or generate a key, then use the Text and Files tabs to encrypt or decrypt data. File operations ask where to save their output.

Use the command-line interface:
```bash
python3 src/main.py generate-key
python3 src/main.py encrypt-text "Confidential message"
python3 src/main.py decrypt-text "<PASTE_TOKEN_HERE>"
```

File example:
```bash
echo "Sensitive internship data" > output/sample.txt
python3 src/main.py encrypt-file output/sample.txt output/sample.enc
python3 src/main.py decrypt-file output/sample.enc output/sample-restored.txt
```

Run tests:
```bash
pytest -q
```

## Security notes
- Keep encryption keys private and never commit real secret keys to Git.
- The included output files are demonstration artifacts only.
- This project is intended for authorized educational/internship use.
- Fernet provides symmetric authenticated encryption; production key management should use a dedicated secrets-management system.

## Project Structure
```text
src/       application source code
  gui.py   Tkinter desktop interface
  main.py  command-line interface
  crypto_tool.py  Fernet cryptographic helpers
tests/     automated tests
output/    safe demonstration artifacts
docs/      project documentation and final report
screenshots/ demonstration evidence
```
