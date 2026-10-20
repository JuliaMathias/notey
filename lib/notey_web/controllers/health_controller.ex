defmodule NoteyWeb.HealthController do
  @moduledoc "Minimal readiness response for release health checks; never includes secrets."
  use NoteyWeb, :controller

  @doc "Returns 200 for a ready database and 503 when the application cannot serve it."
  @spec show(Plug.Conn.t(), map()) :: Plug.Conn.t()
  def show(conn, _params) do
    if Notey.Health.ready?() do
      json(conn, %{status: "ok"})
    else
      conn |> put_status(:service_unavailable) |> json(%{status: "unavailable"})
    end
  end
end
