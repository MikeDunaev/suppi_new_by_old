google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(abcGoods_drawChart);
abcGoods_getSort();

function abcGoods_getSort() {
    const table = document.getElementById('abc-goods');
    const indexRevenue = [...document.getElementById('abc-goods_revenue').parentNode.cells].indexOf(document.getElementById('abc-goods_revenue'));
    
    const order = -1;
    const collator = new Intl.Collator(['en', 'ru'], { numeric: true });
    const comparator = (index, order) => (a, b) => order * collator.compare(
        a.children[index].innerText,
        b.children[index].innerText
    );
    
    table.tBodies[0].append(...[...table.tBodies[0].rows].sort(comparator(indexRevenue, order)));

    table.classList.toggle('abc-sorted');
}

function abcGoods_getData() {
    const table = document.getElementById('abc-goods');
    const indexName = [...document.getElementById('abc-goods_name').parentNode.cells].indexOf(document.getElementById('abc-goods_name'));
    const indexRevenue = [...document.getElementById('abc-goods_revenue').parentNode.cells].indexOf(document.getElementById('abc-goods_revenue'));
    
    let data = [];
    for (const tRow of table.tBodies[0].rows) {
        data.push([String(tRow.children[indexName].innerText), Number(tRow.children[indexRevenue].innerText)]);
    }

    return data;
}

function abcGoods_drawChart() {

    const data = google.visualization.arrayToDataTable([['Товар', 'Выручка'], ...abcGoods_getData()]);

    const options = {
        legend: {position: 'labeled'},
        tooltip: {isHtml: true},
        slices: {0: {offset: 0.1}},
        chartArea:{
            left: 0,
            right: 0,
            top: 30,
            bottom: 30,
            width: '100%',
            height: '100%'
        },

    };

    const chart = new google.visualization.PieChart(document.getElementById('abc-goods__piechart'));

    chart.draw(data, options);
}