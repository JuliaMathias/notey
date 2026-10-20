defmodule Notey.Repo do
  @moduledoc "PostgreSQL access boundary for Notey application records."
  use Ecto.Repo,
    otp_app: :notey,
    adapter: Ecto.Adapters.Postgres
end
