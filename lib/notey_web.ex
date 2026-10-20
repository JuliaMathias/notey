defmodule NoteyWeb do
  @moduledoc """
  The entrypoint for defining your web interface, such
  as controllers, components, channels, and so on.

  This can be used in your application as:

      use NoteyWeb, :controller
      use NoteyWeb, :html

  The definitions below will be executed for every controller,
  component, etc, so keep them short and clean, focused
  on imports, uses and aliases.

  Do NOT define functions inside the quoted expressions
  below. Instead, define additional modules and import
  those modules here.
  """

  @doc "Lists the public static paths served by the endpoint."
  @spec static_paths() :: [String.t()]
  def static_paths, do: ~w(assets fonts images favicon.ico robots.txt)

  @doc "Builds the router imports and verified route setup."
  @spec router() :: Macro.t()
  def router do
    quote do
      use Phoenix.Router, helpers: false

      # Import common connection and controller functions to use in pipelines
      import Plug.Conn
      import Phoenix.Controller
      import Phoenix.LiveView.Router
    end
  end

  @doc "Builds the shared Phoenix channel setup."
  @spec channel() :: Macro.t()
  def channel do
    quote do
      use Phoenix.Channel
    end
  end

  @doc "Builds the controller setup and route helpers."
  @spec controller() :: Macro.t()
  def controller do
    quote do
      use Phoenix.Controller, formats: [:html, :json]

      use Gettext, backend: NoteyWeb.Gettext

      import Plug.Conn

      unquote(verified_routes())
    end
  end

  @doc "Builds the LiveView setup and shared HTML helpers."
  @spec live_view() :: Macro.t()
  def live_view do
    quote do
      use Phoenix.LiveView

      unquote(html_helpers())
    end
  end

  @doc "Builds the LiveComponent setup and shared HTML helpers."
  @spec live_component() :: Macro.t()
  def live_component do
    quote do
      use Phoenix.LiveComponent

      unquote(html_helpers())
    end
  end

  @doc "Builds the function-component and HTML helper setup."
  @spec html() :: Macro.t()
  def html do
    quote do
      use Phoenix.Component

      # Import convenience functions from controllers
      import Phoenix.Controller,
        only: [get_csrf_token: 0, view_module: 1, view_template: 1]

      # Include general helpers for rendering HTML
      unquote(html_helpers())
    end
  end

  @doc false
  # Keep this implementation helper private to its module.
  @spec html_helpers() :: Macro.t()
  defp html_helpers do
    quote do
      # Translation
      use Gettext, backend: NoteyWeb.Gettext

      # HTML escaping functionality
      import Phoenix.HTML
      # Core UI components
      import NoteyWeb.CoreComponents

      # Common modules used in templates
      alias Phoenix.LiveView.JS
      alias NoteyWeb.Layouts

      # Routes generation with the ~p sigil
      unquote(verified_routes())
    end
  end

  @doc "Builds compile-time verified routes for the configured endpoint."
  @spec verified_routes() :: Macro.t()
  def verified_routes do
    quote do
      use Phoenix.VerifiedRoutes,
        endpoint: NoteyWeb.Endpoint,
        router: NoteyWeb.Router,
        statics: NoteyWeb.static_paths()
    end
  end

  @doc """
  When used, dispatch to the appropriate controller/live_view/etc.
  """
  defmacro __using__(which) when is_atom(which) do
    apply(__MODULE__, which, [])
  end
end
