# Weather Forecast MCP Portfolio Project

This project is an advanced portfolio piece that demonstrates a professional-grade workflow for integrating LLMs with custom MCP servers and browser automation.

It showcases how to build a multi-agent system in Python that uses:
- **Anthropic MCP SDK** for exposing custom tools to a language model.
- **Playwright** for automated browser control and web interaction.
- **Groq** for LLM orchestration and tool selection.

---

## Project Overview

The solution includes three main components:
- `host.py` — the chat host that connects to multiple MCP clients, discovers available tools, and forwards user requests to the LLM.
- `client.py` — a generic MCP client wrapper that launches MCP server scripts and manages STDIO communication.
- `weather_USA.py` — a classic MCP server that fetches weather data from the NWS API for the USA.
- `weather_Israel.py` — a new MCP server that performs browser automation to retrieve Israeli weather forecast data from a website.

The architecture intentionally separates concerns: one MCP handles API-based weather data, while another MCP handles browser-driven Israeli weather retrieval.

---

## Why this project is portfolio-worthy

This project is designed to reflect both technical depth and learning progress:
- Building a custom MCP Server from scratch.
- Integrating browser automation with an LLM workflow.
- Enabling the model to choose and orchestrate tools dynamically.
- Solving a real-world problem with non-conventional data access.

It demonstrates the ability to design and implement advanced AI tooling, not just consume existing APIs.

---

## Learning Goals

This project highlights the key professional and educational outcomes:
- Build an independent MCP Server that exposes custom tools to an LLM.
- Use Playwright to extend the LLM with browser automation capabilities.
- Design a multi-step flow that answers real user queries through tool orchestration.
- Apply RAG-style contextual enrichment by extracting and using page content.

---

## Technical Stack

- `MCP SDK` — Anthropic's official toolkit for defining the MCP protocol and exposing tools to the model.
- `Playwright` — Microsoft's modern browser automation framework, used here to automate a real website and perform human-like interactions.

---

## Project Requirements

The main goal is to build a new MCP Server that handles Israeli weather forecast requests by opening a browser and navigating to a specific site, rather than using a conventional API.

Recruiter-worthy highlights:
- A custom MCP Server focused on browser-based data retrieval.
- Playwright-driven automation for searching and selecting a city in a live website.
- A multi-step tool chain that simulates manual browsing from within an AI agent.
- Page extraction and contextualization for the LLM.

---

## Development Stages

### Stage 0 — Project Structure

```
project-template/
├── client.py          # generic MCP Client
├── host.py            # terminal chat host that ties everything together
├── weather_USA.py     # MCP Server for USA using API
└── weather_Israel.py  # ← your core Israel-focused MCP
```

### Stage A — Implement Tools with Playwright

**Goal:** implement MCP tools that allow the LLM to fetch Israeli weather forecast directly from the browser.

The new MCP should load the forecast page from:
https://www.weather2day.co.il/forecast

The MCP exposes three Playwright-based tools that automate the complete flow:
1. `open_weather_forecast_israel` — open the browser and navigate to the weather page.
2. `enter_weather_forecast_city_israel` — enter the city name into the search field.
3. `select_weather_forecast_city_israel` — select the first city suggestion from the list.

To make this work professionally:
- define each function as an MCP tool using the decorator.
- add the new MCP to the host's MCP client list.
- run the system and verify the host selects the new MCP and executes the functions sequentially.

Example command:
```bash
uv run host.py
```

Then ask the system for a forecast in a given city and confirm that the host opened the forecast page in the browser.

---

### Stage B — Let the LLM Finish the Answer

**Goal:** move beyond tool execution and give the LLM page content so it can answer directly in chat.

Add another tool that extracts the page content, cleans it, and returns a useful context snippet for the LLM.
This is the RAG-style enhancement: the model receives actual page text and can incorporate it into the response.

---

## How it works

1. `host.py` connects to the MCP clients defined in `client.py`.
2. It asks Groq to decide which tool should run for a given user query.
3. The selected MCP tool runs and returns real data.
4. If the browser-based MCP is used, Playwright drives the website and extracts context from the page.
5. The result is returned to the user as a fully formed chat answer.

---

## Why this project matters for AI recruiting

This project shows that I can:
- architect multi-agent systems.
- implement custom MCP tools for business logic.
- use browser automation to access data behind interactive websites.
- enrich LLM responses with real-world context.
- solve engineering problems that involve both AI and automation.

---

## Run Instructions

1. Install dependencies:

```powershell
python -m pip install -U pip
python -m pip install groq>=0.4.0 mcp>=1.27.0 python-dotenv>=1.2.2 playwright>=1.44.0
python -m playwright install
```

2. Create a `.env` file with:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=mixtral-8x7b-32768
```

3. Run the host:

```powershell
python host.py
```

4. Ask a query about weather forecast in Israel or the USA.

---

## Sample Questions

- `What is the weather forecast for Jerusalem today?`
- `Open the Israeli weather site and get the forecast for Tel Aviv.`
- `Are there any weather alerts in California?`
- `Use the Israel browser tool and answer from the page content.`
- `How do I get a 5-day forecast for a US location?`

---

## Notes

- The Israeli MCP is intentionally browser-driven rather than API-driven.
- The project emphasizes autonomous tool orchestration and dynamic LLM-driven execution.
- This is a strong portfolio example for AI engineering, agent design, and browser automation skills.
