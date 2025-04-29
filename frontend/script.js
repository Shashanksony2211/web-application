const backend = "http://127.0.0.1:8000";

// DOM Elements
const loginTab = document.getElementById("loginTab");
const signupTab = document.getElementById("signupTab");
const loginForm = document.getElementById("loginForm");
const signupForm = document.getElementById("signupForm");
const passwordToggles = document.querySelectorAll(".toggle-password");
const socialButtons = document.querySelectorAll(".social-button");

// Tab Switching
loginTab.addEventListener("click", () => {
  loginTab.classList.add("active");
  signupTab.classList.remove("active");
  loginForm.classList.add("active");
  signupForm.classList.remove("active");
});

signupTab.addEventListener("click", () => {
  signupTab.classList.add("active");
  loginTab.classList.remove("active");
  signupForm.classList.add("active");
  loginForm.classList.remove("active");
});

// Password Toggle Visibility
passwordToggles.forEach(toggle => {
  toggle.addEventListener("click", () => {
    const passwordField = toggle.previousElementSibling;
    const icon = toggle.querySelector("i");
    
    if (passwordField.type === "password") {
      passwordField.type = "text";
      icon.classList.remove("fa-eye");
      icon.classList.add("fa-eye-slash");
    } else {
      passwordField.type = "password";
      icon.classList.remove("fa-eye-slash");
      icon.classList.add("fa-eye");
    }
  });
});

// Form Validation
function validatePassword(password) {
  if (password.length <= 3) {
    return "Password must be at least 8 characters long";
  }
}

function showError(inputElement, message) {
  const errorMessage = document.createElement("div");
  errorMessage.className = "error-message";
  errorMessage.textContent = message;
  errorMessage.style.color = "#ef4444";
  errorMessage.style.fontSize = "0.75rem";
  errorMessage.style.marginTop = "4px";
  
  // Remove any existing error messages
  const existingError = inputElement.parentNode.querySelector(".error-message");
  if (existingError) {
    existingError.remove();
  }
  
  inputElement.parentNode.appendChild(errorMessage);
  inputElement.style.borderColor = "#ef4444";
}

function removeError(inputElement) {
  const existingError = inputElement.parentNode.querySelector(".error-message");
  if (existingError) {
    existingError.remove();
  }
  inputElement.style.borderColor = "";
}

// Feedback Notifications
function showNotification(message, type = "success") {
  // Remove existing notifications
  const existingNotification = document.querySelector(".notification");
  if (existingNotification) {
    existingNotification.remove();
  }
  
  const notification = document.createElement("div");
  notification.className = `notification ${type}`;
  notification.textContent = message;
  
  // Style the notification
  notification.style.position = "fixed";
  notification.style.top = "20px";
  notification.style.right = "20px";
  notification.style.padding = "12px 20px";
  notification.style.borderRadius = "8px";
  notification.style.color = "white";
  notification.style.fontWeight = "500";
  notification.style.boxShadow = "0 4px 12px rgba(0, 0, 0, 0.15)";
  notification.style.zIndex = "1000";
  notification.style.animation = "slideIn 0.3s ease forwards";
  
  if (type === "success") {
    notification.style.backgroundColor = "#10b981";
  } else if (type === "error") {
    notification.style.backgroundColor = "#ef4444";
  } else {
    notification.style.backgroundColor = "#6366f1";
  }
  
  document.body.appendChild(notification);
  
  // Add slide-in animation
  const keyframes = `
    @keyframes slideIn {
      from { transform: translateX(100%); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }
  `;
  
  const styleSheet = document.createElement("style");
  styleSheet.textContent = keyframes;
  document.head.appendChild(styleSheet);
  
  // Auto-remove after 4 seconds
  setTimeout(() => {
    notification.style.animation = "slideOut 0.3s ease forwards";
    
    // Add slide-out animation
    const outKeyframes = `
      @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
      }
    `;
    
    const outStyleSheet = document.createElement("style");
    outStyleSheet.textContent = outKeyframes;
    document.head.appendChild(outStyleSheet);
    
    setTimeout(() => {
      notification.remove();
    }, 300);
  }, 4000);
}

// Login Form Submit
loginForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  
  const formData = new FormData(e.target);
  const data = Object.fromEntries(formData.entries());
  
  try {
    const submitButton = loginForm.querySelector("button[type='submit']");
    submitButton.textContent = "Logging in...";
    submitButton.disabled = true;
    
    const res = await fetch(`${backend}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    
    const result = await res.json();
    
    if (res.ok) {
      localStorage.setItem("token", result.access_token);
      showNotification("Login successful! Redirecting...");
      
      setTimeout(() => {
        window.location.href = "dashboard.html";
      }, 1000);
    } else {
      throw new Error(result.detail || "Login failed");
    }
  } catch (error) {
    showNotification(error.message, "error");
  } finally {
    const submitButton = loginForm.querySelector("button[type='submit']");
    submitButton.textContent = "Login";
    submitButton.disabled = false;
  }
});

// Signup Form Submit
signupForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  
  const formData = new FormData(e.target);
  const data = Object.fromEntries(formData.entries());
  
  // Validate password
  const passwordField = document.getElementById("password");
  const passwordError = validatePassword(passwordField.value);
  
  if (passwordError) {
    showError(passwordField, passwordError);
    return;
  } else {
    removeError(passwordField);
  }
  
  try {
    const submitButton = signupForm.querySelector("button[type='submit']");
    submitButton.textContent = "Creating account...";
    submitButton.disabled = true;
    
    const res = await fetch(`${backend}/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    
    const result = await res.json();
    
    if (res.ok) {
      showNotification("Account created successfully!");
      
      // Reset form and switch to login
      signupForm.reset();
      loginTab.click();
    } else {
      throw new Error(result.detail || "Signup failed");
    }
  } catch (error) {
    showNotification(error.message, "error");
  } finally {
    const submitButton = signupForm.querySelector("button[type='submit']");
    submitButton.textContent = "Create Account";
    submitButton.disabled = false;
  }
});

// Social login buttons (placeholder functionality)
socialButtons.forEach(button => {
  button.addEventListener("click", () => {
    let provider = "";
    if (button.classList.contains("google")) provider = "Google";
    if (button.classList.contains("facebook")) provider = "Facebook";
    if (button.classList.contains("apple")) provider = "Apple";
    
    showNotification(`${provider} login is not implemented yet`, "info");
  });
});

// Check for token on page load
document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token");
  if (token) {
    // Optional: Verify token validity with backend
    // If valid, redirect to dashboard
    // window.location.href = "dashboard.html";
  }
});

// document.addEventListener("DOMContentLoaded", () => {
//   const roleDropdown = document.getElementById("roleDropdown");

//   fetch("http://localhost:8000/roles") // Replace with actual backend URL
//     .then(res => res.json())
//     .then(data => {
//       data.forEach(role => {
//         const option = document.createElement("option");
//         option.value = role.id;
//         option.textContent = role.name;
//         roleDropdown.appendChild(option);
//       });
//     })
//     .catch(err => console.error("Failed to load roles:", err));
// });

// document.addEventListener("DOMContentLoaded", async () => {
//   const roleDropdown = document.getElementById("roleDropdown");

//   try {
//     const response = await fetch("http://127.0.0.1:8000/roles");
//     const roles = await response.json();

//     // Clear and add the default option
//     roleDropdown.innerHTML = `<option value="" disabled selected>Select Role</option>`;

//     roles.forEach(role => {
//       const option = document.createElement("option");
//       option.value = role.id;
//       option.textContent = role.name;
//       roleDropdown.appendChild(option);
//     });
//   } catch (error) {
//     console.error("Error fetching roles:", error);
//     alert("Failed to load roles. Please try again later.");
//   }
// });

ddocument.addEventListener("DOMContentLoaded", async () => {
  const roleDropdown = document.getElementById("roleDropdown");
  const userDropdown = document.getElementById("userDropdown");

  try {
    const response = await fetch("http://127.0.0.1:8000/rolemap");
    const roles = await response.json();

    roleDropdown.innerHTML = `<option value="" disabled selected>Select Role</option>`;
    userDropdown.innerHTML = `<option value="" disabled selected>Select User</option>`;

    roles.forEach(role => {
      const roleOption = document.createElement("option");
      roleOption.value = role.id;
      roleOption.textContent = role.name;

      const userOption = document.createElement("option");
      userOption.value = role.id;
      userOption.textContent = role.name;

      roleDropdown.appendChild(roleOption);
      userDropdown.appendChild(userOption);
    });
  } catch (error) {
    console.error("Error fetching roles:", error);
    alert("Failed to load roles. Please try again later.");
  }
});




