defmodule Spo2Web.ControllerHelpers do
  import Phoenix.Controller
  import Plug.Conn, only: [halt: 1]
  alias Spo2Web.Router.Helpers, as: Routes

  def requires_login(conn, _opts) do
    if logged_in?(conn) do
      conn
    else
      conn
      |> put_flash(:error, "You must sign in to view that page")
      |> redirect(to: Routes.session_path(conn, :new))
      |> halt
    end
  end

  def logged_in?(conn) do
    !!conn.assigns[:current_user]
  end
end
