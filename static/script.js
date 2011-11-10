var cleanResults = function(){
    $('#responseContainer').empty();
};

var showSpinnter = function(){
    cleanResults();
    $('<img src="/static/spinner.gif" id="spinner">').appendTo($('#responseContainer'));
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
        href:'/services/redirect/info/'+place.name,
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
        for(var i in response[0]){
            InfoRequest.makeRequest(response[0][i]);
        }
        console.log('Success!');
        $('#spinner').detach();
    },
    failed:function(response){
        console.error('Could not get result');
        $('#spinner').detach();
    }
};

$(document).ready(function(){
    $('#searchButton').click(function(){
        showSpinnter();
        SearchRequest.makeRequest($('#searchbox').val());
    });
    $('#searchbox').keyup(function(event){
        if(event.keyCode==13){
            $('#searchButton').click();
        }
    });
});