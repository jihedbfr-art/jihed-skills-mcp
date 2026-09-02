# jihed-skills-mcp

<p align="center">
  <b>Un serveur MCP qui permet à un agent de lire la bibliothèque <a href="https://github.com/jihedbfr-art/ai-skills">ai-skills</a> au moment de l'appel, au lieu de s'en remettre à son pré-entraînement.</b>
</p>

<p align="center">
  <a href="README.md">🇬🇧 Read in English</a>
</p>

---

## Ce qu'il fait

Trois outils exposés en stdio :

| Outil | Ce qu'il renvoie |
|---|---|
| `list_skill_domains()` | Les domaines de premier niveau de la bibliothèque. |
| `search_skills(domain)` | Le contenu d'un domaine. Certains domaines regroupent leurs skills un niveau plus bas — dans ce cas, rappeler l'outil sur `<domaine>/<entrée>`. |
| `read_skill(path)` | Le `SKILL.md` complet à ce chemin, tel quel, pour que ses règles entrent dans le contexte de l'agent. N'importe quelle profondeur de chemin fonctionne. |

Les skills sont récupérés depuis GitHub à chaque appel plutôt qu'embarqués dans le paquet : un
skill corrigé le matin est celui que l'agent obtient l'après-midi, sans release entre les deux.

## Installation

Pas publié sur PyPI. Installation depuis les sources :

```bash
git clone https://github.com/jihedbfr-art/jihed-skills-mcp.git
cd jihed-skills-mcp
pip install .
```

Puis déclarer le serveur auprès du client — pour une configuration façon Claude Desktop :

```json
{
  "mcpServers": {
    "jihed-skills": {
      "command": "jihed-skills-mcp"
    }
  }
}
```

## Exemple

```
list_skill_domains()
  → 01-llm-foundations-and-models, 02-prompt-and-context-engineering,
    03-rag-architectures, ... 15-frontier-models-and-trends

search_skills("05-mcp-protocol-and-tools")
  → mcp-server-stdio-tool-schema, mcp-sse-transport-and-resource-providers

read_skill("05-mcp-protocol-and-tools/mcp-server-stdio-tool-schema")
  → le SKILL.md complet
```

## Deux choses à savoir

- **L'API GitHub est utilisée sans authentification**, soit 60 requêtes par heure et par IP. Une
  liste de domaines vide est bien plus souvent une limite de débit qu'une bibliothèque vide, et
  l'outil le dit au lieu d'annoncer « rien trouvé ».
- **Ce serveur vise MCP 2.x**, où `FastMCP` est devenu `MCPServer`. Du code écrit pour l'API 1.x
  ne s'importe pas avec un SDK à jour.

## Licence

MIT — voir [LICENSE](LICENSE).
