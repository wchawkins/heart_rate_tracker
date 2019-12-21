defmodule Spo2Web.Helpers.Auth do
  def signed_in?(conn) do
    user_id = Plug.Conn.get_session(conn, :user_id)
    # if user_id, do: !!Spo2.Accounts.get
  end
end
