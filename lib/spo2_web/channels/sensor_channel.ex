defmodule Spo2Web.SensorChannel do
  use Phoenix.Channel

  def join("sensor:sensorA", _message, socket) do
    {:ok, socket}
  end

  def join("sensor:" <> sensor_id, _params, socket) do
    # TODO: Authentication
    # {:error, %{reason: "unauthorized"}}
    {:ok, %{msg: "You joined the #{sensor_id} topic"}, socket}
  end

  def handle_in("new_data", %{"sample" => sample}, socket) do
    broadcast!(socket, "new_data", %{sample: sample})
    {:noreply, socket}
  end
end
