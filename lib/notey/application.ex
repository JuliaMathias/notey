defmodule Notey.Application do
  # See https://hexdocs.pm/elixir/Application.html
  # for more information on OTP Applications
  @moduledoc "Supervises Notey database access, telemetry and web services."

  use Application

  @impl true
  @doc "Starts database, telemetry, PubSub and the web endpoint under supervision."
  @spec start(Application.start_type(), term()) :: Supervisor.on_start()
  def start(_type, _args) do
    children = [
      NoteyWeb.Telemetry,
      Notey.Repo,
      {DNSCluster, query: Application.get_env(:notey, :dns_cluster_query) || :ignore},
      {Phoenix.PubSub, name: Notey.PubSub},
      # Start a worker by calling: Notey.Worker.start_link(arg)
      # {Notey.Worker, arg},
      # Start to serve requests, typically the last entry
      NoteyWeb.Endpoint
    ]

    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: Notey.Supervisor]
    Supervisor.start_link(children, opts)
  end

  # Tell Phoenix to update the endpoint configuration
  # whenever the application is updated.
  @impl true
  @doc "Forwards changed runtime endpoint settings during an application upgrade."
  @spec config_change(keyword(), keyword(), [atom()]) :: :ok
  def config_change(changed, _new, removed) do
    NoteyWeb.Endpoint.config_change(changed, removed)
    :ok
  end
end
