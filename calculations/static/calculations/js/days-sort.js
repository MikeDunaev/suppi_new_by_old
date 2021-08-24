document.addEventListener('DOMContentLoaded', () => {

    const getSort = (target) => {
        const order = 1;
        const index = [...target.parentNode.cells].indexOf(target);
        const collator = new Intl.Collator(['en', 'ru'], { numeric: true });
        const comparator = (index, order) => (a, b) => order * collator.compare(
            a.children[index].innerText,
            b.children[index].innerText
        );
        
        let ended = [];
        let toEnd = [];
        let noSalesEnded = [];
        let noSales = [];
        for (const currentRow of target.closest('table').tBodies[0].rows) {
            if (currentRow.children[index].innerText.toLowerCase().indexOf("закончился") >= 0) {
                if (currentRow.children[index].innerText.toLowerCase().indexOf("нет продаж") >= 0) {
                    noSalesEnded.push(currentRow);
                } else {
                    ended.push(currentRow);
                }
            } else if (currentRow.children[index].innerText.toLowerCase().indexOf("нет продаж") >= 0) {
                noSales.push(currentRow);
            } else {
                toEnd.push(currentRow);
            }
        }
        target.closest('table').tBodies[0].append(...ended);
        target.closest('table').tBodies[0].append(...toEnd.sort(comparator(index, order)));
        target.closest('table').tBodies[0].append(...noSalesEnded);
        target.closest('table').tBodies[0].append(...noSales);

        target.classList.toggle('day-sorted');
    }
    
    for (const tableTH of document.querySelectorAll('.days-sort')) {
        getSort(tableTH);
    }
});