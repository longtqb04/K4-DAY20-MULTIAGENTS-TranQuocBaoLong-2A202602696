---
name: check-module-imports
description: Use this skill to verify that all necessary modules are correctly imported and available before running tests or executing code.
---
- Ensure that all required modules are installed and accessible in your environment.
- Check that the import paths are correct relative to your project's structure.
- Include a check to see if the module exists before trying to import it.
- Run tests that involve imports first in an isolated environment to catch import errors early.
- Use virtual environments to manage dependencies effectively.
- Avoid hardcoding paths; instead, use relative paths or configuration options.