
// "Event Listener" for when a click happens in HHI table to open subtable
$(document).on("click", ".mytable .open", function () {

    // Find the next row (which is a invisible child to the selected root)
    //, and Toggle "display: none" style to make the subtable visible
    const tr = $(this).parents("tr").next();
    tr.toggle();

    // transforms + sign in to -
    const el = $(this);
    el.text() == el.data("text-swap")
        ? el.text(el.data("text-original"))
        : el.text(el.data("text-swap"));

    // calls subtable sort 
    subtable_sort()

});

// Sort subtable 
// NOTE: https://stackoverflow.com/questions/14267781/sorting-html-table-with-javascript#answer-70024272
// NOTE: I had to modify the sorting functions to have the desired behavior ( put nan's at the end of the table and sort
//       for numeric and alphanumeric data. And added code to not add button if it was already called )
function subtable_sort() {

    // set style for 
    const styleSheet = document.createElement('style')
    styleSheet.innerHTML = `
        .order-inactive span {
            visibility:visible;
        }
        .order-inactive:hover span {
            visibility:visible;
        }
        .order-active span {
            visibility: visible;
        }
    `
    document.head.appendChild(styleSheet)

    // select table header for adding the sorting buttons and make the sorting
    document.querySelectorAll('th.order').forEach(th_elem => {
        let asc = true

        // Check if the span button was already created
        let doNotExists = ($(th_elem).find("span").length == 0)

        // If not then creates
        if (doNotExists) {
            const span_elem = document.createElement('span')
            span_elem.style = "font-size:0.8rem; margin-left:0.5rem; cursor: pointer;" // added mouse pointer
            span_elem.innerHTML = "\u25BE"
            th_elem.appendChild(span_elem)
            th_elem.classList.add('order-inactive')
        }

        // Creates and array from the th_element childrens and adds a event listener for when the span is clicked
        const index = Array.from(th_elem.parentNode.children).indexOf(th_elem)
        th_elem.addEventListener('click', (e) => {
            document.querySelectorAll('th.order').forEach(elem => {
                elem.classList.remove('order-active')
                elem.classList.add('order-inactive')
            })
            th_elem.classList.remove('order-inactive')
            th_elem.classList.add('order-active')

            // set triangles given the ascending or descending ordering
            if (!asc) {
                th_elem.querySelector('span').innerHTML = '\u25B4'
            } else {
                th_elem.querySelector('span').innerHTML = '\u25BE'
            }

            // Selects the subtable rows
            const arr = Array.from(th_elem.closest("table").querySelectorAll('tbody .subTableTbody tr'))

            // Checks if header of the clicked span is alpha numeric
            const alphaNumericSorting = th_elem.classList.contains("alphaNumericOrdering")

            arr.sort((a, b) => {
                const a_val = a.children[index].innerText
                const b_val = b.children[index].innerText

                // Checks if is strings sort
                
                if (alphaNumericSorting) {
                    return (asc) ? alphanum(a_val, b_val) : alphanum(b_val, a_val)
                    
                } else {
                    isAnyNan = (a_val === 'nan' || b_val === 'nan') ? -1 : 1 // Put NaN values to the end of the table

                    return (asc) ? numericOnly(b_val, a_val) : numericOnly(a_val, b_val) * isAnyNan
                }
            })
            arr.forEach(elem => {
                th_elem.closest("table").querySelector("tbody").appendChild(elem)
                
            })
            asc = !asc
        })
    })
}


