"""MCP server exposing the ai-skills library to autonomous agents.

Skills are read from GitHub at call time rather than vendored here, so an agent always gets
the current version of a skill instead of whatever was bundled when this server was released.
"""

import sys
from typing import Dict, List, Optional

import httpx
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("JihedAiLabs-Skills-MCP")

GITHUB_API_BASE = "https://api.github.com/repos/jihedbfr-art/ai-skills/contents/skills"
RAW_BASE_URL = "https://raw.githubusercontent.com/jihedbfr-art/ai-skills/main/skills"
TIMEOUT = httpx.Timeout(10.0)


async def fetch_directory(path: str = "") -> List[Dict]:
    """Lists one directory of the skills tree. Returns an empty list on any failure."""
    url = f"{GITHUB_API_BASE}/{path}".strip("/")
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            response = await client.get(
                url,
                headers={
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": "jihed-skills-mcp",
                },
            )
        except httpx.HTTPError:
            return []
        if response.status_code != 200:
            return []
        payload = response.json()
        # A file path returns an object rather than a list; callers only ever want directories.
        return payload if isinstance(payload, list) else []


async def fetch_raw(path: str) -> Optional[str]:
    """Downloads one file verbatim from the repository."""
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            response = await client.get(f"{RAW_BASE_URL}/{path}")
        except httpx.HTTPError:
            return None
        return response.text if response.status_code == 200 else None


@mcp.tool()
async def list_skill_domains() -> str:
    """
    Lists the top-level skill domains available in the ai-skills library.

    Call this first to discover what exists before looking for a specific skill.
    """
    contents = await fetch_directory("")
    domains = [item["name"] for item in contents if item["type"] == "dir"]

    if not domains:
        return (
            "No domains returned. The GitHub API is unauthenticated here and allows 60 requests "
            "per hour per IP, so this is most often a rate limit rather than an empty library."
        )

    return "Available skill domains:\n- " + "\n- ".join(domains)


@mcp.tool()
async def search_skills(domain: str) -> str:
    """
    Lists what a domain contains.

    Args:
        domain: A domain name from list_skill_domains, for example '05-mcp-protocol-and-tools'.

    Entries are usually skills, but a domain may group them one level deeper. When an entry turns
    out to hold no SKILL.md, call this tool again with '<domain>/<entry>'.
    """
    contents = await fetch_directory(domain)
    entries = [item["name"] for item in contents if item["type"] == "dir"]

    if not entries:
        return f"No entries found under '{domain}'."

    return f"Under {domain}:\n- " + "\n- ".join(entries)


@mcp.tool()
async def read_skill(path: str) -> str:
    """
    Reads a full SKILL.md and returns it verbatim, so its rules enter the current context.

    Args:
        path: The skill path relative to the skills directory, without the file name, for
            example '05-mcp-protocol-and-tools/mcp-server-stdio-tool-schema'. Any depth works.
    """
    clean = path.strip("/")
    if not clean:
        return "A skill path is required, for example '06-spring-ai-integration/<skill-name>'."

    content = await fetch_raw(f"{clean}/SKILL.md")
    if content is None:
        return (
            f"No SKILL.md at '{clean}'. Use search_skills to confirm the path — some domains "
            "nest their skills one level deeper than others."
        )
    return content


def main() -> None:
    """Runs the server over stdio."""
    # stdout carries the JSON-RPC stream on this transport; anything else printed there
    # corrupts the protocol, so status messages go to stderr.
    print("jihed-skills-mcp: serving ai-skills over stdio", file=sys.stderr, flush=True)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
