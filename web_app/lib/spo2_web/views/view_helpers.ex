defmodule Spo2Web.ViewHelpers do
  def logged_in?(conn) do
    # !!conn.assigns[:current_user]
    !!Plug.Conn.get_session(conn, :user_id)
  end
end
