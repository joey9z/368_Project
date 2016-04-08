// JavaScript for Submit Form GUI

console.log("Hello, world!");

function initialize() {
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
};

document.addEventListener("DOMContentLoaded", initialize);