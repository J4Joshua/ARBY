$.ajax({
  url: "http://54.179.120.53:5000/data",
  type: "GET",
  dataType: "json",
  success: function(data) {
    // Do something with the retrieved data
    var array = data[0];
    $('#id1').append(array[0]);
    $('#name1').append(array[1]);
    console.log(data);
  },
  error: function(jqXHR, textStatus, errorThrown) {
    // Handle any errors
    console.log("Error:", textStatus, errorThrown);
  }
});
