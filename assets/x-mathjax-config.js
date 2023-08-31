// alert('If you see this alert, then your custom JavaScript script has run!');// display message to show that script is running
MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}});
setInterval("MathJax.Hub.Queue(['Typeset',MathJax.Hub])",200); 


// Makes Gross Capital Formation table into bootstrap-table (to use sort table)
function transformGcfTableIntoBootstrapTable() {
    let someComponentClass = $("#table_GFC");


    if (someComponentClass.length > 0 & someComponentClass.is(":visible")) {
        $('#table_GFC').bootstrapTable()
        //clearInterval(refreshID);
    }
}

// call this function every 250 ms
let refreshID = setInterval(transformGcfTableIntoBootstrapTable, 250);