function ShowPopup(hoveritem)
{
hp = document.getElementById("hoverpopup");

// Set position of hover-over popup
hp.style.top = hoveritem.offsetTop + 18;
hp.style.left = hoveritem.offsetLeft + 20;

// Set popup to visible
hp.style.visibility = "Visible";
}

function HidePopup()
{
hp = document.getElementById("hoverpopup");
hp.style.visibility = "Hidden";
}