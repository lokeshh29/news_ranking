class NewsApp {
    constructor() {
        this.currentCategory = 'general';
        this.currentLimit = 3;
        this.isLoading = false;

        this.initElements();
        this.bindEvents();
        this.loadNews();
        // Autorefresh 
        setInterval(() => !this.isLoading && this.loadNews(false, true), 300000);
    }

    initElements() {
        const get = id => document.getElementById(id);
        this.categorySelect = get('category');
        this.limitSelect = get('limit');
        this.refreshBtn = get('refresh-btn');
        this.newsContainer = get('news-container');
        this.error = get('error-message');
        this.newsInfo = get('news-info');
    }

    bindEvents() {
        this.categorySelect.onchange = () => {
            this.currentCategory = this.categorySelect.value;
            this.loadNews();
        };
        this.limitSelect.onchange = () => {
            this.currentLimit = +this.limitSelect.value;
            this.loadNews();
        };
        this.refreshBtn.onclick = () => this.loadNews(true);
    }

    async loadNews(force = false, auto = false) {
        if (this.isLoading && !force) return;
        this.isLoading = true;

        this.showLoadingMessage(auto);

        try {
            const res = await fetch(`/api/news?category=${this.currentCategory}&limit=${this.currentLimit}`);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);

            const data = await res.json();

            if (data.articles?.length) {
                this.render(data);
            } else {
                this.showNoNews();
            }
        } catch (e) {
            console.error(e);
            this.showError(e.message);
        } finally {
            this.isLoading = false;
            this.refreshBtn.classList.remove('loading');
        }
    }

    render({ articles, category, count }) {
        this.clearMessages();
        this.newsInfo.textContent = `Showing ${count} ${this.getCategoryName(category)} articles`;

        this.newsContainer.innerHTML = articles.map(this.articleHTML.bind(this)).join('');
        this.newsContainer.style.display = 'grid';
    }

    articleHTML(article) {
        const escape = text => {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        };

        return `
        <div class="news-article">
            ${article.image ? `<img src="${article.image}" class="article-image" onerror="this.style.display='none'">` : ''}
            <div class="article-content">
                <h3 class="article-title">${escape(article.title)}</h3>
                <p class="article-description">${escape(article.description || '')}</p>
                ${article.enhanced_summary ? `<p><strong>AI Summary:</strong> ${escape(article.enhanced_summary)}</p>` : ''}
                ${article.key_topics?.map(topic => `<span class="topic-tag">${escape(topic)}</span>`).join('') || ''}
                <div class="article-meta">
                    ${article.source?.name ? `<span class="article-source">${escape(article.source.name)}</span>` : ''}
                    ${article.publishedAt ? `<span class="article-date">${this.formatDate(article.publishedAt)}</span>` : ''}
                </div>
                ${article.url ? `<a href="${article.url}" target="_blank" class="read-more-btn">Read Full Article</a>` : ''}
            </div>
        </div>`;
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return isNaN(date.getTime()) ? dateString : date.toLocaleString();
    }

    getCategoryName(category) {
        return {
            general: 'Trending',
            business: 'Business',
            entertainment: 'Entertainment',
            health: 'Health',
            science: 'Science',
            sports: 'Sports',
            technology: 'Technology'
        }[category] || category;
    }

    showError(message) {
        this.clearMessages();
        if (this.error) {
            this.error.style.display = 'block';
            const paragraph = this.error.querySelector('p');
            if (paragraph) paragraph.textContent = `Error: ${message}`;
        }
    }

    showNoNews() {
        this.clearMessages();
        this.newsInfo.textContent = 'No news articles found.';
    }

    showLoadingMessage(auto) {
        this.clearMessages();
        this.newsInfo.textContent = auto ? 'Auto-refreshing news…' : 'Loading news…';
        this.refreshBtn.classList.add('loading');
    }

    clearMessages() {
        if (this.error) this.error.style.display = 'none';
        if (this.newsContainer) {
            this.newsContainer.style.display = 'none';
            this.newsContainer.innerHTML = '';
        }
        if (this.newsInfo) this.newsInfo.textContent = '';
    }
}

document.addEventListener('DOMContentLoaded', () => new NewsApp());
