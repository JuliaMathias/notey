defmodule NoteyWeb.ErrorHTMLTest do
  @moduledoc "Verifies generic error responses do not expose internal details."
  use NoteyWeb.ConnCase, async: true

  # Bring render_to_string/4 for testing custom views
  import Phoenix.Template, only: [render_to_string: 4]

  test "renders 404.html" do
    assert render_to_string(NoteyWeb.ErrorHTML, "404", "html", []) == "Not Found"
  end

  test "renders 500.html" do
    assert render_to_string(NoteyWeb.ErrorHTML, "500", "html", []) == "Internal Server Error"
  end
end
