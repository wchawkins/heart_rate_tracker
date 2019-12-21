defmodule Spo2Web.GraphController do
  use Spo2Web, :controller

  plug :requires_login

  def index(conn, _params) do
    render(conn, "index.html")
  end
end
