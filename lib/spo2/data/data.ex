defmodule Spo2.Data do
  @moduledoc """
  The Data context
  """
  alias Spo2.Data.Sample
  
  import Ecto.Query, warn: false
  alias Spo2.Repo
  
  def save_sample(attrs \\ %{}) do
    %Sample{}
    |> Sample.changeset(attrs)
    |> Repo.insert()
  end
end
