defmodule Spo2Web.Plugs do
  import Plug.Conn

  def login(conn, _opts) do
    user_id = get_session(conn, :user_id)
    user = user_id && Spo2.Accounts.get_user!(user_id)

    if user do
      assign(conn, :current_user, user)
    else
      # I wonder if user is nil anyways, do I need this if-else?
      assign(conn, :current_user, nil)
    end
  end
end
