var $resultContainer = $('#resultContainer');
var $infoContainer = $('#infoContainer');

var showSpinnter = function(){
    $('<img src="/static/spinner.gif" id="spinner">').appendTo($resultContainer);
};

var loadInfo = function(place){
    var $place = $('<div/>',{
        class:'result',
        name:place.name+'_info',
        html:'<h3>'+place.name+'</h3>'
    });
    
    var $info = $('<p>'+place.info+' </p>');
    $('<a/>',{
        html:'...',
        href:'/services/redirect/info/'+place.name,
        target:'_blank'
    }).appendTo($info);
    $info.appendTo($place);
    
    $('<a/>',{
        html:'Get Me There!',
        href:'/services/redirect/travel/'+place.name,
        target:'_blank'
    }).appendTo($place);
    $infoContainer.html($place);
};

var InfoRequest = {
    makeRequest:function(placeName){
        $.ajax({
            url:'/services/info/'+placeName,
            type:'GET',
            dataType:'json',
            success:this.succeed,
            error:this.failed
        });
    },
    succeed:function(response){
        console.log(response);
        loadInfo(response);
        console.log('Success!');
    },
    failed:function(response){
        console.error('Could not get result');
        console.log(response);
    }
};

var buildResultNode = function(place_name, weight){
    var fontSize = weight * window.innerWidth;
    var $place = $('<button/>',{
        class:'result',
        html:place_name,
        name:place_name+'_result',
        css:{'fontSize':fontSize + 'px'},
    });
    $place.click(function(){
        InfoRequest.makeRequest(place_name);
    });
    return $place;
};

var buildResultGraph = function(places){
    // var $target = buildResultNode($('#searchbox').val(),1);
    // $target.appendTo($resultContainer);
    
    for (var i in places){
        var place = places[i];
        if (place[1] >= 1) continue;
        var $candidate = buildResultNode(place[0],place[1]);
        $candidate.appendTo($resultContainer);
    }
};

var SearchRequest = {
    makeRequest:function(searchTerm){
        showSpinnter();
        $.ajax({
            url:'/services/suggest/'+searchTerm,
            type:'GET',
            dataType:'json',
            success:this.succeed,
            error:this.failed
        });
    },
    succeed:function(response){
        console.log(response);
        buildResultGraph(response);
        console.log('Success!');
        $('#spinner').detach();
    },
    failed:function(response){
        console.error('Could not get result');
        console.log(response);
        $('#spinner').detach();
    }
};

$(document).ready(function(){
    $('#searchButton').click(function(){
        $infoContainer.empty();
        $resultContainer.empty();
        SearchRequest.makeRequest($('#searchbox').val());
    });
    $('#searchbox').keyup(function(event){
        if(event.keyCode==13){
            $('#searchButton').click();
        }
    });
});
