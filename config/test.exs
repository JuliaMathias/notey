import Config

# Configure your database
#
# The MIX_TEST_PARTITION environment variable can be used
# to provide built-in test partitioning in CI environment.
# Run `mix help test` for more information.
config :notey, Notey.Repo,
  username: System.get_env("NOTEY_DB_USER", "notey"),
  password: System.get_env("NOTEY_DB_PASSWORD", "notey_dev_only"),
  hostname: System.get_env("NOTEY_DB_HOST", "127.0.0.1"),
  port: String.to_integer(System.get_env("NOTEY_DB_PORT", "55432")),
  database: "notey_test#{System.get_env("MIX_TEST_PARTITION")}",
  pool: Ecto.Adapters.SQL.Sandbox,
  pool_size: System.schedulers_online() * 2

# We don't run a server during test. If one is required,
# you can enable the server option below.
config :notey, NoteyWeb.Endpoint,
  http: [ip: {127, 0, 0, 1}, port: 4002],
  secret_key_base: "CYtPVq9NNbu0JPa0AWH8Z+OtT8xc4Ap8kC03Vd5SAJGXegvnYIoK5ZQwcJ1XOG3F",
  server: false

# Print only warnings and errors during test
config :logger, level: :warning

# Initialize plugs at runtime for faster test compilation
config :phoenix, :plug_init_mode, :runtime

# Enable helpful, but potentially expensive runtime checks
config :phoenix_live_view,
  enable_expensive_runtime_checks: true

# Sort query params output of verified routes for robust url comparisons
config :phoenix,
  sort_verified_routes_query_params: true
