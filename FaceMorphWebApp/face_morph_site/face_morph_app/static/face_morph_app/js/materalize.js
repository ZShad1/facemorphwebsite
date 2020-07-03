
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

              document.getElementById("celebDesc" +i.toString()).innerHTML = celebDesc[name];

              // saving the images url to be used in FaceMorph.py
              document.getElementById("celebURL" +i.toString()).value = celebUrls[name];

              // css adjustments for button, pictures, and icons
              document.getElementById(button).style.visibility = "visible";
              document.getElementById("anonIcon" + i.toString()).style.display = "none";
              document.getElementById("celebPicture" + i.toString()).style.display = "inline-block";
              document.getElementById("celebPicture" + i.toString()).src = celebUrls[name]
              document.getElementById("celebPicture" + i.toString()).style.width = '100%';
              document.getElementById("celebPicture" + i.toString()).style.height = 'auto';



               // show submit button if theres a file and name picked or if theres two names picked
              if (i == 0 && document.getElementById("document").files.length > 0  || i == 1) {
                document.getElementById("submitButton").className = "waves-effect waves-light btn-floating red btn-block";
              }
              break;
          }
      }
    }
};

    // this is the list of all the celebrities in celebs.txt
    var namesListURL = document.getElementById("celebs").innerHTML;
    var namesListDesc = document.getElementById("celebsDesc").innerHTML;

    namesListDesc = namesListDesc.replace("', \"", "', '");
    namesListURL = namesListURL.split(','); // split by commas, this contains at least names and urls within the same index
    namesListDesc = namesListDesc.split(", '")


    celebUrls = {};
    celebDesc = {};

    for (var index in namesListDesc) {
        var splitQuotes = namesListURL[index].split('"');
        var splitDesc = namesListDesc[index].split("': '");

        if (splitDesc.length == 1) {
            splitDesc = namesListDesc[index].replace("': \"", "': '");
            splitDesc = splitDesc.split("': '");

        }

        if (index == 0) {
            tempString = "";
            for (var i = 6; i < splitQuotes[1].length; i++) {
                tempString = tempString + splitQuotes[1][i];
                }
            splitQuotes[1] = tempString;
            }
        options['data'][splitQuotes[1]] = null; //splitquotes[3] is the url
        celebUrls[splitQuotes[1]] = splitQuotes[3];
        if (typeof splitDesc[1] == 'string') {
            celebDesc[splitDesc[0]] = splitDesc[1].slice(0,-1);
        }
    }


    var elems = document.querySelectorAll('.autocomplete');
    var instances = M.Autocomplete.init(elems, options);


    }
);


document.addEventListener('DOMContentLoaded', function() {
    var options = {}
    var elems = document.querySelectorAll('.materialboxed');
    var instances = M.Materialbox.init(elems, options);
  });

document.getElementById("document").addEventListener("input", function() {
    if (document.getElementById("document").files.length > 0 && document.getElementById("removeceleb0").style.visibility == "visible") {
        document.getElementById("submitButton").className = "waves-effect waves-light btn-floating red btn-block";
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
    document.getElementById("celebPicture" + celebIndex).style.display = "none";
    document.getElementById("anonIcon" + celebIndex).style.display = "block";
    document.getElementById("celebURL" + celebIndex).value = "";
    document.getElementById("celebDesc" + celebIndex).innerHTML = "";


     if (celebIndex != "4") { // if we're dealing with indexes other than 4, we have to ensure there are no holes in the list
        for (i = 1; i < 5; i++) {
            indexAsStr = (i-1).toString();
            indexPlusStr = (i).toString();
            if (document.getElementById("celebselect" + indexAsStr).value == "" && document.getElementById("celebselect"+ indexPlusStr).value != "") { // adjusting the list

                //adjust names
                document.getElementById("celebselect" + indexAsStr).value = document.getElementById("celebselect"+ indexPlusStr).value; // move up element up if its empty and the textbox under it isnt
                document.getElementById("celebselect"+ indexPlusStr).value = "";

                //adjust icons and pictures and desc
                document.getElementById("celebPicture" + indexAsStr).src = document.getElementById("celebPicture" + indexPlusStr).src;
                document.getElementById("celebURL" + indexAsStr).value = document.getElementById("celebPicture" + indexPlusStr).src;
                document.getElementById("celebURL" + indexPlusStr).value = "";
                document.getElementById("celebPicture" + indexPlusStr).style.display = "none";
                document.getElementById("anonIcon" + indexAsStr).style.display = "none";
                document.getElementById("anonIcon" + indexPlusStr).style.display = "block";
                document.getElementById("celebPicture" + indexAsStr).style.display = "block";
                document.getElementById("celebDesc" + indexAsStr).innerHTML = document.getElementById("celebDesc" + indexPlusStr).innerHTML;
                document.getElementById("celebDesc" + indexPlusStr).innerHTML = "";


                // now adjust the buttons
                document.getElementById("removeceleb" + indexAsStr).style.visibility = "visible";
                document.getElementById("removeceleb" + indexPlusStr).style.visibility = "hidden";
        }
    }
    }

    // hide submit button if theres no file and only one name is picked OR hide it if there are no names picked
    if (document.getElementById("document").files.length == 0 && document.getElementById("removeceleb1").style.visibility == "hidden" || document.getElementById("removeceleb0").style.visibility == "hidden") {
        document.getElementById("submitButton").className = "waves-effect waves-light disabled btn-floating red btn-block";

    }

}
