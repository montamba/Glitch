
let istrue = true
function toggleprofile(){
    let to = document.querySelector(".tprofile");

    to.classList.toggle("down")
    

}



function checkwidth(){
    let n = document.querySelector(".tprofile");
    let b = document.querySelector(".buttons");
    let nn = document.querySelectorAll(".nv");
    if(window.innerWidth < 750){
        
        n.append(...nn)

        n.style.minWidth = "100%"
       n.style.right ="0px"

    }else{
       b.prepend(...nn)
       n.style.minWidth = "200px"
       n.style.right ="50px"

    }

}

function changelocate(){
    let navigations = [...document.querySelectorAll(".nv")]; 
    let locations = ["/home", "/movies", "/about", "/post"];
    for (let i = 0; i < navigations.length; i++) {
        navigations[i].addEventListener("click", () => {
            document.body.innerHTML += `
            <img src="../static/img/background/b3.gif" class="glitcheffect">`
            setTimeout(()=>{window.location.href = locations[i]}, 1000)

        });
    }
}




changelocate()



window.addEventListener("resize",checkwidth)




