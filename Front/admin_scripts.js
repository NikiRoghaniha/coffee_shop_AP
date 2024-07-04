document.addEventListener('DOMContentLoaded', function() {
  const menuIcon = document.getElementById('menu-icon');
  const menu = document.getElementById('menu');
  const sidebar = document.getElementById('sidebar');
  const productList = document.getElementById('product-list');

  menuIcon.addEventListener('click', function() {
      sidebar.style.display = sidebar.style.display === 'block' ? 'none' : 'block';
  });

  const products = [
      { id: 1, name: 'Espresso', vertical: 'Coffee', price: '$3.00' },
      { id: 2, name: 'Latte', vertical: 'Coffee', price: '$4.50' },
      { id: 3, name: 'Green Tea', vertical: 'Tea', price: '$2.50' },
      { id: 4, name: 'Black Tea', vertical: 'Tea', price: '$2.00' },
      { id: 5, name: 'Chocolate Croissant', vertical: 'Pastries', price: '$3.50' },
      { id: 6, name: 'Blueberry Muffin', vertical: 'Pastries', price: '$2.75' },
      { id: 7, name: 'Sandwich', vertical: 'Snacks', price: '$5.00' },
      { id: 8, name: 'Cookies', vertical: 'Snacks', price: '$1.50' }
  ];

  const loadProducts = (vertical) => {
      productList.innerHTML = '';
      const filteredProducts = products.filter(product => product.vertical === vertical);
      filteredProducts.forEach(product => {
          const productDiv = document.createElement('div');
          productDiv.classList.add('product');
          productDiv.innerHTML = `
              <h3>${product.name}</h3>
              <p>${product.price}</p>
          `;
          productList.appendChild(productDiv);
      });
  };

  sidebar.addEventListener('click', function(e) {
      if (e.target.tagName === 'LI') {
          const vertical = e.target.getAttribute('data-vertical');
          loadProducts(vertical);
          sidebar.style.display = 'none'; // Close sidebar on selection
      }
  });

  // Load default products on page load
  loadProducts('Coffee');
});



document.addEventListener('DOMContentLoaded', function() {
  const adminName = document.getElementById('admin-name');
  adminName.textContent = 'Admin Name'; // Set admin name dynamically if needed

  const productSelect = document.getElementById('product-select');
  const timeSelect = document.getElementById('time-select');
  const ctx = document.getElementById('sales-chart').getContext('2d');

  let chart;

  const salesData = {
      coffee: {
          daily: [12, 19, 3, 5, 2, 3],
          weekly: [70, 60, 80, 81, 56, 55, 40],
          monthly: [300, 400, 200, 450, 500, 400, 300]
      },
      tea: {
          daily: [15, 10, 5, 8, 3, 2],
          weekly: [60, 70, 90, 80, 60, 70, 50],
          monthly: [250, 350, 300, 400, 450, 350, 300]
      },
      pastries: {
          daily: [20, 25, 30, 35, 40, 45],
          weekly: [90, 80, 70, 100, 120, 110, 130],
          monthly: [400, 500, 450, 550, 600, 500, 400]
      },
      snacks: {
          daily: [10, 20, 30, 40, 50, 60],
          weekly: [50, 60, 70, 80, 90, 100, 110],
          monthly: [200, 300, 400, 500, 600, 700, 800]
      }
  };

  function loadChartData(product, timePeriod) {
      const data = salesData[product][timePeriod];
      const labels = timePeriod === 'daily' ? ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'] :
          timePeriod === 'weekly' ? ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7'] :
          ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'];

      if (chart) {
          chart.destroy();
      }

      chart = new Chart(ctx, {
          type: 'bar',
          data: {
              labels: labels,
              datasets: [{
                  label: `${product.charAt(0).toUpperCase() + product.slice(1)} Sales`,
                  data: data,
                  backgroundColor: 'rgba(54, 162, 235, 0.2)',
                  borderColor: 'rgba(54, 162, 235, 1)',
                  borderWidth: 1
              }]
          },
          options: {
              scales: {
                  y: {
                      beginAtZero: true
                  }
              }
          }
      });
  }

  productSelect.addEventListener('change', function() {
      loadChartData(productSelect.value, timeSelect.value);
  });

  timeSelect.addEventListener('change', function() {
      loadChartData(productSelect.value, timeSelect.value);
  });

  // Load initial chart data
  loadChartData('coffee', 'daily');
});

document.addEventListener('DOMContentLoaded', function() {
  const adminName = document.getElementById('admin-name');
  adminName.textContent = 'Admin Name'; // Set admin name dynamically if needed

  const updateInventory = (ingredient) => {
      const quantityInput = document.getElementById(`${ingredient}-quantity`);
      const stockDisplay = document.getElementById(`${ingredient}-stock`);

      const newQuantity = quantityInput.value;
      if (newQuantity && !isNaN(newQuantity)) {
          stockDisplay.textContent = `${newQuantity} kg`;
          quantityInput.value = ''; // Clear the input after update
          alert(`${ingredient.charAt(0).toUpperCase() + ingredient.slice(1)} updated to ${newQuantity} kg`);
      } else {
          alert('Please enter a valid quantity.');
      }
  };

  window.updateInventory = updateInventory;
});

document.addEventListener('DOMContentLoaded', function() {
  const adminName = document.getElementById('admin-name');
  adminName.textContent = 'Admin Name'; // Set admin name dynamically if needed

  const addProductForm = document.getElementById('add-product-form');
  
  addProductForm.addEventListener('submit', function(event) {
      event.preventDefault();
      
      const productName = document.getElementById('product-name').value;
      const productImage = document.getElementById('product-image').files[0];
      const productCategory = document.getElementById('product-category').value;
      const productPrice = document.getElementById('product-price').value;
      const sugarAmount = document.getElementById('sugar-amount').value;
      const coffeeAmount = document.getElementById('coffee-amount').value;
      const flourAmount = document.getElementById('flour-amount').value;
      const chocolateAmount = document.getElementById('chocolate-amount').value;

      // Assuming you are storing the products in local storage for simplicity
      let products = JSON.parse(localStorage.getItem('products')) || [];
      
      const newProduct = {
          name: productName,
          image: URL.createObjectURL(productImage),
          category: productCategory,
          price: productPrice,
          ingredients: {
              sugar: sugarAmount,
              coffee: coffeeAmount,
              flour: flourAmount,
              chocolate: chocolateAmount
          }
      };

      products.push(newProduct);
      localStorage.setItem('products', JSON.stringify(products));

      alert('Product added successfully!');
      
      // Reset the form
      addProductForm.reset();
  });
});


document.addEventListener('DOMContentLoaded', function() {
  const signupForm = document.getElementById('signup-form');
  const usernameInput = document.getElementById('username');
  const usernameError = document.getElementById('username-error');

  const predefinedAdmins = ['admin1', 'admin2', 'admin3']; // Predefined admin usernames
  const users = JSON.parse(localStorage.getItem('users')) || [];

  signupForm.addEventListener('submit', function(event) {
      event.preventDefault();

      const givenName = document.getElementById('given-name').value;
      const surname = document.getElementById('surname').value;
      const username = usernameInput.value;
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      if (predefinedAdmins.includes(username)) {
          usernameError.textContent = 'Username not available.';
          usernameError.style.display = 'block';
          return;
      }

      if (users.some(user => user.username === username)) {
          usernameError.textContent = 'Username already taken.';
          usernameError.style.display = 'block';
          return;
      }

      const newUser = {
          givenName: givenName,
          surname: surname,
          username: username,
          email: email,
          password: password
      };

      users.push(newUser);
      localStorage.setItem('users', JSON.stringify(users));

      alert('Account created successfully!');
      signupForm.reset();
      window.location.href = 'index.html'; // Redirect to home page after sign-up
  });

  usernameInput.addEventListener('input', function() {
      usernameError.style.display = 'none';
  });
});


document.addEventListener('DOMContentLoaded', function() {
  const signinForm = document.getElementById('signin-form');
  const loginError = document.getElementById('login-error');

  const predefinedAdmins = ['admin1', 'admin2', 'admin3']; // Predefined admin usernames
  const users = JSON.parse(localStorage.getItem('users')) || [];

  signinForm.addEventListener('submit', function(event) {
      event.preventDefault();

      const usernameEmail = document.getElementById('username-email').value;
      const password = document.getElementById('password').value;

      const user = users.find(user => 
          (user.username === usernameEmail || user.email === usernameEmail) && user.password === password
      );

      if (user) {
          if (predefinedAdmins.includes(user.username)) {
              window.location.href = 'shop_management.html'; // Redirect to Shop Management page for admins
          } else {
              window.location.href = 'index.html'; // Redirect to Home page for users
          }
      } else {
          loginError.textContent = 'Invalid username/email or password.';
          loginError.style.display = 'block';
      }
  });
});
