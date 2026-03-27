**Introduction:**
  -  This script is a simple code of an AI Agent that interacts with Rest API.
  -  As IBM Maximo developer, I attempted this project to practice my AI learnings in a semblance of Maximo API 

**Setup:**
  -  Install python version 3.12 or above
  -  Install 'uv' python library if not already installed
  -  Clone the project with this command'_git clone https://github.com/sankargh/maxrest_ai.git_'

**Run:**
  -  First, run the below command - To start the Rest API application.
      -  uv run maxrest.py
  -  Then, open another Terminal, to run the agent script
      -  uv run agent.py
  -  A chat interface is now accessible typically at --> http://127.0.0.1:7860

**Test:**
  -  Open the above chat window and Type your request for adding or querying the 'Asset, Location or Person' data
      -  Example 1: Please add location data ..(_LOC1001, 'Desc', Site' etc._).
      -  Example 2: Get the Asset details at Site01

**Limitations:**
  -  As of now (_27-Mar-2026)_, Only Asset, Location, Person objects are available with limited fields.
  -  For adding new data, we may have to confirm again, after entering details.

**Ideas:**
  -  Here are few ideas to improvise.
      -  Add 'InputGuardRails' to validate data restrictions of user profile
      -  Wrap the Querying & other data functions as MCP_Tool
      -  Add Document retrieval options.
