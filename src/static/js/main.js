// JavaScript for Submit Form GUI

console.log("Hello, world!");

function initialize() {
    let submit = document.querySelector("input[name=submit]");
    populateForms();
    
    submit.addEventListener("click", makeRequest, false);
};

function populateForms() {
    let semesters = document.querySelector("select[name=semesters]");
    let grad_year = document.querySelector("select[name=grad_year]");
    let start_year = document.querySelector("select[name=start_year]");
    let courses_taken = document.querySelector("textarea[name=courses_taken]");
    
    let sem_names = ["Fall", "Spring", "Summer"];
    let courses = ["ECE 20000", "ECE 20100", "ECE 20700"];
    
    let curr_year = new Date().getFullYear();
    
    for (let year = curr_year; year < curr_year + 5; year++)
    {
        for (let sem of sem_names)
        {
            let option = document.createElement("option");
            option.value = sem + " " + year;
            option.text = sem + " " + year;
            (sem=="Fall" || sem=="Spring") && (option.selected = "true");
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

function makeRequest(e) {
    e.preventDefault();
    let form = document.querySelector("form");
    form.parentNode.removeChild(form);
    let formData = new FormData(form);
    
    console.log("#### Form Data ####\n");
    for (let entry of formData) {
        console.log(entry);
    }
    
    let xhr = new XMLHttpRequest();
    xhr.open('POST', "/submit", true);
    xhr.send(formData);

    xhr.addEventListener("readystatechange", processData, false);
}
    
function processData() {
    
    if (this.readyState == 4 && this.status == 200)
    {
        console.log("We have data");
        
        let data = JSON.parse(this.responseText);
        makeSemesterTables(data.semesters);
    }
    else if (this.readyState == 4 && this.status != 200)
    {
        console.log("Problemo!");
    }
    
}

function makeSemesterTables(semesters) {
    let main = document.querySelector("div.content");
    
    for (let semester of semesters) {
        let table = document.createElement("table");
        let row = document.createElement("tr");
        let header = document.createElement("th");
        let title = document.createTextNode(semester.semester + " " + semester.year);
        table.setAttribute("class", "table table-bordered");
        
        header.appendChild(title);
        row.appendChild(header);
        table.appendChild(row);
        main.appendChild(table);
        
        for (let course of semester.courses) {
            let row = document.createElement("tr");
            let col = document.createElement("td");
            row.appendChild(col);
            col.textContent = course;
            table.appendChild(row);
        }
    }
}

document.addEventListener("DOMContentLoaded", initialize);  // run the initialize function when the DOM is ready