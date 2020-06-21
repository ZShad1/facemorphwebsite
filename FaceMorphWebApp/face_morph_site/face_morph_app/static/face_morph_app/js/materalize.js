
document.addEventListener('DOMContentLoaded', function() {


    var options = {
    data: {

    },
    onAutocomplete:function(name) {
      for (i = 0; i < 5; i++) {
          var inputBox = "celebselect" + i;
          var button = "removeceleb" + i;

          if (document.getElementById(inputBox).value == "") {
              document.getElementById(inputBox).value = name;
              document.getElementById(button).style.visibility = "visible";

               // show submit button if theres a file and name picked or if theres two names picked
              if (i == 0 && document.getElementById("document").files.length > 0  || i == 1) {
                document.getElementById("submitButton").className = "waves-effect waves-light btn-floating red btn-large";
              }
              break;
          }
      }
    }
};


    var namesList = document.getElementById("celebs").innerHTML;
    namesList = namesList.split(','); // split by commas, this contains at least names and urls within the same index

    for (var index in namesList) {
        var splitQuotes = namesList[index].split('"');
        options['data'][splitQuotes[1]] = null; //splitquotes[3] is the url
    }


    var elems = document.querySelectorAll('.autocomplete');
    var instances = M.Autocomplete.init(elems, options);


    }
);


//document.addEventListener('DOMContentLoaded', function() {
//    var elems = document.querySelectorAll('.materialboxed');
//    var instances = M.Materialbox.init(elems, options);
//  });

document.getElementById("document").addEventListener("input", function() {
    if (document.getElementById("document").files.length > 0 && document.getElementById("removeceleb0").style.visibility == "visible") {
        document.getElementById("submitButton").className = "waves-effect waves-light btn-floating red btn-large";
    }
});

document.getElementById("removeceleb0").addEventListener("click", function() {
    removeCelebs("0")
    });
document.getElementById("removeceleb1").addEventListener("click", function() {
    removeCelebs("1")
    });
document.getElementById("removeceleb2").addEventListener("click", function() {
    removeCelebs("2")
    });

document.getElementById("removeceleb3").addEventListener("click", function() {
    removeCelebs("3")
    });

document.getElementById("removeceleb4").addEventListener("click", function() {
    removeCelebs("4")
    });

function removeCelebs(celebIndex) {
    document.getElementById("celebselect" + celebIndex).value = "";
    document.getElementById("removeceleb" + celebIndex).style.visibility = "hidden";



     if (celebIndex != "4") { // if we're dealing with indexes other than 4, we have to ensure there are no holes in the list
        for (i = 1; i < 5; i++) {
            indexAsStr = (i-1).toString();
            indexPlusStr = (i).toString();
            if (document.getElementById("celebselect" + indexAsStr).value == "" && document.getElementById("celebselect"+ indexPlusStr).value != "") { // adjusting the list

                document.getElementById("celebselect" + indexAsStr).value = document.getElementById("celebselect"+ indexPlusStr).value; // move up element up if its empty and the textbox under it isnt
                document.getElementById("celebselect"+ indexPlusStr).value = "";

                // now adjust the buttons
                document.getElementById("removeceleb" + indexAsStr).style.visibility = "visible";
                document.getElementById("removeceleb" + indexPlusStr).style.visibility = "hidden";
        }
    }
    }

    // hide submit button if theres no file and only one name is picked OR hide it if there are no names picked
    if (document.getElementById("document").files.length == 0 && document.getElementById("removeceleb1").style.visibility == "hidden" || document.getElementById("removeceleb0").style.visibility == "hidden") {
        document.getElementById("submitButton").className = "waves-effect waves-light disabled btn-floating red btn-large";

    }

}
