const button = document.querySelector('#search');
const status = document.querySelector('#status');
const results = document.querySelector('#results');
async function runMarketSearch() {
    status.textContent = 'loading';
    const params = new URLSearchParams({
        region: 'BR',
        sort: 'gmv_desc'
    });
    const response = await fetch(`/api/search?${params}`);
    const data = await response.json();
    results.replaceChildren(...data.items.map((item)=>{
        const li = document.createElement('li');
        li.dataset.productId = item.product_id;
        li.textContent = `${item.name}: ${item.gmv_7d}`;
        return li;
    }));
    status.textContent = `loaded:${data.items.length}:cursor=${data.next_cursor}`;
}
button.addEventListener('click', runMarketSearch);
