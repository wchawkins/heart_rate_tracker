defmodule Spo2Web.PageController do
  use Spo2Web, :controller

  def index(conn, _params) do
    render(conn, "index.html")
  end
end
