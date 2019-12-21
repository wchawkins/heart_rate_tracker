defmodule Spo2.Repo do
  use Ecto.Repo,
    otp_app: :spo2,
    adapter: Ecto.Adapters.Postgres
end
