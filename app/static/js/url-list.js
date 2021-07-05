window.addEventListener('load', () => {
    let storage = window.sessionStorage;
    let logoutButton = document.getElementById('logout');
    let itemList = document.getElementById('item-list');
    let pageNumber = document.getElementById('page');
    let prevPage = document.getElementById('prev-page');
    let nextPage = document.getElementById('next-page');

    
    var logout = _ => {
        storage.clear();
        window.location.replace('/');
    };
    var verifyToken = _ => {
        let jwt = storage.getItem('jwt');
        if (!jwt) {
            logout();
        }
    };
    verifyToken();

    var renderList = json => {
        itemList.innerHTML = '';
        json.items.forEach(url => {
            let a = document.createElement('a');
            a.href = url.shorted_key;
            a.target = '_blank';
            a.appendChild(document.createTextNode(url.shorted_key))
            let li = document.createElement('li');
            let liText = document.createTextNode(` ← ${url.original_url}`);
            li.appendChild(a);
            li.appendChild(liText);
            itemList.appendChild(li);
        });

        pageNumber.innerHTML = `${json.page} of ${json.pages}`;
        if (json.has_prev) {
            prevPage.disabled = false;
            prevPage.onclick = () => loadUrls(json.page - 1);
        } else {
            prevPage.disabled = true;
        }

        if (json.has_next) {
            nextPage.disabled = false;
            nextPage.onclick = () => loadUrls(json.page + 1);
        } else {
            nextPage.disabled = true;
        }

    };
    
    var loadUrls = page => {
        fetch(`/short-urls?page=${page}`, {
            method: 'GET',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('jwt')}`
            }
        }).then(response => {
            if (response.status == 200){
                return response.json();
            } else {
                console.error('Error:', response.json());
            }
        }).then(json => {
            renderList(json);
        }).catch(error => {
            console.error('Error:', error);
        });
    };

    logoutButton.addEventListener('click', (event) => {
        event.preventDefault();
        logout();
    });
    loadUrls(1);
});
