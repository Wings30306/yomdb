console.log("Script loaded")

const csrftoken = document.cookie.split("=")[1]
console.log(csrftoken)

const resultDiv = document.querySelector('#show-results')
const searchInput = document.querySelector('#search');
searchInput.addEventListener('change', displayMatches);
searchInput.addEventListener('keyup', displayMatches);

function displayMatches() {
    resultDiv.innerHTML = ""
    const API = "https://www.omdbapi.com/?type=movie&apikey=da298606&s="
    fetch(API + this.value)
        .then(searchResult => searchResult.json())
        .then(movies => movies.Search
            .map(movie => makeHtmlString(movie.imdbID)))
}


function makeHtmlString(data) {
    fetch(`https://www.omdbapi.com/?i=${data}&apikey=da298606`)
        .then(result => result.json())
        .then(result => `<h3>${result.Title}</h3>
            <p>ID: ${result.imdbID}</p>
            <p>Cast: ${result.Actors}</p>
            <p>Genre: ${result.Genre}</p>
            <form method="POST">
            <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">
            <input type="hidden" name="title" value="${result.Title}">
            <input type="hidden" name="cast" value="${result.Actors}">
            <input type="hidden" name="genre" value="${result.Genre}">
            <input type="hidden" name="id" value="${result.imdbID}">
            <input type="submit" value="Add movie">
            </form>`)
        .then(htmlString => resultDiv.innerHTML += htmlString)
}