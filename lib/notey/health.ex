defmodule Notey.Health do
  @moduledoc "Checks database readiness without returning connection details to clients."
  alias Ecto.Adapters.SQL

  @doc "Checks SQL readiness; an injected query function keeps failure tests deterministic."
  @spec ready?((-> term())) :: boolean()
  def ready?(query \\ fn -> SQL.query(Notey.Repo, "SELECT 1", []) end) do
    case query.() do
      {:ok, %{rows: [[1]]}} -> true
      _other -> false
    end
  rescue
    _error in [DBConnection.ConnectionError, Postgrex.Error] -> false
  end
end
