import { createClient } from "redis";

function redisConnect() {
  const client = createClient();

  client.on("connect", () => {
    console.log("Redis client connected to the server");
  });

  client.on("error", (err) => {
    console.error(`Redis client not connected to the server: ${err.message}`);
  });
}

redisConnect();
