
 $(document).ready(function(){
    $('#displayTasks').click(function(){
       displayTasks();
    });
  });


function displayTasks(){
  // jquery to retrieve json data
  $.getJSON("http://127.0.0.1:5000/display", function(data) {
    console.log("type of data: ", typeof data);

    console.log("success", data);
    var datasize = Object.keys(data).length;
    console.log("data size", datasize);

    var divArray = [];
    for (var i = 0; i < datasize; i++){
        var div = document.createElement('div');
        div.id="div_" + i;
        div.className="taskDiv";
        divArray.push(div)
        document.body.appendChild(div);
    }


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


    for (var i = 0; i < datasize; i++){


        var iD = data[i].id;
        var toDoBy = data[i].taskdeadline;
        var name = data[i].taskname;
        var editButton = editButtonArray[i];
        editButton.id="edbutton_" + iD;
        var deleteButton = delButtonArray[i];
        deleteButton.id="delbutton_" + iD;
        var thisDiv = divArray[i];
        console.log("edit button", editButton);
        console.log("del Form array", delFormArray);

        var oneLine = "<b>  Task id: </b> "+ iD + " <b>  Task: </b>" + name + " " +  "<b>  Deadline: </b>" + toDoBy;

        thisDiv.innerHTML = oneLine;
        //thisDiv.appendChild(editButton);
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

