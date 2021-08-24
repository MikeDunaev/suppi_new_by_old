document.addEventListener('DOMContentLoaded', () => {

    const table = document.querySelector("#speed-good");
    let maxValue;
    let rot = -90;
  	let val;
    
    maxValue = 0.0;
    for (const currentRow of table.tBodies[0].rows) {
        val = Number((currentRow.children[3].innerText).replace(',','.'));
        if (maxValue < val) {
            maxValue = val;
        }
    }
    for (const currentRow of table.tBodies[0].rows) {
        val = Number((currentRow.children[3].innerText).replace(',','.'));
        rot = -90.0 + (val / maxValue * 180.0);  
        currentRow.children[3].querySelector(".needle").style.transform = "rotate(" + rot + "deg";
    }

    maxValue = 0.0;
    for (const currentRow of table.tBodies[0].rows) {
        val = Number((currentRow.children[4].innerText).replace(',','.'));
        if (maxValue < val) {
            maxValue = val;
        }
    }
    for (const currentRow of table.tBodies[0].rows) {
        val = Number((currentRow.children[4].innerText).replace(',','.'));
        rot = -90.0 + (val / maxValue * 180.0);  
        currentRow.children[4].querySelector(".needle").style.transform = "rotate(" + rot + "deg";
    }
});
  