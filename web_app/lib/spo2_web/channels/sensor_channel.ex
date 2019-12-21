defmodule Spo2Web.SensorChannel do
  use Phoenix.Channel
  alias Spo2.Data
  alias Spo2.Accounts

  def join("sensor:" <> sensor_id, _params, socket) do
    # TODO: Authentication
    # {:error, %{reason: "unauthorized"}}
    socket = assign(socket, :username, sensor_id)
    {:ok, %{msg: "You joined the #{sensor_id} topic"}, socket}
  end

  # handle spo2 and heart rate
  def handle_in("new_data", sample, socket) do
    broadcast!(socket, "new_data", sample)
    # Save in database
    user = Accounts.get_user_by_username(socket.assigns.username)
    Data.save_sample(user, sample)
    {:noreply, socket}
  end

  # Not using this currently
  def handle_in("new_raw_data", %{"red_buffer" => red_buffer, "ir_buffer" => ir_buffer}, socket) do
    broadcast!(socket, "new_raw_data", %{red_buffer: red_buffer, ir_buffer: ir_buffer})
    # TODO: Persist data to database
    {:noreply, socket}
  end
end
