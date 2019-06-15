# Developer Setup

These instructions are intended to help you get your development environment setup in order to start working on the SpO2 Web application.

## Clone the Project Repository

1. Clone the git repository: `git clone git@gitlab.com:spo2/spo2-web.git`. This will create a local copy of the repo on your machine.
2. Change directories to the project folder: `cd spo2-web`

## Install asdf tool manager

asdf is a convenient way to manage versions of the different runtimes required to run the Phoenix web application, namely Elixir, Erlang and Node JS.

1. [Install asdf](https://asdf-vm.com/#/core-manage-asdf-vm)
2. Add each of the asdf plugins list in the repo's `.tool-versions` file: `asdf plugin-add <plugin>`, where *plugin* should be `erlang`, `elixir`, then `nodejs`.
3. Run `bash ~/.asdf/plugins/nodejs/bin/import-release-team-keyring` to import keys necessary to build and install nodejs.
4. Run `asdf install`. This will actually install the runtimes defined in the `.tool-versions` file. This might take a few minutes.

## Install Database

The web app uses PostgresSQL as the database.

There are several ways to install Postgres. My preferred method is to [use Docker](https://hub.docker.com/_/postgres). For Mac OS, there's [this](https://postgresapp.com/) (never tested it).

## Install Phoenix and dependencies

To start the Phoenix server:

1. Install dependencies with `mix deps.get`
2. Create and migrate your database with `mix ecto.setup`
3. Install Node.js dependencies with `cd assets && npm install`
4. Start Phoenix with `mix phx.server`
