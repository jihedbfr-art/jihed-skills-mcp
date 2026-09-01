import os
import httpx
import yaml
import asyncio
from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Optional

# Initialize FastMCP Server
mcp = FastMCP("JihedAiLabs-Skills-MCP")

GITHUB_API_BASE = "https://api.github.com/repos/jihedbfr-art/ai-skills/contents/skills"
RAW_BASE_URL = "https://raw.githubusercontent.com/jihedbfr-art/ai-skills/main/skills"

async def fetch_github_contents(path: str = "") -> List[Dict]:
    """Fetches directory contents from the GitHub API."""
    url = f"{GITHUB_API_BASE}/{path}".strip("/")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url, 
            headers={"Accept": "application/vnd.github.v3+json", "User-Agent": "Jihed-Skills-MCP"}
        )
        if response.status_code == 200:
            return response.json()
        return []

async def fetch_raw_skill(path: str) -> Optional[str]:
    """Fetches the raw SKILL.md file from GitHub."""
    url = f"{RAW_BASE_URL}/{path}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.text
        return None

@mcp.tool()
async def list_skill_domains() -> str:
    """
    Lists all available engineering and AI skill domains (platforms/models) from JihedAiLabs.
    Use this to discover what domains are available before searching for specific skills.
    """
    contents = await fetch_github_contents("")
    domains = [item['name'] for item in contents if item['type'] == 'dir']
    
    if not domains:
        return "No domains found or API rate limit exceeded."
    
    return "Available Skill Domains:\n- " + "\n- ".join(domains)

@mcp.tool()
async def search_skills(domain: str) -> str:
    """
    Lists all specific skills available within a given domain.
    Args:
        domain: The name of the domain (e.g., '16-ai-platforms' or '06-spring-ai').
    """
    contents = await fetch_github_contents(domain)
    skills = [item['name'] for item in contents if item['type'] == 'dir']
    
    if not skills:
        return f"No skills found in domain '{domain}'."
        
    return f"Skills in {domain}:\n- " + "\n- ".join(skills)

@mcp.tool()
async def read_skill(domain: str, skill_name: str) -> str:
    """
    Reads the full Agent-Ready SKILL.md for a specific skill. 
    This injects production-grade engineering rules, heuristics, and execution context directly into your cognitive loop.
    
    Args:
        domain: The domain folder (e.g., '16-ai-platforms').
        skill_name: The specific skill folder (e.g., 'openai-spring-sdk').
    """
    path = f"{domain}/{skill_name}/SKILL.md"
    content = await fetch_raw_skill(path)
    
    if not content:
        return f"Could not find or read SKILL.md for {domain}/{skill_name}."
        
    return content

def main():
    """Starts the MCP server on stdio."""
    print("Starting JihedAiLabs Skills MCP Server...", flush=True)
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
