const apiKey = 'aa908021ff1c4dd4a032f3ecb4942bd3';  // Your API Key
const apiUrl = 'http://127.0.0.1:8000/api/news/'; // Call your Django proxy


// Fetch news data from the API with API key in headers
fetch(apiUrl, {
    method: 'GET',
    headers: {
        'X-Api-Key': apiKey  // Use header for API key
    }
})
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        const articles = data.articles;

        // Shuffle the articles array to randomize the order
        const shuffledArticles = articles.sort(() => 0.5 - Math.random());

        // Select a subset of articles to display (e.g., first 3 random articles)
        const selectedArticles = shuffledArticles.slice(0, 3);

        // Select the container where the news articles will be inserted
        const newsContainer = document.getElementById('news-articles');
        newsContainer.innerHTML = ''; // Clear previous content

        // Check if there are any articles
        if (selectedArticles.length > 0) {
            selectedArticles.forEach(article => {
                // Create a new column for each article
                const articleHtml = `
                    <div class="col-md-4" data-aos="fade-up">
                        <img src="${article.urlToImage || 'images/default_image.jpg'}" alt="blogpost pic" />
                        <div class="mt-4">
                            <small>Posted in <a href="#">${article.source.name}</a> ${new Date(article.publishedAt).toLocaleDateString()}</small>
                            <h5 class="mt-1 mb-2"><a href="${article.url}" target="_blank">${article.title}</a></h5>
                            <p>
                                ${article.description || 'No description available.'}
                            </p>
                        </div>
                    </div>
                `;

                // Append the article HTML to the news container
                newsContainer.insertAdjacentHTML('beforeend', articleHtml);
            });
        } else {
            newsContainer.innerHTML = '<p>No news articles found for the specified query.</p>';
        }
    })
    .catch(error => {
        console.error('Error fetching the news:', error);
    });
