defmodule Spo2.Repo.Migrations.AddTempToSample do
  use Ecto.Migration

  def change do
    alter table(:samples) do
      add :temp, :float
    end
  end
end
