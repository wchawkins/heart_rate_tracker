defmodule Spo2.Repo.Migrations.CreateSamples do
  use Ecto.Migration
  
  def change do
    create table(:samples) do
      add :spo2, :float
      add :heart_rate, :float
      add :user_id, references(:users), null: false
      
      timestamps()
    end
  end
end
