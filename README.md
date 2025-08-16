Understood — there's **no timing feature** implemented in your repository. Based on the project contents I can review (e.g., with files like `tools.py`, `guardrails.py`, `main.py`, etc., but no timing tool), here’s an updated `README.md` without any mention of library hours or timing features:

---

```markdown
# Agentic SDK Assignment 05

This project is a **Library Assistant** built using the **OpenAI Agents SDK**. It demonstrates how to integrate LLMs with structured tools and guardrails to enable safe, focused functionality around library-related queries.

---

##  Features

- **Agent** & **Runner** handle dialogue flow and tool orchestration  
- Tools implemented for:
  - Searching for books
  - Checking book availability
- **Guardrails** to restrict the assistant to library-relevant questions only  
- Configurable model setup using `AsyncOpenAI` (e.g., Gemini) and `RunConfig`

---

##  Project Structure

```

assignment\_05/
├── configuration.py     # Load & manage model/client configuration
├── guardrails.py        # Guardrail definitions to ensure safe assistant behavior
├── main.py              # Entry point — sets up the agent and runs interactions
├── tools.py             # Function tools (@function\_tool definitions for core features)
├── .gitignore           # Ignores sensitive and generated files (e.g., .env, venv)
├── README.md            # Project documentation
├── pyproject.toml       # Dependency and project metadata
└── uv.lock              # Lock file for reproducible environment setup

````

---

##  Setup & Installation

### Prerequisites:
- Python 3.11+
- A package manager like `pip`

### Steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/anusbutt/Agentic_SDK_Assignment_05.git
   cd Agentic_SDK_Assignment_05
````

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   *(If `requirements.txt` isn't present, you can install dependencies listed in `pyproject.toml` manually.)*

3. **Configure environment variables:**

   * Create a `.env` file in the root:

     ```env
     GEMINI_API_KEY=your_api_key_here
     ```
   * This ensures your API key is kept out of version control.

4. **Run the assistant:**

   ```bash
   python main.py
   ```

---

## Usage Examples

* **Search for a book:**

  ```
  Q: Can you search for "1984"?
  A: [Returns search results from the book database tool]
  ```

* **Check if a book is available:**

  ```
  Q: Is "To Kill a Mockingbird" available?
  A: [Returns availability status]
  ```

* **Prevent off-topic queries:**

  ```
  Q: How do I fix a leaking faucet?
  A: Sorry, I can only assist with library-related questions.
  ```

---

## Why This Project Matters

It showcases how to:

* Build AI assistants that link LLM responses with real-world logic
* Enforce context and relevance using **guardrails**
* Flexibly configure model backends using `RunConfig` and `AsyncOpenAI`

---

## Future Improvements

* Add more functional tools (e.g., borrowing books, returning books)
* Connect to a real library database or API
* Expand guardrail rules to enhance safety and scope control

---

## Acknowledgements

* Built using the \[OpenAI Agents SDK]
* Environment variables handled with `python-dotenv`

---
