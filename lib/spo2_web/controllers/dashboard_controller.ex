defmodule Spo2Web.DashboardController do
  use Spo2Web, :controller

  plug :requires_login

  def index(conn, _opts) do
    render(conn, "index.html")
  end

  # Maybe this should be called the "SampleController" since technically
  # that's what we're wanting to render
  def spo2(conn, _opts) do
    render(conn, "graph.html", name: "spo2", title: "SpO2")
  end

  def heart_rate(conn, _opts) do
    render(conn, "graph.html", name: "heart_rate", title: "Heart Rate")
  end

  def skin_temp(conn, _opts) do
    render(conn, "graph.html", name: "temp", title: "Skin Temperature")
  end
end
