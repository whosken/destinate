var map = function(doc) {
  if (doc.profile)
    for (var word in doc.profile)
      emit(word, [doc._id]);
};

var reduce = function(keys,values,rereduce) {
  var result = values[0];
  for (var i in values)
    var value = values[i];
    for (var j in value)
      var name = value[j];
      if (result.indexOf(name) < 0)
        result.push(name);
  return result;
};