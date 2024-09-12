window.onload= function(){
    if(localStorage)
    {
        populate();
        const form=document.getElementById('registrationForm');
        form.addEventListener('submit',store);
    }
    else{
        window.alert('localstorage is not supported');
    }
    }
    function store() {
        let firstname = document.forms.personalinfo.firstname.value;
        let lastname = document.forms.personalinfo.lastname.value;
        let dob = document.forms.personalinfo.dob.value;
        let sex = document.forms.personalinfo.sex.value;
        let email = document.forms.personalinfo.email.value;
        let password = document.forms.personalinfo.password.value;
        let confirmPassword = document.forms.personalinfo.confirmPassword.value;
        localStorage.setItem('firstname', firstname);
        localStorage.setItem('lastname', lastname);
        localStorage.setItem('dob', dob);
        localStorage.setItem('sex', sex);
        localStorage.setItem('email', email);
        localStorage.setItem('password', password);
        localStorage.setItem('confirmPassword', confirmPassword);
    
    }
    
    function populate() {
        let firstname = document.forms.personalinfo.firstname;
        let lastname = document.forms.personalinfo.lastname;
        let dob = document.forms.personalinfo.dob;
        let sex = document.forms.personalinfo.sex;
        let email = document.forms.personalinfo.email;
        let password = document.forms.personalinfo.password;
        let confirmPassword = document.forms.personalinfo.confirmPassword;
    
        if (localStorage.getItem('firstname') != null) {
            firstname.value = localStorage.getItem('firstname');
        }
    
        if (localStorage.getItem('lastname') != null) {
            lastname.value = localStorage.getItem('lastname');
        }
    
        if (localStorage.getItem('dob') != null) {
            dob.value = localStorage.getItem('dob');
        }
    
        if (localStorage.getItem('sex') != null) {
            sex.value = localStorage.getItem('sex');
        }
    
        if (localStorage.getItem('email') != null) {
            email.value = localStorage.getItem('email');
        }
    
        if (localStorage.getItem('password') != null) {
            password.value = localStorage.getItem('password');
        }
    
        if (localStorage.getItem('confirmPassword') != null) {
            confirmPassword.value = localStorage.getItem('confirmPassword');
        }
    }
    
    function validatepersonalinfo() {
        let firstname = document.forms.personalinfo.firstname.value;
        let lastname = document.forms.personalinfo.lastname.value;
        let dob = document.forms.personalinfo.dob.value;
        let sex = document.forms.personalinfo.sex.value;
        let email = document.forms.personalinfo.email.value;
        let password = document.forms.personalinfo.password.value;
        let confirmPassword = document.forms.personalinfo.confirmPassword.value;
    
        if (!firstname) {
            document.getElementById('firstnameErr').innerHTML = "First name is required";
            document.forms.personalinfo.firstname.focus();
            return false;
        }
    
        if (!lastname) {
            document.getElementById('lastnameErr').innerHTML = "Last name is required";
            document.forms.personalinfo.lastname.focus();
            return false;
        }
    
        if (!dob) {
            document.getElementById('dobErr').innerHTML = "Date of Birth is required";
            document.forms.personalinfo.dob.focus();
            return false;
        }
        if (!lastname) {
            document.getElementById('lastnameErr').innerHTML = "Last name is required";
            document.forms.personalinfo.lastname.focus();
            return false;
        }
        if (!sex) {
            document.getElementById('sexErr').innerHTML = "Sex is required";
            document.forms.personalinfo.sex.focus();
            return false;
        }
        if (!email) {
            document.getElementById('emailErr').innerHTML = "email is required";
            document.forms.personalinfo.email.focus();
            return false;
        }
        if (!password) {
            document.getElementById('passwordErr').innerHTML = "Password is required";
            document.forms.personalinfo.password.focus();
            return false;
        }
        return true;
    }
    function validatePasswords() {
        let password = document.forms.personalinfo.password.value;
        let confirmPassword = document.forms.personalinfo.confirmPassword.value;
    
        if (password !== confirmPassword) {
            document.getElementById('confirmPasswordErr').innerHTML = "Passwords do not match";
            document.forms.personalinfo.confirmPassword.focus();
            return false;
        } else {
            document.getElementById('confirmPasswordErr').innerHTML = "";
            return true;
        }
    }
    function validatefn() {
        let namepattern = /^[A-Za-z\s]*$/;
        let firstname = document.forms.personalinfo.firstname.value;
    
        if (firstname) {
            let x = namepattern.test(firstname);
            if (x === false) {
                document.getElementById('firstnameErr').innerHTML = "<br/>First name can only contain letters and white spaces";
                document.forms.personalinfo.firstname.focus();
                return false;
            } else {
                document.getElementById('firstnameErr').innerHTML = "";
                document.forms.personalinfo.firstname.style.borderColor = 'teal';
                return true;
            }
        }
        return false;
    }
    
    