window.addEventListener('load', () => {
    let storage = window.sessionStorage;
    function logout(){
        storage.clear();
        window.location.replace('/');
    }

    let access_token = storage.getItem('access_token');
    if (!access_token) {
        logout();
    }

});
