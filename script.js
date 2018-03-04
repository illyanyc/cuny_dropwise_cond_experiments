var videos = [];
var unique;
var dict  = {};
var counter = 0;
var loadingol = 0;
var kepid = "Kep;"

var tag = document.createElement('script');
tag.src = "https://www.youtube.com/player_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

$(window).on("load", function() {

    loadImage();
    loadImage();
    loadImage();

});

$(window).on("scroll", function() {
	var scrollHeight = $(document).height();
	var scrollPosition = $(window).height() + $(window).scrollTop();
	if ((scrollHeight - scrollPosition) / scrollHeight === 0) {
		loadImage();
	}
});

function YouTubeGetID(url){
    var ID = '';
    url = url.replace(/(>|<)/gi,'').split(/(vi\/|v=|\/v\/|youtu\.be\/|\/embed\/)/);
    if(url[2] !== undefined) {
        ID = url[2].split(/[^0-9a-z_\-]/i);
        ID = ID[0];
    }
    else {
        ID = url;
    }
    return ID;
}


Array.prototype.unique = function() {
    return this.filter(function (value, index, self) {
        return self.indexOf(value) === index;
    });
}

function ListOfSamples(array){
    var list = array;
    var uniqueList = [];

    for (i = 0; i < list.length; i++) {
        uniqueList.push(list[i][0])
    }
    unique = uniqueList.unique();


    return unique;

}

function Setdata(csv, callback){
    videos = csvToArray(csv);

    callback();
}

function csvToArray (csv) {
    rows = csv.split("\n");

    return rows.map(function (row) {
        return row.split(",");
    });


};

function populateDict(){
    var listOfsamples = ListOfSamples(videos);
    var data = videos;
    var c = 0
    for (i = 0; i < listOfsamples.length; i++){
        var arr = [];
        var name = listOfsamples[i];
        for (j = 0; j < data.length; j++){
            var experimentType = data[j][0];
            if (name === experimentType ){

                arr.push(data[j]);

            }
        }
        dict[c]=arr;
        c = c + 1;



    }
    console.log(dict);
}



function loadImage() {

    var arr = dict[counter];
    var dictlenght = Object.keys(dict).length;

    if (counter < dictlenght)
    {
        var samplename = arr[0][0];
        var string  = "";

            for (i = 0; i < arr.length; i++)
            {
                var line = arr[i];
                console.log(arr);

                var vid = line[0];
                var trial = line [1];
                var URL = line[2];
                var info = line[3];

                var id = YouTubeGetID(URL);

                var iframeMarkup =

                    '<iframe width="300" height="160" src='+ '"' +
                    URL + '"' + 'frameborder="0" allow="encrypted-media" allowfullscreen></iframe>'

                string = string + '<div class="sample">+<div class="title-minor">'+vid+'-'+trial+'</div>'+
                     iframeMarkup + '<textarea rows="3" cols="30">' +info  +'</textarea>'
                    +'</div>';


                     setTimeout(function () {
                        kepid = '#kep'+ counter;
                        $(kepid).fadeIn(300);
                        loadingol = 0;
                     }, 300);


            }

            counter = counter + 1;
        $( "#gallery" ).append('<span class="title">'+ samplename + '</span>'+'<p></p>' +'<div class="flex-container">' + string +'</span>');
        console.log("Pass")
    }

}

$(window).scroll(function() {
    var height = $(window).scrollTop();
    if (height > 100) {
        $('#back2Top').fadeIn();
    } else {
        $('#back2Top').fadeOut();
    }
});


$(document).ready(function() {

    $(document).ready(function() {
        $.ajax({
            type: "GET",
            url: "videos.csv",
            dataType: "text",
            success: function(data) {Setdata(data, function() {
                populateDict();
                loadImage();
                loadImage();
                loadImage();
                loadImage();
                loadImage();
                loadImage();

            });
                }
        });
    });

    $("#back2Top").click(function(event) {
        event.preventDefault();
        $("html, body").animate({ scrollTop: 0 }, "slow");
        return false;
    });


});