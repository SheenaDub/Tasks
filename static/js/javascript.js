
 $(document).ready(function(){
    $('#displayTasks').click(function(){
       displayTasks();
    });
  });


function displayTasks(){
    //window.location.reload(true);


    window.location.reload(true);
    // jquery to retrieve json data

  $.getJSON("http://127.0.0.1:5000/display", function(data) {
    console.log("type of data: ", typeof data);

    console.log("success", data);
    var datasize = Object.keys(data).length;
    console.log("data size", datasize);

    // create array of divs
    var divArray = [];
    for (var i = 0; i < datasize; i++){
        var div = document.createElement('div');
        div.id="div_" + i;
        div.className="taskDiv";
        divArray.push(div)
        document.body.appendChild(div);
        console.log("this div id: ", div.id);
    }

//create edit buttons
    var editButtonArray = [];
    for (var i = 0; i < datasize; i++){

        var edButton = document.createElement("button");
        //edButton.id="edbutton_" + i;
        edButton.className="taskEditButton";
        edButton.type="submit";
        edButton.innerText="Edit Task";
        edButton.disabled = false;
        editButtonArray.push(edButton);
    }

// create delete buttons
    var delButtonArray = [];
    for (var i = 0; i < datasize; i++){
        var delButton = document.createElement("button");
        //delButton.id="delbutton_" + i;
        delButton.className="taskDeleteButton";
        delButton.type="submit";
        delButton.innerText="Delete Task";
        delButtonArray.push(delButton);
    }


    var delFormArray = [];
    for (var i = 0; i < datasize; i++) {
        var f = document.createElement("form");
        f.setAttribute('method', "post");
        f.setAttribute('action',"delete");
        //create a button
        var s = document.createElement("input");
        s.type = "submit";
        s.value = "Submit";
        f.appendChild(s);
    }

// populate each line of with task data
    for (var i = 0; i < datasize; i++){

        var iD = data[i].id;
        var toDoBy = data[i].taskdeadline;
        var name = data[i].taskname;
        var editButton = editButtonArray[i];
        editButton.id="edbutton_" + iD;
        var deleteButton = delButtonArray[i];
        deleteButton.id="delbutton_" + iD;
        var thisDiv = divArray[i];


        var oneLine = "<b>  Task id: </b> "+ iD + " <b>  Task: </b>" + name + " " +  "<b>  Deadline: </b>" + toDoBy;

        thisDiv.innerHTML = oneLine;
        thisDiv.appendChild(editButton);
        thisDiv.appendChild(deleteButton);


    } // end for loop


  })
    // end function data
  .done(function() { console.log( "second success" );
  })
  .fail(function() { console.log( "error" );
  })
  .always(function() { console.log( "complete" );
  });

}// end function display



// to delete task - first accesses id of button clicked
$(document).on('click', "[id^=delbutton_]", function(){

    var buttonId = jQuery(this).attr("id");
    var chars = buttonId.split("_");
    var thisID = parseInt(chars[1]);
    alert(thisID);
    console.log(buttonId);

    //"div_" + i;

    //$('#' + buttonId).remove();

    $.ajax({
  type : 'POST',
  url : "/delete",
  data : {thisID}
});

    //location.reload(true);
window.location.reload(true);
});

// clears all tasks from db
$(document).on('click', "[id=clearTasks]", function(){
    alert("clear all has been called");
    $.ajax({
  type : 'POST',
  url : "/clearAll",
});


window.location.reload(true);
});