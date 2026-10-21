defmodule NoteyWeb.FoundationLiveTest do
  @moduledoc "Checks the real LiveView event, database write and reload path."
  use NoteyWeb.ConnCase, async: true
  import Phoenix.LiveViewTest
  import Notey.Factory

  test "opening the page displays an existing connection check", %{conn: conn} do
    check = insert(:foundation_check, inserted_at: ~U[2026-01-02 00:00:00.000000Z])
    assert {:ok, view, _html} = live(conn, ~p"/")
    assert has_element?(view, "#check-id", check.id)
    assert has_element?(view, "#check-result", "Saved successfully.")
  end

  test "saving a check persists a UUID and survives a new page mount", %{conn: conn} do
    assert {:ok, view, _html} = live(conn, ~p"/")
    assert has_element?(view, "#check-result", "No connection check saved yet.")
    view |> element("#save-check") |> render_click()
    check = Notey.Foundation.latest_check()
    assert check != nil
    assert has_element?(view, "#check-id", check.id)
    assert {:ok, reloaded, _html} = live(conn, ~p"/")
    assert has_element?(reloaded, "#check-id", check.id)
    assert has_element?(reloaded, "h1", "Notey")
  end
end
