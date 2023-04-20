document.getElementById('login-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const loginform = $('#login-form');

    $.ajax({
        type: "POST",
        url: "/verify-login",
        data: loginform.serialize(),
        success: function (result) {
            if(result["status"] == false) {
                document.getElementById('incorrect-credentials').style.display = "block";
            } else {
                localStorage.setItem('user-email', result['email']);
                localStorage.setItem('user-name', result['name']);
                window.location.href = '/';
            }
        }
    })
})

function checkLoggedIn() {
    if(localStorage.getItem('user-email') === null) {
        windows.location.href = '/';
    }
}

function fetchRecommendedMovies() {
    let email = localStorage.getItem('user-email');
    $.ajax({
        type: "POST",
        url: '/fetch-recommendations',
        data: email,
        success: function (result) {
            console.log(result)
            let fill = ``;
            for (let i in result) {
                fill += `<div class="recommendation-tile">
                <img src="${result[i]['path']}" alt="no image">
                <h3>${result[i]['title']}</h3>
            </div>`;
            }
            // document.getElementById('simple-spinner').style.display = 'none';
            document.getElementById('recommendations-div').innerHTML = fill;
        }
    })
}

function fetchwatchlist() {
    let email = localStorage.getItem('user-email');
    $.ajax({
        type: "POST",
        url: '/fetchwatchlist',
        data: email,
        success: function (result) {
            console.log(result);
            let fill = ``;
            for (let i in result) {
                fill += `<div class="recommendation-tile">
                <img src="${result[i]['path']}" alt="no image">
                <h3>${result[i]['title']}</h3>
            </div>`;
            }
            // document.getElementById('simple-spinner').style.display = 'none';
            document.getElementById('recommendations-div').innerHTML = fill;
        }
    })
}