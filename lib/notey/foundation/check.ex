defmodule Notey.Foundation.Check do
  @moduledoc "A synthetic connection-check record; contains no session or user material."
  use Notey.Schema

  schema "foundation_checks" do
    timestamps(updated_at: false)
  end

  @type t :: %__MODULE__{id: Ecto.UUID.t() | nil, inserted_at: DateTime.t() | nil}
end
