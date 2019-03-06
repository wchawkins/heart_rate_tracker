defmodule Spo2Web.PageController do
  use Spo2Web, :controller
  
  plug :redirect_logged_in_user

  def index(conn, _params) do
    render(conn, "index.html")
  end
  
  defp redirect_logged_in_user(conn, _opts) do
    case conn.assigns.current_user do
      nil -> conn
      _ -> redirect(conn, to: Routes.dashboard_path(conn, :index))
    end
  end
end
