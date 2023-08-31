// Adds event listener to the dropdown menu in the pyramid inverter page
// When the dropdown menu is clicked, the "invert" button is clicked
// This is done to make the pyramid inverter page more user friendly
// The user can now click the dropdown menu and select the desired option
// without having to click the "invert" button every time. The button is also hiddeng now.

document.addEventListener( "click", someListener );

var lastText = 'DLS level language count'

function someListener(event){
    var element = event.target;
    if(element.tagName == 'DIV' && element.classList.contains("VirtualizedSelectOption") && 
    ((element.textContent == 'DLS level language count') || (element.textContent == 'DLS level population count')) ){
        // console.log("hi");
        if (lastText != element.textContent){

            lastText = element.textContent;
            document.querySelector("#input > g > form > div > label").click()

        }        
    }
}