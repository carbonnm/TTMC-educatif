//Function that will add each game to the table games with the associated actions
function addGame(gameName) {
    //Add a row
    const $row = $(document.createElement('tr'));

    //Name of the game in a cell
    const $nameGame = $(document.createElement('td')).text(gameName);

    //Different actions we can do here
    const $startSynchro = $(document.createElement('button'))
        .attr('class', 'btn btn-primary')
        .on('click', () => {
            startSynchro();
        });

    //Inner = What will be displayed in the button
    const $startSynchroInner = $(document.createElement('span'))
        .text('Mode synchrone')
        .attr('class', 'badge');
    
    const $startAsync = $(document.createElement('button'))
        .attr('class', 'btn btn-primary')
        .on('click', () => {
            startAsync();
        });
    
    const $startAsyncInner = $(document.createElement('span'))
        .text('Mode asynchrone')
        .attr('class', 'badge');
    
    const $accessResults = $(document.createElement('button'))
        .attr('class', 'btn btn-primary')
        .on('click', () => {
            accessResults();
        });

    const $accessResultsInner = $(document.createElement('span'))
        .text('Résultats')
        .attr('class', 'badge');
    
    const $editGame = $(document.createElement('button'))
        .attr('class', 'btn btn-warning')
        .on('click', () => {
            editGame(game.id);
        });

    const $editGameInner = $(document.createElement('span'))
        .text('Modifier')
        .attr('class', 'badge');
    
    const $deleteGame = $(document.createElement('button'))
        .attr('class', 'btn btn-danger')
        .on('click', () => {
            deleteGame(game.id);
        });
    
    const $deleteGameInner = $(document.createElement('span'))
        .text('Supprimer')
        .attr('class', 'badge');

    $('#gameTbody').append(
        $row.append(
            $nameGame,
            $(document.createElement('td')).append(
                $startSynchro.append($startSynchroInner),
                $startAsync.append($startAsyncInner),
                $accessResults.append($accessResultsInner),
                $editGame.append($editGameInner),
                $deleteGame.append($deleteGameInner)
            )
        )
    );
}


//Listen the doc to undertsand whenerver a game is added
document.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch(`/api/profile/gameName`);

    for (const gameName of await response.json()) {
        addGame(gameName);
    }
});