defmodule Notey.FoundationTest do
  @moduledoc "Exercises real PostgreSQL UUID storage and reload without remote services."
  use Notey.DataCase, async: true
  alias Notey.Foundation

  test "a saved synthetic check reloads with a UUID and UTC timestamp" do
    assert Foundation.latest_check() == nil
    assert {:ok, check} = Foundation.save_check()
    assert {:ok, check.id} == Ecto.UUID.cast(check.id)
    assert check.inserted_at.time_zone == "Etc/UTC"
    assert Foundation.latest_check().id == check.id
    assert Repo.get!(Notey.Foundation.Check, check.id).id == check.id

    result =
      Ecto.Adapters.SQL.query!(
        Repo,
        "SELECT data_type FROM information_schema.columns WHERE table_name = 'foundation_checks' AND column_name = 'id'",
        []
      )

    assert result.rows == [["uuid"]]
  end
end
