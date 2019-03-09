defmodule Spo2.Repo.Migrations.UpdateSamples do
  use Ecto.Migration

  def change do
    alter table(:samples) do
      add :red_buffer, {:array, :float}
      add :ir_buffer, {:array, :float}
    end
  end
end
