get_data();
$(document).ready(function() {
    $('#registerBtn').click(function() {
        // Get the username from the form
        const username = $('#username').val();
        $('#username').val("");
        $.ajax({
            type: 'POST',
            url: 'http://54.179.120.53:5000/check_user',
            data: JSON.stringify({username: username, method: 'register'}),
            dataType: 'json',
            contentType:"application/json",
            success: function(data) {
                console.log(data.message)
            },
            error: function(xhr, textStatus, errorThrown) {
                // Display an error message
                console.log(username)
            }
        });
    });
    $('#loginBtn').click(function() {
        // Get the username from the form
        const username = $('#username1').val();
        $('#username1').val("");
        $.ajax({
            type: 'POST',
            url: 'http://54.179.120.53:5000/check_user',
            data: JSON.stringify({username: username, method: 'login'}),
            dataType: 'json',
            contentType:"application/json",
            success: function(data) {
                if (data.status == 'success') {
                    console.log(data.user_data)
                }
                console.log(data.message)

            },
            error: function(xhr, textStatus, errorThrown) {
                // Display an error message
                console.log(username)
            }
        });
    });
    $('#submitBtn').click(function() {
        // Get the username from the form
        const pairname = $('#pairname').val();
        $('#pairname').val("");
        $.ajax({
            type: 'POST',
            url: 'http://54.179.120.53:5000/addpair',
            data: JSON.stringify({pairname: pairname}),
            dataType: 'json',
            contentType:"application/json",
            success: function(data) {
                get_data();
            },
            error: function(xhr, textStatus, errorThrown) {
                // Display an error message
                console.log(pairname)
            }
        });
    });
    $('#deleteBtn').click(function() {
        // Get the username from the form
        const pairname = $('#pairname1').val();
        $('#pairname1').val("");
        $.ajax({
            type: 'POST',
            url: 'http://54.179.120.53:5000/removepair',
            data: JSON.stringify({pairname: pairname}),
            dataType: 'json',
            contentType:"application/json",
            success: function(data) {
                get_data();
            },
            error: function(xhr, textStatus, errorThrown) {
                // Display an error message
                console.log(pairname)
            }
        });
    });
});

function get_data() {
    $.ajax({
    url: "http://54.179.120.53:5000/getdata",
    type: "GET",
    dataType: "json",
    success: function(data) {
        // Do something with the retrieved data
        if (data.status=='error') {
            console.log('invalid ticker');
        }
        else {
            const rows = data.rows;
            const table = document.getElementById('table-body');
            table.innerHTML =
            `<tr>
                <th scope="col">ID</th>
                <th scope="col">NAME</th>
                <th scope="col">BUY</th>
                <th scope="col">SELL</th>
                <th scope="col">VOL</th>
            </tr>`;
            for (let i = 0; i < rows.length; i++) {
                const row = rows[i];
                console.log(rows[i]);
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
        }
    },
    error: function(jqXHR, textStatus, errorThrown) {
        // Handle any errors
        console.log("Error:", textStatus, errorThrown);
    }
    });
}


