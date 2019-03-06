defmodule Spo2Web.DashboardController do
  use Spo2Web, :controller
  
  plug :requires_login
  
  def index(conn, _opts) do
    render(conn, "index.html")
  end
end
