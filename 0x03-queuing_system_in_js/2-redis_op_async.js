import { createClient } from "redis";
import { promisify } from "util";

const client = createClient();

client.on("connect", () => {
  console.log("Redis client connected to the server");
});

client.on("error", (err) => {
  console.error(`Redis client not connected to the server: ${err.message}`);
});

const getAsync = promisify(client.get).bind(client);

async function displaySchoolValue(schoolName) {
  try {
    const value = await getAsync(schoolName);
    console.log(value);
  } catch (err) {
    console.error(err);
  }
}

function setNewSchool(schoolName, value) {
  client.set(schoolName, value, (err, reply) => {
    if (err) {
      console.error(err);
    } else {
      console.log(reply);
    }
  });
}

(async () => {
  await displaySchoolValue("ALX");
  setNewSchool("ALXSanFrancisco", "100");
  await displaySchoolValue("ALXSanFrancisco");
})();
