document.addEventListener('DOMContentLoaded', () => {

    const thCity = document.getElementById('abc-into-warehouse_warehouse');
    const thCash = document.getElementById('abc-into-warehouse_revenue');
    const indexCity = [...thCity.parentNode.cells].indexOf(thCity);
    const indexCash = [...thCash.parentNode.cells].indexOf(thCash);

    const order = -1;
    const collator = new Intl.Collator(['en', 'ru'], { numeric: true });
    const comparator = (index, order) => (a, b) => order * collator.compare(
        a.children[index].innerText,
        b.children[index].innerText
    );

    let newBody = {}
    let headLines = [];
    for (const tRow of thCity.closest('table').tBodies[0].rows) {
        if (tRow.children[indexCity].innerText.trim() in newBody) {
            newBody[tRow.children[indexCity].innerText.trim()].push(tRow);
            let whClass = tRow.children[indexCity].classList.item(0);
            tRow.children[indexCity].classList.remove(whClass);
        } else {
        newBody[tRow.children[indexCity].innerText.trim()] = [];

        // Строка - заголовок склада
        // Создаем строку таблицы и добавляем ее
        let amount_row = document.createElement("TR");
        newBody[tRow.children[indexCity].innerText.trim()].push(amount_row);
        amount_row.classList.add('warehouse-headline-row');
        // Создаем ячейки 
        for (let td_sep, i=0; i<8; i++) {
            td_sep = document.createElement("TD");
            amount_row.appendChild(td_sep);
        }
        // Наполняем ячейки
        amount_row.children[indexCity].innerText = tRow.children[indexCity].innerText.trim();
        let whClass = tRow.children[indexCity].classList.item(0);
        amount_row.children[7].classList.add(whClass);
        tRow.children[indexCity].classList.remove(whClass);

        newBody[tRow.children[indexCity].innerText.trim()].push(tRow);
        }
    }

    // Заполнение значений и классов у блоков городов
    for (let currCity of Object.keys(newBody)) {
        let amountProceed = 0;
        for (let currProceed of newBody[currCity]) {
            amountProceed += Number(currProceed.children[indexCash].innerText);
        }
        newBody[currCity][0].children[indexCash].innerText = amountProceed;
        newBody[currCity][0].children[indexCity].style.paddingLeft = "10px";
        newBody[currCity][0].children[indexCash].style.paddingLeft = "10px";

        // Выделение границы после последнего товара у склада
        newBody[currCity][newBody[currCity].length - 1].classList.add('warehouse-last-row');

        headLines.push(newBody[currCity][0]);
        // Сортировка внутри склада
        newBody[currCity].sort(comparator(indexCash, order));

        newBody[currCity][0].children[7].setAttribute("rowspan", newBody[currCity].length);
    }

    // Сортировка складов
    headLines.sort(comparator(indexCash, order));
    for (let currCity of headLines) {
        thCity.closest('table').tBodies[0].append(...newBody[currCity.children[indexCity].innerText]);
    }

});