google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(abcIntoWarehouse_drawChart);

function abcIntoWarehouse_drawChart() {

    const chartsWrapper = document.getElementById('abc-into-warehouse__charts');
    const AllWarehouses = abcIntoWarehouse_getData();
    let iter = 0;
    for (const wHouse in AllWarehouses) {
        iter++;
        const data = google.visualization.arrayToDataTable([['Товар', 'Выручка'], ...AllWarehouses[wHouse]]);
        const options = {
            title: wHouse,
            legend: {position: 'none'},
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
        const div_chart = document.createElement("DIV");
        div_chart.id = 'abc-into-warehouse__piechart-' + iter;
        div_chart.style.width = '300px';
        div_chart.style.height = '300px';
        chartsWrapper.appendChild(div_chart);

        const chart = new google.visualization.PieChart(document.getElementById('abc-into-warehouse__piechart-' + iter));
        chart.draw(data, options);
    }
}

function abcIntoWarehouse_getData() {
    const table = document.getElementById('abc-into-warehouse');
    const indexWarehouse = [...document.getElementById('abc-into-warehouse_warehouse').parentNode.cells].indexOf(document.getElementById('abc-into-warehouse_warehouse'));
    const indexName = [...document.getElementById('abc-into-warehouse_name').parentNode.cells].indexOf(document.getElementById('abc-into-warehouse_name'));
    const indexRevenue = [...document.getElementById('abc-into-warehouse_revenue').parentNode.cells].indexOf(document.getElementById('abc-into-warehouse_revenue'));
    
    let data = {};
    for (const tRow of table.tBodies[0].rows) {
        // .warehouse-headline-row - класс строки-заголовка склада
        if (!tRow.classList.contains('warehouse-headline-row')) {
            let city = String(tRow.children[indexWarehouse].innerText);
            if (data[city]) {
                data[city].push([String(tRow.children[indexName].innerText), Number(tRow.children[indexRevenue].innerText)]);
            } else {
                data[city] = [];
                data[city].push([String(tRow.children[indexName].innerText), Number(tRow.children[indexRevenue].innerText)]);
            }
        }
    }

    return data;
}