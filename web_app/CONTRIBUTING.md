# Developer Setup

These instructions are intended to help you get your development environment setup in order to start working on the web application.

### Clone the Project Repository

1. Clone the git repository: `git clone https://github.com/wchawkins/heart_rate_tracker.git`. This will create a local copy of the repo on your machine.
2. Change directories to the project folder: `cd heart_rate_tracker/web_app`

### Install asdf tool manager

asdf is a convenient way to manage versions of the different runtimes required to run the Phoenix web application, namely Elixir, Erlang and Node JS.

1. [Install asdf](https://asdf-vm.com/#/core-manage-asdf-vm)
2. Run `bash ~/.asdf/plugins/nodejs/bin/import-release-team-keyring` to import keys necessary to build and install nodejs.
2. Run `asdf plugin-add <plugin>`, where <plugin> should be `erlang`, `elixir`, and `nodejs`. This will install all of the required asdf plugins.
3. Run `asdf install`. This will install all the runtimes defined in the `.tool-versions` file. This might take a few minutes.

## Install Database

The web app uses PostgresSQL as the database.

1. There are several ways to install Postgres. Docker is a good choice if you're familiar with it: [Postgres image](https://hub.docker.com/_/postgres). For Mac OS, there's [this tool](https://postgresapp.com/).

## Install Phoenix and dependencies

1. Install dependencies with `mix deps.get`
2. Create and migrate your database with `mix ecto.setup`
3. Install Node.js dependencies with `cd assets && npm install`
4. Start Phoenix server with `mix phx.server`
