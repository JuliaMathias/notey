defmodule NoteyWeb.HealthControllerTest do
  @moduledoc "Checks the deployed readiness HTTP contract against real PostgreSQL."
  use NoteyWeb.ConnCase, async: true

  test "readiness returns a small non-sensitive response", %{conn: conn} do
    assert conn |> get(~p"/health") |> json_response(200) == %{"status" => "ok"}
  end
end
