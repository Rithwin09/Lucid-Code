# MetaMind 🧠

**An AI-powered application to instantly generate documentation and enable conversational search for your database schemas.**

---

## ✨ Features

MetaMind is a powerful tool for data professionals and developers, designed to accelerate the understanding of complex database structures.

-   **Dual Input Methods:** Supports both direct upload of **SQLite** (`.db`) files and pasting raw **SQL `CREATE TABLE` statements** for other databases like MySQL and PostgreSQL.
-   **AI-Powered Documentation:** Automatically generates comprehensive documentation for each table, including:
    -   A clear, one-sentence purpose.
    -   Detailed descriptions for each column.
    -   Relevant business tags for quick context.
    -   Actionable data quality check suggestions.
-   **Conversational Schema Search:** An interactive chat interface that allows you to ask follow-up questions about your schema in plain English.
-   **Secure API Key Handling:** A user-friendly sidebar allows users to enter their own API key, which is used only for their session and is never stored.

---

## 🛠️ Tech Stack

-   **Language:** Python
-   **Framework:** Streamlit
-   **AI Model:** Llama 3 via Groq API
-   **Libraries:** SQLAlchemy (for schema parsing), python-dotenv (for local development)

---

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

-   Python 3.9+
-   A free API key from [GroqCloud](https://console.groq.com/keys)

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/metamind_project.git](https://github.com/YOUR_USERNAME/metamind_project.git)
    cd metamind_project
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your API key (for local development):**
    -   Create a file named `.env` in the root of the project folder.
    -   Add your Groq API key to the file like this:
        ```
        GROQ_API_KEY="gsk_YourSecretKeyHere"
        ```

5.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
    The application will open in your web browser. For local development, it will use the key from your `.env` file. Otherwise, you can enter a key in the sidebar.

---

## 🌐 Deployment

This application is designed to be deployed on **Streamlit Community Cloud**. It will prompt users to enter their own API key in the sidebar, making it easily shareable.
