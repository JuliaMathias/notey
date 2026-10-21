defmodule Notey.Repo.Migrations.CreateFoundationChecks do
  @moduledoc "Creates the synthetic UUID persistence check used by foundation acceptance."
  use Ecto.Migration

  @doc "Creates UUID-backed checks without any personal data fields."
  @spec change() :: term()
  def change do
    create table(:foundation_checks, primary_key: false) do
      add :id, :binary_id, primary_key: true
      timestamps(type: :utc_datetime_usec, updated_at: false)
    end
  end
end
