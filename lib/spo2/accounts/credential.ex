defmodule Spo2.Accounts.Credential do
  use Ecto.Schema
  import Ecto.Changeset
  alias Spo2.Accounts.User
  alias Comeonin.Bcrypt

  schema "credentials" do
    field :email, :string
    field :password, :string, virtual: true
    field :hashed_password, :string
    field :session_secret, :string
    belongs_to :user, User

    timestamps()
  end

  @doc false
  def changeset(credential, attrs) do
    credential
    |> cast(attrs, [:email, :password, :hashed_password])
    |> validate_required([:email, :password])
    |> unique_constraint(:email)
    |> validate_length(:password, min: 6)
    |> put_change(:hashed_password, Bcrypt.hashpwsalt(attrs["password"]))
  end
end
