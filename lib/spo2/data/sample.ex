defmodule Spo2.Data.Sample do
  use Ecto.Schema
  import Ecto.Changeset
  alias Spo2.Accounts.User

  schema "samples" do
    field :spo2, :float
    field :heart_rate, :float
    field :red_buffer, {:array, :float}
    field :ir_buffer, {:array, :float}
    field :temp, :float
    belongs_to :user, User

    timestamps()
  end

  @doc false
  def changeset(sample, attrs) do
    sample
    |> cast(attrs, [:spo2, :heart_rate, :red_buffer, :ir_buffer, :temp])
  end
end
