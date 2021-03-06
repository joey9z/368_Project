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

    var listen1 = document.querySelector("select[name=grad_year]");
    var listen2 = document.querySelector("select[name=start_year]");
    var listen3 = document.querySelector("select[name=start_sem]");
    var listen4 = document.querySelector("select[name=grad_sem]");

    listen1.addEventListener("change", clearForms, false);
    listen2.addEventListener("change", clearForms, false);
    listen3.addEventListener("change", clearForms, false);
    listen4.addEventListener("change", clearForms, false);
    
    submit.addEventListener("click", makeRequest, false);

    submit.addEventListener("click", makeRequest, false);
};

/****************************************************
* populateForms
*
* dynamically populates the form's select elements
*****************************************************/
function clearForms(){
    let semesters = document.querySelector("select[name=semesters]");
    let not_semesters = document.querySelector("select[name=not_semesters]");
    let grad_year = document.querySelector("select[name=grad_year]");
    let start_year = document.querySelector("select[name=start_year]");
    let grad_sem = document.querySelector("select[name=grad_sem]");

    while (semesters.firstChild)
    {
        semesters.removeChild(semesters.firstChild);
    }

    while (not_semesters.firstChild)
    {
        not_semesters.removeChild(not_semesters.firstChild);
    }

    curr_sem = updateForms();
    if(semesters.firstChild.value != null)
    {
        while (semesters.firstChild.value.slice(0,4) < curr_sem)
        {
            semesters.removeChild(semesters.firstChild);
        }

        if(grad_sem.value == "Spring")
        {
            sem = 10;
        }
        else
        {
            sem = 30;
        }

        max_sem = grad_year.value+''+sem;

        while (semesters.lastChild.value > max_sem)
        {
            semesters.removeChild(semesters.lastChild);
        }
        if(not_semesters.lastChild.value != null)
        {
            do
            {
                if(not_semesters.lastChild.value >= max_sem)
                {
                    not_semesters.removeChild(not_semesters.lastChild);
                }
                else
                {
                    break;
                }
            }while(not_semesters.length > 0)

        }
    }

}

function updateForms(){
    let semesters = document.querySelector("select[name=semesters]");
    let not_semesters = document.querySelector("select[name=not_semesters]");
    let grad_year = document.querySelector("select[name=grad_year]");
    let start_year = document.querySelector("select[name=start_year]");

    let year_offset = (grad_year.value - start_year.value);

    let sem_names = ["Spring", "Summer", "Fall"];
    let sems = [10, 20, 30];

    let curr_year = start_year.value;
    let curr_sem = new Date().getFullYear();
    for (let year = curr_sem; year <= grad_year.value; year++)
    {
        // populate semester select elements
        for (let i = 0; i < sems.length; i++)
        {
            let option = document.createElement("option");
            option.value = year+''+sems[i];
            option.text = sem_names[i] + " " + year;
            sems[i]==20 ? not_semesters.appendChild(option) : semesters.appendChild(option);
        }
        
        // populate grad year elements
        let option = document.createElement("option");
        option.value = year;
        option.text = year;
        SelectSort(option);

        //grad_year.appendChild(option);
        
        // populate start year elements
        option = document.createElement("option");
        option.value = year-5;
        option.text = year-5;
        SelectSort(option);

        //start_year.appendChild(option);
    }
    SelectSort(semesters);
    SelectSort(not_semesters);  

    return (curr_sem);
}

function populateForms() {
    let semesters = document.querySelector("select[name=semesters]");
    let not_semesters = document.querySelector("select[name=not_semesters]");
    let grad_year = document.querySelector("select[name=grad_year]");
    let start_year = document.querySelector("select[name=start_year]");
    let courses_taken = document.querySelector("textarea[name=courses_taken]");
    
    const default_start = 2013;
    const default_grad = 2017;
    
    let sem_names = ["Spring", "Summer", "Fall"];
    let sems = [10, 20, 30];
    let courses = ["ECE 20000", "ECE 20100", "ECE 20700"];
    
    let curr_year = new Date().getFullYear();
    
    for (let year = curr_year; year < curr_year + 5; year++)
    {
        // populate semester select elements
        for (let i = 0; i < sems.length; i++)
        {
            let option = document.createElement("option");
            option.value = year+''+sems[i];
            option.text = sem_names[i] + " " + year;
            sems[i]==20 ? not_semesters.appendChild(option) : semesters.appendChild(option);
        }
        
        // populate grad year elements
        let option = document.createElement("option");
        option.value = year;
        option.text = year;
        if (year == default_grad) option.selected=true;
        grad_year.appendChild(option);
        SelectSort(option);
        
        // populate start year elements
        option = document.createElement("option");
        option.value = year-5;
        option.text = year-5;
        if (year-5 == default_start) option.selected=true;
        start_year.appendChild(option);
        SelectSort(option);
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
    let semesters = document.querySelector("select[name=semesters]");
    
    // select all the elements in "semesters on campus" when submitted
    for (let i = 0; i < semesters.length; i++)
    {
        semesters.children[i].selected = true;
    }
    
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
        //makeSemesterTables(data.semesters);     // generate tables to represent the semesters
        makeMatchList(data.course_matches)
    }
    // the request was not successful
    else if (this.readyState == 4 && this.status != 200)
    {
        console.log("Problem!");
    }
}
    
function makeMatchList(matches) {
    let main = document.querySelector("div.content");   // find the main div
    let list = document.createElement("ul");
    
    for (let match of matches)
    {
        let item = document.createElement("li");
        item.innerHTML = "<a href=/api?id="+match+">"+match+"</a>";
        list.appendChild(item);
    }
    main.appendChild(list);
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
            //newOption.selected = true;
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
    SelectSort(dest)
}

function SelectSort(SelList)
{
    var ID='';
    var Text='';
    for (x=0; x < SelList.length - 1; x++)
    {
        for (y=x + 1; y < SelList.length; y++)
        {
            if (SelList[x].value > SelList[y].value)
            {
                // Swap rows
                ID=SelList[x].value;
                Text=SelList[x].text;
                SelList[x].value=SelList[y].value;
                SelList[x].text=SelList[y].text;
                SelList[y].value=ID;
                SelList[y].text=Text;
            }
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
