document.addEventListener('DOMContentLoaded', () => {

    const calculateColor = (x) => {
        let r_col = 0;
        let g_col = 0;
        let b_col = 0;

        if (x > 100.0) {
            g_col = 255;
        } else if (x > 50) {
            x = Math.floor(x);
            g_col = 255;
            r_col = (x / 50) * 255;
        } else if (x > 0) {
            x = Math.floor(x);
            r_col = 255;
            g_col = (x / 50) * 255;
        }

        return ('rgba('+ r_col + ',' + g_col + ',' + b_col + ', 0.5)');
    }

    for (const tableTD of document.querySelectorAll('.days-to-null-colored')) {
        tableTD.style.background=calculateColor(tableTD.innerText);
    }
});