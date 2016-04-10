function toggle(el){
    if(el.className!="pause")
    {
        el.src='img/pause.jpg';
        el.className="pause";
        document.getElementById('player').play();
    }
    else if(el.className=="pause")
    {
        el.src='img/play.png';
        el.className="play";
        document.getElementById('player').pause();
    }

    return false;
}

