defmodule Spo2Web.SensorChannel do
  use Phoenix.Channel

  def join("sensor:" <> sensor_id, _params, socket) do
    # TODO: Authentication
    # {:error, %{reason: "unauthorized"}}
    {:ok, %{msg: "You joined the #{sensor_id} topic"}, socket}
  end

  # handle spo2 and heart rate
  def handle_in("new_data", %{"spo2" => spo2, "hr" => hr}, socket) do
    broadcast!(socket, "new_data", %{spo2: spo2, hr: hr})
    # TODO: Persist data to database
    {:noreply, socket}
  end
end
