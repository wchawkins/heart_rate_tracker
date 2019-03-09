defmodule Spo2.Data do
  @moduledoc """
  The Data context
  """
  alias Spo2.Data.Sample
  alias Spo2.Accounts.User

  import Ecto.Query, warn: false
  alias Spo2.Repo

  def save_sample(%User{} = user, attrs \\ %{}) do
    %Sample{}
    |> Sample.changeset(attrs)
    |> Ecto.Changeset.put_change(:user_id, user.id)
    |> Repo.insert()
  end
end
