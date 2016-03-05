var request = require("request");

request("https://selfservice.mypurdue.purdue.edu/prod/bwckctlg.p_disp_course_detail?cat_term_in=201510&subj_code_in=PHYS&crse_numb_in=17200", function (e, r, html) {
    var match = /<span class="fieldlabeltext">Prerequisites: <\/span>\s<br>\s(.+)/i.exec(html);
    
    var list = match[1].trim();
    
    console.log("\n", list, "\n");
    
    list = list.replace(/\s<a href="[A-z=;&0-9_./?]+">\s<\/a>/ig, "");  //Case where no text in link
    list = list.replace(/\s<a href="[A-z=;&0-9_./?]+">([A-Z]+\s[A-Z]*[0-9]+)<\/a>/ig, "$1");
    list = list.replace(/Undergraduate level /ig, "");
    list = list.replace(/Minimum Grade of ([ABCDFS](-|\+)*)/g, "{$1}");
    list = list.replace(/([A-Z]+\s[A-Z]*[0-9]+(\s\{[ABCDFS](-|\+)*\})*)\s\[may be taken concurrently\]/g, "[$1]");
    
    console.log("\n", list, "\n");
});