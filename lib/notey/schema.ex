defmodule Notey.Schema do
  @moduledoc """
  Ecto schema defaults shared by Notey records: UUID keys and UTC timestamps.

  This only configures schemas; migrations must still use matching SQL types.
  """

  @doc "Applies Notey's primary-key, association-key and timestamp conventions."
  defmacro __using__(_opts) do
    quote do
      use Ecto.Schema
      @primary_key {:id, :binary_id, autogenerate: true}
      @foreign_key_type :binary_id
      @timestamps_opts [type: :utc_datetime_usec]
    end
  end
end
