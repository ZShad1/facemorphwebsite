
document.addEventListener('DOMContentLoaded', function() {


    var options = {
    data: {
      "All": null,
      "Apple": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg",
      "Google": "https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg",
      "Microsoft": null
    },
    onAutocomplete:function(x) {
      for (i = 0; i < 5; i++) {
          var inputBox = "celebselect" + i;

          if (document.getElementById(inputBox).value === "") {
              document.getElementById(inputBox).value = x;
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


    });



