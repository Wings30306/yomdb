const movies = JSON.parse(document.getElementById('all-movies').textContent);

const searchbox = document.getElementById('search')
const genreDropdown = document.getElementById('genre')
const actorDropdown = document.getElementById('cast')

const selectionDiv = document.getElementById('selected-movies')

function getSelectedMovies() {
    const selectedMovies = movies
        .filter(movie => movie["genre"].toLowerCase().includes(genreDropdown.value.toLowerCase()))
        .filter(movie => movie["cast"].toLowerCase().includes(actorDropdown.value.toLowerCase()))
        .filter(movie => movie["title"].toLowerCase().includes(searchbox.value.toLowerCase()))
        .map(movie => `<div class="col-12 col-sm-6 col-lg-4">
        <h3><a href="/watchlist/${movie["pk"]}">${movie["title"]}</a></h3>
        <p>Cast: ${movie["cast"]}</p>
        <p>Genre: ${movie["genre"]}</p>
        ${movie.watched ? "<p>You've watched this movie</p>" : ""}
        </div>`)
        .join("")
    selectionDiv.innerHTML = selectedMovies
}

genreDropdown.addEventListener("change", getSelectedMovies)
actorDropdown.addEventListener("change", getSelectedMovies)
searchbox.addEventListener("change", getSelectedMovies)
searchbox.addEventListener("keyup", getSelectedMovies)
