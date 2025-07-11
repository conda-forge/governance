## Bot Sub-Team

### Role

Develop and manage the conda-forge migration bot and all related tooling.
Also manages and deploys migrations themselves.

### Charter

Dynamic

### Responsibility

The migration and autotick bot is now a central part of the conda-forge ecosystem.
This subteam has the right and responsibility to manage and develop the general
operation of the bot.
This includes building new migrators, fixing migration related bugs, and tooling.
Example migrations that can happen include:

- Compiler bumps
- Python version bump
- R version bump
- Build number bumps of the ecosystem when a pinned package version updates and
  there is a binary incompatibility which necessitates downstream rebuilds.
- Automatically version bumping of feedstocks when the package releases a new version.

For large scale (affecting >20% of packages) this sub-team will inform and
discuss with the core team about the upcoming migration prior to starting the
migration.

Packages and tools that fall under the purview of the bot subteam include:

- cf-scripts
- libcflib
- libcfgraph
- cf-graph
- circle-worker