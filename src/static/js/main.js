// JavaScript for Submit Form GUI

console.log("Hello, world!");


/***********************************
* initialize
*
* executes when the DOM is loaded
* sets up event listeners
************************************/

function initialize() {
    let submit = document.querySelector("input[name=submit]");
    populateForms();
    
    submit.addEventListener("click", makeRequest, false);
};

/****************************************************
* populateForms
*
* dynamically populates the form's select elements
*****************************************************/

function populateForms() {
    let semesters = document.querySelector("select[name=semesters]");
    let grad_year = document.querySelector("select[name=grad_year]");
    let start_year = document.querySelector("select[name=start_year]");
    let courses_taken = document.querySelector("textarea[name=courses_taken]");
    
    let sem_names = ["Fall", "Spring", "Summer"];
    let sems = [10, 20, 30];
    let courses = ["ECE 20000", "ECE 20100", "ECE 20700"];
    
    let curr_year = new Date().getFullYear();
    
    for (let year = curr_year; year < curr_year + 5; year++)
    {
        for (let i = 0; i < sems.length; i++)
        {
            let option = document.createElement("option");
            option.value = year+''+sems[i];
            option.text = sem_names[i] + " " + year;
            (sems[i]==30) && (option.selected = "true");
            semesters.appendChild(option);
        }
        
        let option = document.createElement("option");
        option.value = year;
        option.text = year;
        grad_year.appendChild(option);
        
        option = document.createElement("option");
        option.value = year-5;
        option.text = year-5;
        grad_year.appendChild(option);
        start_year.appendChild(option);
    }
    
    for (let course of courses)
    {
        let node = document.createTextNode(course+"\n");
        courses_taken.appendChild(node);  
    }    
}

/****************************************
* makeRequest
*
* submits a web request to /submit
*****************************************/

function makeRequest(e) {
    e.preventDefault();     // prevent form from submitting itself
    let form = document.querySelector("form");      // find the form element
    form.parentNode.removeChild(form);              // remove the form element
    let formData = new FormData(form);              // encode the form's data
    
    // print the form data to the console
    
    console.log("#### Form Data ####\n");
    for (let entry of formData) {
        console.log(entry);
    }
    
    // make the web request to /submit with the form data
    
    let xhr = new XMLHttpRequest();
    xhr.open('POST', "/submit", true);
    xhr.send(formData);
    
    // listen for the response to the web request

    xhr.addEventListener("readystatechange", processData, false);
}

/****************************************
* processData
*
* checks status of web request
* acts upon received data
*****************************************/
    
function processData() {
    
    // the request was successful
    if (this.readyState == 4 && this.status == 200)
    {
        console.log("We have data");
        
        let data = JSON.parse(this.responseText);   // convert the data to JavaScript Notation
        console.log(data);
        makeSemesterTables(data.semesters);     // generate tables to represent the semesters
    }
    // the request was not successful
    else if (this.readyState == 4 && this.status != 200)
    {
        console.log("Problem!");
    }
}

/****************************************
* makeSemesterTables
*
* checks status of web request
*****************************************/

function makeSemesterTables(semesters) {
    let main = document.querySelector("div.content");   // find the main div
    
    for (let semester of semesters) {
        // create a table element for each semester
        
        let table = document.createElement("table");
        let row = document.createElement("tr");
        let header = document.createElement("th");
        let title = document.createTextNode(semester.semester + " " + semester.year);
        table.setAttribute("class", "table table-bordered");
        
        header.appendChild(title);
        row.appendChild(header);
        table.appendChild(row);
        main.appendChild(table);
        
        // create a row in the semester's table for each course
        
        for (let course of semester.courses) {
            let row = document.createElement("tr");
            let col = document.createElement("td");
            row.appendChild(col);
            col.textContent = course;
            table.appendChild(row);
        }
    }
}

function listbox_move(listID, direction) {
    var listbox = document.getElementById(listID);
    var selIndex = listbox.selectedIndex;
    if (-1 == selIndex) {
        alert("Please select an option to move.");
        return;
    }
    var increment = -1;
    if (direction == 'up')
        increment = -1;
    else
        increment = 1; if ((selIndex + increment) < 0 || (selIndex + increment) > (listbox.options.length - 1)) {
        return;
    }
    var selValue = listbox.options[selIndex].value;
    var selText = listbox.options[selIndex].text;
    listbox.options[selIndex].value = listbox.options[selIndex + increment].value
    listbox.options[selIndex].text = listbox.options[selIndex + increment].text
    listbox.options[selIndex + increment].value = selValue;
    listbox.options[selIndex + increment].text = selText;
    listbox.selectedIndex = selIndex + increment;
    }

    function listbox_moveacross(sourceID, destID) {
    var src = document.getElementById(sourceID);
    var dest = document.getElementById(destID);
    for (var count = 0; count < src.options.length; count++) {
        if (src.options[count].selected == true) {
            var option = src.options[count];
            var newOption = document.createElement("option");
            newOption.value = option.value;
            newOption.text = option.text;
            newOption.selected = true;
            try {
                dest.add(newOption, null);
                src.remove(count, null);
            } catch (error) {
                dest.add(newOption);
                src.remove(count);
            }
            count--;
        }
    }
    }

    function listbox_selectall(listID, isSelect) {
    var listbox = document.getElementById(listID);
    for (var count = 0; count < listbox.options.length; count++) {
        listbox.options[count].selected = isSelect;
    }
    }                


// run the initialize function when the DOM is ready

document.addEventListener("DOMContentLoaded", initialize);