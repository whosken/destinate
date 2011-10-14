var getInfoLink = function(name){
    return 'http://wikitravel.org/en/'+name;
};
    
var getTravelLink = function(name){
    return 'http://skyscanner.net/'; // TODO: proper link
};

var cleanResults = function(){
    $('#responseContainer').empty();
};
    
var addToResults = function(place){
    var $place = $('<div/>',{
        class:'place',
        name:place.name,
        html:'<h3>'+place.name+'</h3>'
    });
    
    var $info = $('<p>'+place.info+' </p>');
    $('<a/>',{
        html:'...',
        href:'/services/redirect/travel/'+place.name,
        target:'_blank'
    }).appendTo($info);
    $info.appendTo($place);
    
    $('<a/>',{
        html:'Get Me There!',
        href:'/services/redirect/travel/'+place.name,
        target:'_blank'
    }).appendTo($place);
    $('#responseContainer').append($place);
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
        addToResults(response);
        console.log('Success!');
    },
    failed:function(response){
        console.error('Could not get result');
    }
};

var SearchRequest = {
    makeRequest:function(searchTerm){
        $.ajax({
            url:'/services/suggest/'+searchTerm,
            type:'GET',
            dataType:'json',
            success:this.succeed,
            error:this.failed
        });
    },
    succeed:function(response){
        cleanResults();
        for(var i in response[0]){
            InfoRequest.makeRequest(response[0][i]);
        }
        console.log('Success!');
    },
    failed:function(response){
        console.error('Could not get result');
    }
};

$(document).ready(function(){
    $('#searchButton').click(function(){
        SearchRequest.makeRequest($('#searchbox').val());
    });
    $('#searchbox').keyup(function(event){
        if(event.keyCode==13){
            $('#searchButton').click();
        }
    });
});