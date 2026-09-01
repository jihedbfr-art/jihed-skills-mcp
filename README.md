# JihedAiLabs Skills MCP Server

<p align="center">
  <b>The official Model Context Protocol (MCP) server for JihedAiLabs.</b>
</p>

## Overview

This MCP server allows autonomous AI agents (like Claude Desktop, Cursor, or custom orchestration loops) to dynamically discover and inject production-grade engineering skills from the `ai-skills` repository.

Rather than relying on outdated pre-training knowledge, agents can use this server to fetch deterministic Agent-Ready rules (e.g., how to correctly govern Claude 3.7 budget tokens, or how to write deterministic Spring AI Tool Calls) directly from the JihedAiLabs GitHub repository in real-time.

## Installation

You can run this MCP server directly via `uvx`:

```json
{
  "mcpServers": {
    "jihed-skills": {
      "command": "uvx",
      "args": [
        "jihed-skills-mcp"
      ]
    }
  }
}
```

Or install it locally:

```bash
git clone https://github.com/jihedbfr-art/jihed-skills-mcp.git
cd jihed-skills-mcp
pip install .
```

## Available Tools

The server exposes the following tools to the LLM:

1. `list_skill_domains`: Returns a list of all top-level engineering domains (e.g., `16-ai-platforms`, `06-spring-ai`).
2. `search_skills(domain)`: Returns all available Agent-Ready skills within a specific domain.
3. `read_skill(domain, skill_name)`: Reads the full markdown/YAML configuration of a skill and injects it into the LLM's context.

## Strategic Position

This project implements the "Killer Feature" identified in the **JihedAiLabs Top 10 World Strategy** (Section 43), transforming a static Markdown library into an ecosystem-agnostic distribution system for AI capabilities.

---
*Architected for the autonomous enterprise. A JihedAiLabs project.*
