document.addEventListener('DOMContentLoaded', () => {

    const calculateColor = (x) => {
        let r_col = 0;
        let g_col = 0;
        let b_col = 0;

        if (x.toLowerCase().indexOf("нет продаж") >= 0) {
            r_col = 255;
        } else if (x.toLowerCase().indexOf("кончился") >= 0) {
            r_col = 255;
        } else {
            x = Number(x.substring(0, x.indexOf("-")));
            if (x > 100) {
                g_col = 255;
            } else if (x > 50) {
                g_col = 255;
                r_col = Math.floor((x / 50) * 255);
            } else if (x > 0) {
                r_col = 255;
                g_col = Math.floor((x / 50) * 255);
            } else {
                r_col = 255;
            }
        }

        return ('rgba('+ r_col + ',' + g_col + ',' + b_col + ', 0.5)');
    }

    for (const tableTD of document.querySelectorAll('.days-left-colored')) {
        tableTD.style.background=calculateColor(tableTD.querySelector('.table-view_value').innerHTML);
    }
});