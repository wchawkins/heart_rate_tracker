defmodule Spo2.Accounts.Credential do
  use Ecto.Schema
  import Ecto.Changeset
  alias Spo2.Accounts.User

  schema "credentials" do
    field :email, :string
    field :hashed_password, :string
    field :session_secret, :string
    belongs_to :user, User

    timestamps()
  end

  @doc false
  def changeset(credential, attrs) do
    credential
    |> cast(attrs, [:email])
    |> validate_required([:email])
    |> unique_constraint(:email)
  end
end
