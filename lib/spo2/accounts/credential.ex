defmodule Spo2.Accounts.Credential do
  use Ecto.Schema
  import Ecto.Changeset

  schema "credentials" do
    field :email, :string
    field :hashed_password, :string
    field :session_secret, :string
    field :user_id, :id

    timestamps()
  end

  @doc false
  def changeset(credential, attrs) do
    credential
    |> cast(attrs, [:email, :hashed_password, :session_secret])
    |> validate_required([:email, :hashed_password, :session_secret])
    |> unique_constraint(:email)
  end
end
