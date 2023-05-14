$.ajax({
  url: "http://54.179.120.53:5000/data",
  type: "GET",
  dataType: "json",
  success: function(data) {
    // Do something with the retrieved data
    var array = data[0];
    console.log(data);
  },
  error: function(jqXHR, textStatus, errorThrown) {
    // Handle any errors
    console.log("Error:", textStatus, errorThrown);
  }
});
$.ajax({
  url: "http://192.168.5.45:5000/api/ticker/book",
  type: "GET",
  dataType: "json",
  success: function(data) {
    // Do something with the retrieved data
    const rows = data.rows;
    const table = document.getElementById('table-body');
    console.log(rows);
    for (let i = 0; i < rows.length; i++) {
        const row = rows[i];
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <th scope="row">${i+1}</th>
          <td>${row.symbol}</td>
          <td>${row.bidPrice}</td>
          <td>${row.askPrice}</td>
          <td>${row.bidQty + row.askQty}</td>
        `;
        table.appendChild(tr);
    }
    console.log(data);
  },
  error: function(jqXHR, textStatus, errorThrown) {
    // Handle any errors
    console.log("Error:", textStatus, errorThrown);
  }
});


