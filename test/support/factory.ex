defmodule Notey.Factory do
  @moduledoc """
  Builds synthetic test records and inserts them through the sandboxed repository.

  Factories supply test setup, not the application operation under test. Keep
  timestamps and identifiers explicit when a test depends on ordering.
  """
  use ExMachina.Ecto, repo: Notey.Repo

  @doc "Builds an unsaved connection check; Ecto generates its UUID and timestamp on insert."
  @spec foundation_check_factory() :: Notey.Foundation.Check.t()
  def foundation_check_factory, do: %Notey.Foundation.Check{}
end
