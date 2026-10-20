defmodule NoteyWeb.FoundationLive do
  @moduledoc "Minimal deployed foundation screen; tests LiveView and PostgreSQL together."
  use NoteyWeb, :live_view
  alias Notey.Foundation

  @doc "Loads the last database check so persistence is observable after reload."
  @spec mount(map(), map(), Phoenix.LiveView.Socket.t()) :: {:ok, Phoenix.LiveView.Socket.t()}
  @impl true
  def mount(_params, _session, socket) do
    {:ok, assign(socket, page_title: "Notey", check: Foundation.latest_check(), error: nil)}
  end

  @doc "Persists a synthetic check only after the user requests one."
  @spec handle_event(String.t(), map(), Phoenix.LiveView.Socket.t()) ::
          {:noreply, Phoenix.LiveView.Socket.t()}
  @impl true
  def handle_event("save-check", _params, socket) do
    case Foundation.save_check() do
      {:ok, check} -> {:noreply, assign(socket, check: check, error: nil)}
      {:error, _changeset} -> {:noreply, assign(socket, error: "The check could not be saved.")}
    end
  rescue
    _error in [DBConnection.ConnectionError, Postgrex.Error] ->
      {:noreply, assign(socket, error: "The database is unavailable. Please try again.")}
  end

  @doc "Renders the honest foundation status and the persistence test control."
  @spec render(map()) :: Phoenix.LiveView.Rendered.t()
  @impl true
  def render(assigns) do
    ~H"""
    <Layouts.app flash={@flash}>
      <p class="text-sm font-semibold uppercase tracking-widest text-base-content/70">
        Study notes, with their sources
      </p>
      <h1 class="text-4xl font-semibold tracking-tight sm:text-5xl">Notey</h1>
      <p class="max-w-xl text-lg leading-relaxed">
        The foundation is running. Session uploads, transcription and note generation are being built.
      </p>
      <section aria-labelledby="connection-heading" class="mt-8 border-t border-base-300 pt-6">
        <h2 id="connection-heading" class="text-xl font-semibold">Connection check</h2>
        <p class="mt-2 text-base-content/80">
          Save a synthetic record to check LiveView and PostgreSQL. Reload to confirm it was kept.
        </p>
        <button
          id="save-check"
          phx-click="save-check"
          phx-disable-with="Saving…"
          class="btn btn-neutral mt-5 min-h-12"
        >
          Save connection check
        </button>
        <div id="check-result" role="status" aria-live="polite" class="mt-5 space-y-2">
          <p :if={is_nil(@check)}>No connection check saved yet.</p>
          <div :if={@check}>
            <p>Saved successfully.</p>
            <p class="mt-2 text-sm">Record UUID</p>
            <code id="check-id" class="block break-all text-sm">{@check.id}</code>
            <p class="mt-2 text-sm text-base-content/70">
              {@check.inserted_at |> DateTime.to_iso8601()}
            </p>
          </div>
        </div>
        <p :if={@error} id="check-error" role="alert" class="mt-4 text-error">{@error}</p>
      </section>
    </Layouts.app>
    """
  end
end
