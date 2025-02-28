const usernameField=document.querySelector('#usernameField');
const feedbackArea=document.querySelector('.invalid-feedback');
const emailField=document.querySelector('#emailField');
const emailfeedbackArea=document.querySelector('.emailFeedbackArea');
const usernamesuccessOutput= document.querySelector('.usernamesuccessOutput');
const showPasswordToggle = document.querySelector('.PasswordToggle');
const passwordField=document.querySelector('#passwordField')
const submitBtn=document.querySelector('.submit-btn')
const handleToggleInput=(e)=>{
    if (showPasswordToggle.textContent ==='SHOW'){
        showPasswordToggle.textContent='HIDE';
        passwordField.setAttribute("type","text");
    }
    else{
        showPasswordToggle.textContent='SHOW';
        passwordField.setAttribute("type","password");
    }
}

showPasswordToggle.addEventListener('click', handleToggleInput);




//email validation field
emailField.addEventListener('keyup', (e)=>{
    const emailVal = e.target.value;
    
    emailField.classList.remove('is-invalid');
    emailfeedbackArea.style.display="none";
    if (emailVal.length > 0) {
        fetch("/authentication/validate-email", {
            method: 'POST',
            
            body: JSON.stringify({email: emailVal}),
        }).then(response => response.json())
        .then(data=>{
            if(data.email_error){
                submitBtn.disabled = true;
                emailField.classList.add('is-invalid');
                emailfeedbackArea.style.display="block";
                emailfeedbackArea.innerHTML=`<p>${data.email_error}</p>`
            }
            else{
                submitBtn.removeAttribute('disabled');
            }
        } );
    }
})

// username validation field
usernameField.addEventListener('keyup', (e) => {
    const usernameVal = e.target.value;
    usernamesuccessOutput.style.display = "block"
   // usernamesuccessOutput.textContent = `Checking ${usernameVal}`;
    usernameField.classList.remove('is-invalid');
    feedbackArea.style.display="none";
    
    if (usernameVal.length>0){
        // Make an AJAX request to the server to validate the username
        fetch("/authentication/validate-username",{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()  // Envoi du token CSRF
            },
            body:JSON.stringify({username:usernameVal}),
    
        })
        .then(response => response.json())
        .then(data=>{
            usernamesuccessOutput.style.display = "none"
            if(data.username_error){
                usernameField.classList.add('is-invalid');
                feedbackArea.style.display="block";
                feedbackArea.innerHTML=`<p>${data.username_error}</p>` 
                submitBtn.disabled = true;               
            }
            else{
                submitBtn.removeAttribute('disabled');
            }
        } );
    }
   
});


/*
    if (usernameVal.length>0){
        // Make an AJAX request to the server to validate the username
        fetch("/authentication/validate-username",{
            
            body:JSON.stringify({username:usernameVal}),
            method: 'POST'
    
        })
        .then(response => response.json())
        .then(data=>{
            console.log(data);
        } );
    }
*/