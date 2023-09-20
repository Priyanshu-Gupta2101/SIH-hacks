const slidePage = document.querySelector(".page");
const nextBtnFirst = document.querySelector(".firstNext");
const prevBtnSec = document.querySelector(".prev-1");
const nextBtnSec = document.querySelector(".next-1");
const prevBtnThird = document.querySelector(".prev-2");
const nextBtnThird = document.querySelector(".next-2");
const prevBtnFourth = document.querySelector(".prev-3");
const nextBtnFourth = document.querySelector(".next-3");
const prevBtnFifth = document.querySelector(".prev-4");
const submitBtn = document.querySelector(".submit");
const progressText = document.querySelectorAll(".step p");
const progressCheck = document.querySelectorAll(".step .check");
const bullet = document.querySelectorAll(".step .bullet");
let current = 1;

nextBtnFirst.addEventListener("click", function(event){
  event.preventDefault();
  slidePage.style.marginLeft = "-25%";
  current += 1;
});
nextBtnSec.addEventListener("click", function(event){
  event.preventDefault();
  slidePage.style.marginLeft = "-50%";
  current += 1;
});
nextBtnThird.addEventListener("click", function(event){
  event.preventDefault();
  slidePage.style.marginLeft = "-75%";
  current += 1;
});
nextBtnFourth.addEventListener("click", function(event){
    event.preventDefault();
    slidePage.style.marginLeft = "-100%";
    current += 1;
    }
);
submitBtn.addEventListener("click", function(){
  current += 1;
  setTimeout(function(){
    alert("Your Form Successfully Signed up");
    location.reload();
  },800);
});

prevBtnSec.addEventListener("click", function(event){
  event.preventDefault();
  slidePage.style.marginLeft = "0%";
  current -= 1;
});
prevBtnThird.addEventListener("click", function(event){
  event.preventDefault();
  slidePage.style.marginLeft = "-25%";
  current -= 1;
});
prevBtnFourth.addEventListener("click", function(event){
  event.preventDefault();
  slidePage.style.marginLeft = "-50%";
  current -= 1;
});
prevBtnFifth.addEventListener("click", function(event){
    event.preventDefault();
    slidePage.style.marginLeft = "-75%";
    current -= 1;
    }
);



document.getElementById('personal_detail').addEventListener('click', function (e) {
    e.preventDefault();  // Prevent the form from submitting traditionally

    console.log('form submitted');  // Sanity check
    // Collect form data

    console.log(document.getElementById('dob').value);
    // Send data to Django using fetch
    fetch('/personal_detail/', {
        method: 'PUT',
        body: JSON.stringify({
            'first_name': document.getElementById('first_name').value,
            'last_name': document.getElementById('last_name').value,
            'enrol_no': document.getElementById('enrol_no').value,
            'dob': document.getElementById('dob').value,
        }),
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),  // Include the CSRF token
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(data => {
        // Handle successful response from Django
        console.log(data);
        // You can redirect or display a success message here
    })
    .catch(error => {
        // Handle errors
        console.error('There was a problem with the fetch operation:', error);
    });
});

document.getElementById('contact_detail').addEventListener('click', function (e) {
  e.preventDefault();  // Prevent the form from submitting traditionally

  console.log('form submitted');  // Sanity check
  // Collect form data

  
  // Send data to Django using fetch
  fetch('/contact_detail/', {
      method: 'PUT',
      body: JSON.stringify({
        'email': document.getElementById('email').value,
        'phone_no': document.getElementById('phone_no').value,
        'address': document.getElementById('address').value,
        'city': document.getElementById('city').value,
        'state': document.getElementById('state').value,
        'pincode': document.getElementById('pincode').value,
        'country': document.getElementById('country').value,
      }),
      headers: {
          'X-CSRFToken': getCookie('csrftoken'),  // Include the CSRF token
      },
  })
  .then(response => {
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      return response.text();
  })
  .then(data => {
      // Handle successful response from Django
      console.log(data);
      // You can redirect or display a success message here
  })
  .catch(error => {
      // Handle errors
      console.error('There was a problem with the fetch operation:', error);
  });
});

document.getElementById('guardian_detail').addEventListener('click', function (e) {
  e.preventDefault();  // Prevent the form from submitting traditionally

  console.log('form submitted');  // Sanity check
  // Collect form data

  
  // Send data to Django using fetch
  fetch('/guardian_detail/', {
      method: 'PUT',
      body: JSON.stringify({
          'guardian_name': document.getElementById('guardian_name').value,
          'guardian_no': document.getElementById('guardian_no').value,
          'guardian_email': document.getElementById('guardian_email').value,
          'guardian_gender': document.getElementById('guardian_gender').value,
      }),
      headers: {
          'X-CSRFToken': getCookie('csrftoken'),  // Include the CSRF token
      },
  })
  .then(response => {
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      return response.text();
  })
  .then(data => {
      // Handle successful response from Django
      console.log(data);
      // You can redirect or display a success message here
  })
  .catch(error => {
      // Handle errors
      console.error('There was a problem with the fetch operation:', error);
  });
});


document.getElementById('file_detail').addEventListener('click', function (e) {
    e.preventDefault();  // Prevent the form from submitting traditionally
  
    console.log('form submitted');  // Sanity check
    // Collect form data
    
    let formData = new FormData();
    formData.append('profile_pic', document.getElementById('profile_pic').files[0]);
    formData.append('signature', document.getElementById('signature').files[0]);
    formData.append('aadhar', document.getElementById('aadhar_card').files[0]);
    if (document.getElementById('income_cert').files[0] != undefined) {
        formData.append('income_cert', document.getElementById('income_cert').files[0]);
    }

    
    // Send data to Django using fetch
    fetch('/file_detail/', {
        method: 'PUT',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),  // Include the CSRF token
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(data => {
        // Handle successful response from Django
        console.log(data);
        // You can redirect or display a success message here
    })
    .catch(error => {
        // Handle errors
        console.error('There was a problem with the fetch operation:', error);
    });
  });



// Function to get the CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}