# AGENTS.md - Coding Assistant Guide

## Commands
- **Run main application**: `python slep.py` (long-running sleep loop)
- **Run scripts**: `python <script_name>.py` (no testing framework detected)
- **Docker**: `docker build .` and `docker run <image>`
- **Install dependencies**: `pip install -r requirements.txt`

## Architecture
- **Language**: Python 3.11
- **Database**: Neo4j graph database (neo4j://neo4j:7687)
- **External API**: SATO building management API (project-sato1/2.lasige.di.fc.ul.pt)
- **Main modules**: 
  - `discovery.py` - Neo4j graph population from SATO API
  - `sato_function.py` - SATO API interaction utilities
  - `Fetch_building_data.py` - Neo4j query functions
  - `base_line_approach/` - Alternative discovery implementations

## Code Style
- **Imports**: Standard library first, then third-party (neo4j, pandas, requests)
- **Variables**: snake_case naming convention
- **Functions**: snake_case with descriptive names
- **API**: Hardcoded credentials and endpoints (NEO4J_URI, api_endpoints, headers)
- **Error handling**: Basic exception raising with custom messages
- **Data formats**: Pandas DataFrames for Excel, JSON for API responses
