function myFunction() {
    console.log("hello world");
  }

  //fixme to include event delegatio



function postData(){


    let virtual = document.getElementById('check_virtual')
    let lgbtq = document.getElementById('check_LGBTQ')
    

    fetch( '/projectApp/list',{
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            //'X-CSRFToken': getCSRFToken() //fixme DNE currently
        },
        body: JSON.stringify({
            // virtual: virtual.checked,
             lgbtq: lgbtq.checked
        })

    }
    )
    .then(response => response.text())  // Not `.json()` because it's HTML shoudl witch to json likely 
        .then(html => {
            document.getElementById("cards").innerHTML = html;
            const virtual = document.getElementById("apply");
            virtual.addEventListener("click", postData);
        })
        .catch(error => console.error('Error:', error));
    }

    // .then(response => response.json()) //this is becuase .json is an async function
    // .then(filterJson => {
    //     console.log("Success", filterJson)

    // })
    // .catch ((error =>
    //     console.error("Error:", error)
    // ));


//onInit

const checkbox = document.getElementById('check_virtual');

checkbox.addEventListener('change', function() {
    if (this.checked) {
    console.log('Checkbox is checked');
    // Perform actions when checked
    } else {
    console.log('Checkbox is unchecked');
    // Perform actions when unchecked
    }
});
const virtual = document.getElementById("apply")
virtual.addEventListener("click", postData);