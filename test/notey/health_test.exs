defmodule Notey.HealthTest do
  @moduledoc "Verifies readiness error handling without stopping a real database or sleeping."
  use ExUnit.Case, async: true

  test "a query failure is unavailable, not a successful readiness check" do
    refute Notey.Health.ready?(fn -> {:error, :disconnected} end)
    refute Notey.Health.ready?(fn -> raise DBConnection.ConnectionError, "synthetic failure" end)
  end

  test "readiness needs the expected SQL response" do
    assert Notey.Health.ready?(fn -> {:ok, %{rows: [[1]]}} end)
    refute Notey.Health.ready?(fn -> {:ok, %{rows: []}} end)
  end
end
