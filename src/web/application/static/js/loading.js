var i = 0;

//Creation of the bar that will move as a loading bar.
function move() {
    if (i == 0) {
        i = 1;
        var bar = document.getElementById("barProgress");
        var width = 1;
        /*
        SetInterval is a js function that will call a function repeateadly.
        And this with an amount of time fixed between the different calls.
        Here, the function will be called to make the progress bar advance.
        */
        var id = setInterval(border, 100);
        function border() {
            if (width >= 100) {
                /*
                This will stop the process because width is covered.
                */
                clearInterval(id);
                i = 0;
            }
            else {
                width++;
                bar.style.width = width + "%";
            }
        }
    }
}