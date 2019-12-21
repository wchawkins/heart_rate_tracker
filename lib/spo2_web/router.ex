defmodule Spo2Web.Router do
  use Spo2Web, :router

  pipeline :browser do
    plug :accepts, ["html"]
    plug :fetch_session
    plug :fetch_flash
    plug :protect_from_forgery
    plug :put_secure_browser_headers
    plug :login
  end

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", Spo2Web do
    pipe_through :browser

    get "/", PageController, :index
    get "/login", SessionController, :new
    post "/login", SessionController, :create
    get "/logout", SessionController, :delete
    get "/graph", GraphController, :index
    resources "/data", DataController
    get "/users/new", UserController, :new
    post "/users", UserController, :create
    get "/dashboard", DashboardController, :index

    # Sample Data
    get "spo2", DashboardController, :spo2
    get "hr", DashboardController, :heart_rate
    get "temperature", DashboardController, :skin_temp
  end

  # Other scopes may use custom stacks.
  # scope "/api", Spo2Web do
  #   pipe_through :api
  # end
end
