//Focus on the enter a url part.
$('#url').focus();
$('#url').select();

function enterURL() {
    if ($('#url').val() === "") {
        aler('Veuillez rentrer un URL Valide')
    }
}