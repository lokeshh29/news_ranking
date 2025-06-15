class NewsApp {
    constructor() {
        this.currentCategory = 'general';
        this.currentLimit = 3;
        this.isLoading = false;

        this.initElements();
        this.bindEvents();
        this.loadNews();
    }

    initElements() {
        this.categorySelect = document.getElementById('category');
        this.limitSelect = document.getElementById('limit');
        this.refreshBtn = document.getElementById('refresh-btn');
        this.newsContainer = document.getElementById('news-container');
        this.newsInfo = document.getElementById('news-info');
        this.error = document.getElementById('error-message');
    }

    bindEvents() {
        this.categorySelect.onchange = () => {
            this.currentCategory = this.categorySelect.value;
            this.loadNews();
        };

        this.limitSelect.onchange = () => {
            this.currentLimit = parseInt(this.limitSelect.value);
            this.loadNews();
        };

        this.refreshBtn.onclick = () => this.loadNews();
    }

    async loadNews() {
        if (this.isLoading) return;
        this.isLoading = true;

        this.clearMessages();
        this.newsInfo.textContent = 'Loading news...';
        this.refreshBtn.classList.add('loading');

        try {
            const res = await fetch(`/api/news?category=${this.currentCategory}&limit=${this.currentLimit}`);
            const data = await res.json();

            if (data.articles?.length) {
                this.renderNews(data.articles);
                this.newsInfo.textContent = `Showing ${data.count} ${this.getCategoryName(data.category)} articles`;
            } else {
                this.newsInfo.textContent = 'No news articles found.';
            }
        } catch (err) {
            this.error.style.display = 'block';
            this.error.textContent = 'Failed to load news.';
        } finally {
            this.isLoading = false;
            this.refreshBtn.classList.remove('loading');
        }
    }

    renderNews(articles) {
        this.newsContainer.innerHTML = articles.map(article => {
            return `
                <div class="news-article">
                    ${article.image ? `<img src="${article.image}" class="article-image" onerror="this.style.display='none'">` : ''}
                    <div class="article-content">
                        <h3>${article.title}</h3>
                        <p>${article.description}</p>
                        <p><small>${this.formatDate(article.publishedAt)}</small></p>
                        <a href="${article.url}" target="_blank">Read Full Article</a>
                    </div>
                </div>
            `;
        }).join('');
        this.newsContainer.style.display = 'grid';
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return isNaN(date) ? dateString : date.toLocaleString();
    }

    getCategoryName(category) {
        return {
            general: 'OverAll',
            business: 'Business',
            entertainment: 'Entertainment',
            health: 'Health',
            science: 'Science',
            sports: 'Sports',
            technology: 'Technology'
        }[category] || 'General';
    }

    clearMessages() {
        this.newsContainer.innerHTML = '';
        this.newsInfo.textContent = '';
        this.error.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', () => new NewsApp());
