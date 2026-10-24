# Blockchain-Enabled Chat Application

A web-based chat application built with **Python and Django** that combines user registration and login, administrator approval, user discovery, and one-to-one messaging with a proof-of-work blockchain-style ledger. Messages are encrypted before being stored in the message ledger.

> **Project status:** Academic/demo project. Review the security notes below before deploying it publicly or using real user data.

## Features

- **User registration** with name, email, username, mobile number, password validation, and optional profile picture.
- **Login and session-based access** for registered users.
- **Administrator approval**: newly registered accounts wait for approval before they can chat.
- **User search** to find active users and start a one-to-one conversation.
- **Encrypted messages** using AES encryption from PyCryptodome.
- **Blockchain-style message ledger** with block indexes, timestamps, previous-block hashes, SHA-256 hashing, and a simple proof-of-work process.
- **Admin dashboard** to view users and activate, deactivate, or delete accounts.
- **SQLite database** for local development and persistence of application records.
- **Django templates and CSS** for the web interface.

## Technology Stack

| Area | Technology |
|---|---|
| Language | Python |
| Web framework | Django |
| Database | SQLite |
| Encryption | PyCryptodome (AES) |
| Hashing | SHA-256 (`hashlib`) |
| Front end | HTML, CSS, Django Templates |
| Image handling | Pillow |
| Version control | Git and GitHub |

## Project Structure

```text
bcchat/
├── Admin/                                  # Admin views and configuration
├── Blockchain_Enabled_Chat_Application_System/
│   ├── settings.py                         # Django settings
│   ├── urls.py                             # URL routes
│   ├── views.py                            # Main page views
│   ├── asgi.py
│   └── wsgi.py
├── Users/
│   ├── migrations/                         # Database migrations
│   ├── blockchain.py                       # Block, hashing, mining, encryption
│   ├── models.py                           # User and block models
│   └── views.py                            # Registration, login, search, chat
├── Templates/                              # HTML templates and CSS
├── media/                                  # Uploaded profile pictures (runtime data)
├── manage.py
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.10 or a compatible Python version
- `pip`
- Git (optional, for cloning the repository)

## Setup and Run

### 1. Get the source code

Clone your repository and enter the project directory:

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

Replace the URL and directory name with your actual GitHub repository details. If you already have the project locally, open a terminal in the folder containing `manage.py`.

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt instead:

```bat
.venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Prepare the database

```bash
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

Stop the server with `Ctrl+C`.

## How to Use

1. Open the application in your browser.
2. Register a user account.
3. Sign in using the registered account after administrator approval.
4. Search for another active user.
5. Open a conversation and send a message.
6. Use the admin interface in the project to review accounts and approve or deactivate users.

The project's custom admin login flow is implemented separately from Django's built-in admin site. Check the relevant code and configuration for the current demo login behavior before using the application.

## How the Blockchain-Style Ledger Works

1. A message is encrypted before it is placed in a block.
2. Each block stores metadata such as sender, recipient, timestamp, previous block hash, nonce, and its own hash.
3. The block hash is calculated from the block data using SHA-256.
4. A simple proof-of-work loop increments the nonce until the hash meets the configured difficulty.
5. The application stores message-block records in the database and uses them to load conversations.

**Important:** This is an educational, application-level blockchain implementation. It is not a distributed blockchain network: it does not provide peer-to-peer consensus, independent network nodes, or decentralized replication.

## Security Notes

This codebase is intended for learning and demonstration, not production use. Before publishing or deploying it:

- **Replace hard-coded secrets and encryption keys.** Store secrets in environment variables and never commit them to GitHub.
- **Configure Django securely:** set `DEBUG = False` in production, use a strong private `SECRET_KEY`, and configure `ALLOWED_HOSTS` appropriately.
- **Fix authentication before using real accounts.** The current implementation appears to compare submitted passwords directly with database values instead of using Django's password-hashing APIs. Use Django's authentication system and hashed passwords.
- **Replace the hard-coded demo admin credentials** with secure, properly managed authentication.
- **Review the encryption design.** The current AES-CBC implementation should not be treated as production-grade end-to-end encryption. Use authenticated encryption and a proper key-management design.
- Do not commit real user data, local database files, uploaded profile images, logs, virtual environments, or private credentials.
- Use HTTPS and review CSRF, session-cookie, authorization, and file-upload settings before deployment.

## Limitations

- The blockchain ledger is maintained by the application rather than a distributed network.
- The current encryption key is configured in source code and must be replaced with secure key management.
- The app is designed as a demonstration and needs security hardening and testing before production use.

## Future Improvements

- Adopt Django's built-in authentication and password hashing.
- Move secrets to environment variables and add a safe example configuration file.
- Add automated tests for registration, access control, messaging, and ledger integrity.
- Use authenticated encryption with a robust key-management approach.
- Add pagination, delivery/read status, and improved conversation handling.
- Consider a real blockchain framework only if decentralized verification is a project requirement.

## License

No license is specified yet. Add a license file if you want others to reuse or distribute this project under defined terms.
