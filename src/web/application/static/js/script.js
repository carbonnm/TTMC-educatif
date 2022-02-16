//Focus on the enter a url part.
$('#url').focus();
$('#url').select();

function enterURL() {
    if ($('#urlSearch').val() === "") {
        alert('Veuillez rentrer un URL Valide')
    }
}
enterURL();