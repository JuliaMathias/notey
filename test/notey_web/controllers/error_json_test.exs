defmodule NoteyWeb.ErrorJSONTest do
  @moduledoc "Verifies generic error responses do not expose internal details."
  use NoteyWeb.ConnCase, async: true

  test "renders 404" do
    assert NoteyWeb.ErrorJSON.render("404.json", %{}) == %{errors: %{detail: "Not Found"}}
  end

  test "renders 500" do
    assert NoteyWeb.ErrorJSON.render("500.json", %{}) ==
             %{errors: %{detail: "Internal Server Error"}}
  end
end
