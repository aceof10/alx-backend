import express from "express";
import redis from "redis";
import kue from "kue";
import { promisify } from "util";

const app = express();
const port = 1245;
const redisClient = redis.createClient();
const queue = kue.createQueue();
const getAsync = promisify(redisClient.get).bind(redisClient);

let reservationEnabled = true;

function reserveSeat(number) {
  redisClient.set("available_seats", number);
}

async function getCurrentAvailableSeats() {
  const seats = await getAsync("available_seats");
  return seats ? parseInt(seats, 10) : null;
}

app.get("/available_seats", async (req, res) => {
  const seats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: seats });
});

app.get("/reserve_seat", (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: "Reservation are blocked" });
  }

  const job = queue.create("reserve_seat").save((err) => {
    if (!err) {
      res.json({ status: "Reservation in process" });
    } else {
      res.json({ status: "Reservation failed" });
    }
  });

  job.on("complete", () =>
    console.log(`Seat reservation job ${job.id} completed`)
  );
  job.on("failed", (err) =>
    console.log(`Seat reservation job ${job.id} failed: ${err.message}`)
  );
});

app.get("/process", async (req, res) => {
  res.json({ status: "Queue processing" });

  queue.process("reserve_seat", async (job, done) => {
    const seats = await getCurrentAvailableSeats();

    if (seats <= 0) {
      reservationEnabled = false;
      return done(new Error("Not enough seats available"));
    }

    reserveSeat(seats - 1);

    if (seats - 1 === 0) {
      reservationEnabled = false;
    }

    done();
  });
});

reserveSeat(50);

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
