# jihed-skills-mcp

<p align="center">
  <b>An MCP server that lets an agent read the <a href="https://github.com/jihedbfr-art/ai-skills">ai-skills</a> library at call time, instead of relying on what it was trained on.</b>
</p>

<p align="center">
  <a href="README.fr.md">🇫🇷 Lire en Français</a>
</p>

---

## What it does

Three tools over stdio:

| Tool | What it returns |
|---|---|
| `list_skill_domains()` | The top-level domains of the skill library. |
| `search_skills(domain)` | What a domain contains. Some domains group skills one level deeper — call it again on `<domain>/<entry>` when that happens. |
| `read_skill(path)` | The full `SKILL.md` at that path, verbatim, so its rules enter the agent's context. Any path depth works. |

Skills are fetched from GitHub on each call rather than vendored into this package: a skill edited
this morning is the one the agent gets this afternoon, with no release in between.

## Install

Not published to PyPI. Install from source:

```bash
git clone https://github.com/jihedbfr-art/jihed-skills-mcp.git
cd jihed-skills-mcp
pip install .
```

Then register it with your client — for a Claude Desktop-style config:

```json
{
  "mcpServers": {
    "jihed-skills": {
      "command": "jihed-skills-mcp"
    }
  }
}
```

## Example

```
list_skill_domains()
  → 01-llm-foundations-and-models, 02-prompt-and-context-engineering,
    03-rag-architectures, ... 15-frontier-models-and-trends

search_skills("05-mcp-protocol-and-tools")
  → mcp-server-stdio-tool-schema, mcp-sse-transport-and-resource-providers

read_skill("05-mcp-protocol-and-tools/mcp-server-stdio-tool-schema")
  → the full SKILL.md
```

## Two things worth knowing

- **The GitHub API here is unauthenticated**, which means 60 requests per hour per IP. An empty
  domain list is far more often a rate limit than an empty library, and the tool says so rather
  than reporting nothing found.
- **This targets MCP 2.x**, where `FastMCP` became `MCPServer`. Code written against the 1.x API
  will not import against a current SDK.

## License

MIT — see [LICENSE](LICENSE).

## Validation

Six offline tests cover directory/file responses, HTTP rejection, network errors, raw text and invalid or undecodable JSON responses. A malformed directory response returns an empty list, like other fetch failures. HTTP calls are mocked; these tests validate neither a stdio MCP exchange nor a live GitHub connection.

CI builds and installs the wheel, then runs these tests on Ubuntu/Windows with Python 3.10 and 3.12.

```bash
python -m pip install build twine
python -m build
python -m twine check --strict dist/*
python -m unittest discover -s tests
```

---

<div align="center">
  <img src="https://raw.githubusercontent.com/jihedbfr-art/jihedbfr-art/main/assets/brand/jihedailabs-logo.svg" alt="JihedAiLabs" width="120"/>
  <br/>
  <sub>A <a href="https://github.com/jihedbfr-art"><b>JihedAiLabs</b></a> project</sub>
</div>
