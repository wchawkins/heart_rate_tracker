defmodule Spo2Web.Router do
  use Spo2Web, :router

  pipeline :browser do
    plug :accepts, ["html"]
    plug :fetch_session
    plug :fetch_flash
    plug :protect_from_forgery
    plug :put_secure_browser_headers
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
  end

  # Other scopes may use custom stacks.
  # scope "/api", Spo2Web do
  #   pipe_through :api
  # end
end
