# This file is responsible for configuring your application
# and its dependencies with the aid of the Mix.Config module.
#
# This configuration file is loaded before any dependency and
# is restricted to this project.

# General application configuration
use Mix.Config

config :spo2,
  ecto_repos: [Spo2.Repo]

# Configures the endpoint
config :spo2, Spo2Web.Endpoint,
  url: [host: "localhost"],
  secret_key_base: "IXSEecOw4UxFnX+R7w8aMKzzOlgaquQJp9kSO6P8t8Kv/xcZBhLqKyHq8ZBd7Qcc",
  render_errors: [view: Spo2Web.ErrorView, accepts: ~w(html json)],
  pubsub: [name: Spo2.PubSub, adapter: Phoenix.PubSub.PG2]

# Configures Elixir's Logger
config :logger, :console,
  format: "$time $metadata[$level] $message\n",
  metadata: [:request_id]

# Use Jason for JSON parsing in Phoenix
config :phoenix, :json_library, Jason

# Doorman authentication library
config :doorman,
  repo: Spo2.Repo,
  secure_with: Doorman.Auth.Bcrypt,
  user_module: Spo2.Accounts.User

# Import environment specific config. This must remain at the bottom
# of this file so it overrides the configuration defined above.
import_config "#{Mix.env()}.exs"
