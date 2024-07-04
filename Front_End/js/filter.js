const btns = [
  {
    category: 2,
    name: "Coffee",
  },
  {
    category: 3,
    name: "Tea",
  },
  {
    category: 4,
    name: "Pastries",
  },
  {
    category: 5,
    name: "Snacks",
  },
];

const urlParams = new URLSearchParams(window.location.search);
const category = urlParams.get("category");

const products = [];
const fetchAndDisplay = async () => {
  try {
    const responses = await Promise.all([
      fetch("http://127.0.0.1:8000/api/categories/tea/"),
      fetch("http://127.0.0.1:8000/api/categories/pastries/"),
      fetch("http://127.0.0.1:8000/api/categories/coffee/"),
      fetch("http://127.0.0.1:8000/api/categories/snacks/"),
    ]);

    const dataes = await Promise.all(
      responses.map((response) => response.json())
    );

    dataes.forEach((d) => {
      products.push(...d.products);
    });

    // Render items after fetching
    displayItem(products);
  } catch (error) {
    console.error("Error fetching the API data", error);
  }
  if (category) {
    filterItems(category);
  }
};

fetchAndDisplay();

const filters = [...new Set(btns)];

document.getElementById("btns").innerHTML = filters
  .map((btn) => {
    var { name, category } = btn;
    return `<button class='fil-p' onclick='filterItems(${category})'>${name}</button>`;
  })
  .join("");

console.log(products);
const categories = [...products];

const filterItems = (category) => {
  const filteredCategories = products.filter(
    (item) => +item.category == +category
  );
  displayItem(filteredCategories);
};

const displayItem = (items) => {
  const result = items
    .map((item) => {
      const { id, name, image, price } = item;
      return `<div class='box' id="${id}">
                <h3>${name}</h3>
                <div class='img-box'>
                <img class='images' src=${image}></img>
                </div>
                <div class='bottom'>
                <h2>$ ${price}</h2>
                <button onclick="addToCard(${id})">Add to cart</button>
                </div>
                </div>`;
    })
    .join("");

  document.getElementById("root").innerHTML = result;
};

displayItem(categories);
