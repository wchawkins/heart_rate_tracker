# In this file, we load production configuration and secrets
# from environment variables. You can also hardcode secrets,
# although such is generally not recommended and you have to
# remember to add this file to your .gitignore.
import Config
import Spo2.Release, only: [get_env: 1, get_env: 2]

http_port = get_env("HTTP_PORT")
https_port = get_env("HTTPS_PORT")
secret_key_base = get_env("SECRET_KEY_BASE")
ssl_key_path = get_env("SSL_KEY_PATH")
ssl_cert_path = get_env("SSL_CERT_PATH")
host = get_env("HOST")

config :spo2, Spo2Web.Endpoint,
  http: [:inet6, port: http_port],
  https: [
    :inet6,
    port: https_port,
    cipher_suite: :strong,
    keyfile: ssl_key_path,
    certfile: ssl_cert_path
  ],
  force_ssl: [hsts: true],
  url: [host: host, port: https_port],
  server: true

config :spo2, Spo2.Repo,
  url: get_env("DATABASE_URL"),
  pool_size: String.to_integer(get_env("POOL_SIZE", "15"))
