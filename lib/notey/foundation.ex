defmodule Notey.Foundation do
  @moduledoc """
  Persists synthetic foundation checks through Notey.Repo.

  It exercises a real database round trip without implementing study-session
  features or contacting remote AI services.
  """
  alias Notey.Foundation.Check
  alias Notey.Repo
  import Ecto.Query

  @doc "Saves a synthetic check with an automatically generated UUID."
  @spec save_check() :: {:ok, Check.t()} | {:error, Ecto.Changeset.t()}
  def save_check, do: Repo.insert(%Check{})

  @doc "Returns the most recently inserted synthetic check, or nil."
  @spec latest_check() :: Check.t() | nil
  def latest_check do
    Repo.one(from c in Check, order_by: [desc: c.inserted_at, desc: c.id], limit: 1)
  end
end
