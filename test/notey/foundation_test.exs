defmodule Notey.FoundationTest do
  @moduledoc "Exercises real PostgreSQL UUID storage and reload without remote services."
  use Notey.DataCase, async: true
  import Notey.Factory
  alias Notey.Foundation

  test "latest check uses timestamp first and UUID to resolve equal timestamps" do
    insert(:foundation_check,
      id: "00000000-0000-0000-0000-000000000009",
      inserted_at: ~U[2026-01-01 00:00:00.000000Z]
    )

    newest =
      insert(:foundation_check,
        id: "00000000-0000-0000-0000-000000000003",
        inserted_at: ~U[2026-01-02 00:00:00.000000Z]
      )

    insert(:foundation_check,
      id: "00000000-0000-0000-0000-000000000002",
      inserted_at: newest.inserted_at
    )

    assert Foundation.latest_check().id == newest.id
  end

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
