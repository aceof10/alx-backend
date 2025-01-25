import express from "express";
import { promisify } from "util";
import redis from "redis";

const app = express();
const port = 1245;
const redisClient = redis.createClient();
const getAsync = promisify(redisClient.get).bind(redisClient);

const listProducts = [
  {
    itemId: 1,
    itemName: "Suitcase 250",
    price: 50,
    initialAvailableQuantity: 4,
  },
  {
    itemId: 2,
    itemName: "Suitcase 450",
    price: 100,
    initialAvailableQuantity: 10,
  },
  {
    itemId: 3,
    itemName: "Suitcase 650",
    price: 350,
    initialAvailableQuantity: 2,
  },
  {
    itemId: 4,
    itemName: "Suitcase 1050",
    price: 550,
    initialAvailableQuantity: 5,
  },
];

function getItemById(id) {
  return listProducts.find((product) => product.itemId === id);
}

function reserveStockById(itemId, stock) {
  redisClient.set(`item.${itemId}`, stock);
}

async function getCurrentReservedStockById(itemId) {
  const stock = await getAsync(`item.${itemId}`);
  return stock ? parseInt(stock, 10) : null;
}

app.get("/list_products", (req, res) => {
  res.json(listProducts);
});

app.get("/list_products/:itemId", async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const item = getItemById(itemId);

  if (!item) {
    return res.json({ status: "Product not found" });
  }

  const currentStock =
    (await getCurrentReservedStockById(itemId)) ??
    item.initialAvailableQuantity;

  res.json({
    ...item,
    currentQuantity: currentStock,
  });
});

app.get("/reserve_product/:itemId", async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const item = getItemById(itemId);

  if (!item) {
    return res.json({ status: "Product not found" });
  }

  const currentStock =
    (await getCurrentReservedStockById(itemId)) ??
    item.initialAvailableQuantity;

  if (currentStock <= 0) {
    return res.json({ status: "Not enough stock available", itemId });
  }

  reserveStockById(itemId, currentStock - 1);
  res.json({ status: "Reservation confirmed", itemId });
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
